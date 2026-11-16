import sys, asyncio
from playwright.async_api import async_playwright
BASE=sys.argv[1]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=await (await b.new_context(viewport={'width':390,'height':844})).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(BASE); await pg.wait_for_selector('.tab')
    for q in ['"the blood of jesus"','"church by the fire"','"thanks for watching"','conlee','"Kilted Christian"','"Brothers and a Bible"','Khazarian','Evren','"I pray for you guys"']:
      await pg.fill('#q',q); await pg.click('.search button')
      await pg.wait_for_function("!document.querySelector('#status').textContent.startsWith('Searching')"); await pg.wait_for_timeout(1200)
      st=await pg.text_content('#status')
      first=await pg.eval_on_selector('.card','c=>[c.querySelector("h2").textContent,c.querySelector(".counts").textContent,c.querySelector(".snip").innerHTML.slice(0,400)]') if await pg.query_selector('.card') else None
      print('Q',q,'|',st,'\n  ',first)
    print('errors',errs); await b.close()
asyncio.run(main())
