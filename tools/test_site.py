import sys, asyncio, json
from playwright.async_api import async_playwright
BASE=sys.argv[1]; SHOT=sys.argv[2] if len(sys.argv)>2 else None
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(BASE); await pg.wait_for_selector('.tab'); 
    print('stats:',await pg.text_content('#stats'))
    tabs=await pg.eval_on_selector_all('.tab','els=>els.map(e=>e.textContent)'); print('tabs',len(tabs),tabs[:4])
    for q in ['forgiveness','prophecy','"Holy Spirit"','holy spirit','"born again"','resurrection']:
      await pg.fill('#q',q); await pg.click('.search button')
      await pg.wait_for_function("!document.querySelector('#status').textContent.startsWith('Searching')")
      await pg.wait_for_timeout(1500)
      st=await pg.text_content('#status')
      first=await pg.eval_on_selector('.card','c=>[c.querySelector(".show").textContent,c.querySelector("h2").textContent,c.querySelector(".counts").textContent,c.querySelector(".snip").innerHTML.slice(0,260),c.querySelector("a").href]')
      print('Q',q,'|',st,'\n  ',first)
    # tabs filter
    for name in ['Book of Heaven','Church by the Fire']:
      await pg.click(f'.tab[data-show="{name}"]'); await pg.wait_for_function("!document.querySelector('#status').textContent.startsWith('Searching')"); await pg.wait_for_timeout(500)
      shows=await pg.eval_on_selector_all('.card .show','e=>[...new Set(e.map(x=>x.textContent))]')
      print('TAB',name,await pg.text_content('#status'),shows)
      if name=='Book of Heaven' and SHOT:
        await pg.wait_for_timeout(1500); await pg.screenshot(path=SHOT)
    # viewer
    await pg.click('.card .read'); await pg.wait_for_function("document.querySelector('#vCount').textContent.includes('of')",timeout=15000)
    print('viewer',await pg.text_content('#vCount'),await pg.text_content('#vTitle'))
    if SHOT: await pg.screenshot(path=SHOT.replace('.png','-transcript.png'))
    await pg.click('#vClose'); await pg.wait_for_timeout(300)
    print('viewer hidden',await pg.is_hidden('#viewer'))
    # no query browse
    await pg.fill('#q',''); await pg.click('.tab[data-show="__all"]'); await pg.wait_for_timeout(300); print('browse',await pg.text_content('#status'))
    sw=await pg.evaluate("navigator.serviceWorker.getRegistration().then(r=>!!r)"); print('sw',sw)
    w=await pg.evaluate("document.documentElement.scrollWidth"); print('scrollWidth',w)
    print('errors',errs); await b.close()
asyncio.run(main())
