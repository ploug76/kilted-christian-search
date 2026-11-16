'use strict';
const $=s=>document.querySelector(s);
const PAGE=25;
let DATA=null, curShow='__all', lastResults=[], shown=0, lastQuery=null;
const shardCache=new Map(), textCache=new Map();
const PRIORITY=['Book of Heaven','Church by the Fire'];
const TOK=/[\p{L}\p{N}]+(?:['’][\p{L}\p{N}]+)*/gu;
const norm=s=>s.normalize('NFC').toLowerCase().replace(/’/g,"'");
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmtDate=d=>{if(!d)return 'Date unknown';const [y,m,dd]=d.split('-').map(Number);return new Date(y,m-1,dd).toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'})};
const fmtDur=s=>{if(!s)return '';const t=Math.round(Number(s)/60);const h=Math.floor(t/60);return `${h?h+'h ':''}${t%60}m`};

async function init(){
  const r=await fetch('docs.json'); DATA=await r.json();
  DATA.byShow={};
  for(const d of DATA.docs)(DATA.byShow[d.show]??=[]).push(d);
  DATA.shardKeys=Object.keys(DATA.shards);
  $('#stats').textContent=`${DATA.N.toLocaleString()} episodes · ${(DATA.totalWords/1e6).toFixed(1)}M words, fully searchable`;
  buildTabs(); readState(); run();
}
function buildTabs(){
  const shows=Object.keys(DATA.byShow).sort((a,b)=>{
    const pa=PRIORITY.indexOf(a),pb=PRIORITY.indexOf(b);
    if(pa>=0||pb>=0)return (pa<0?99:pa)-(pb<0?99:pb);
    return DATA.byShow[b].length-DATA.byShow[a].length});
  const t=$('#tabs'); t.innerHTML='';
  const mk=(id,label,n)=>{const b=document.createElement('button');b.className='tab';b.type='button';b.dataset.show=id;b.setAttribute('role','tab');
    b.innerHTML=`${esc(label)}<small>${n}</small>`;b.onclick=()=>{curShow=id;writeState();run();};t.appendChild(b)};
  mk('__all','All shows',DATA.N);
  for(const s of shows)mk(s,s,DATA.byShow[s].length);
}
function markTabs(){for(const b of document.querySelectorAll('.tab')){const on=b.dataset.show===curShow;b.setAttribute('aria-selected',on);if(on)b.scrollIntoView({block:'nearest',inline:'center'})}}
function readState(){const p=new URLSearchParams(location.hash.slice(1));$('#q').value=p.get('q')||'';curShow=p.get('show')||'__all';$('#forms').checked=p.get('forms')==='1';
  if(curShow!=='__all'&&!DATA.byShow[curShow])curShow='__all'}
function writeState(){const p=new URLSearchParams();const q=$('#q').value.trim();if(q)p.set('q',q);if(curShow!=='__all')p.set('show',curShow);if($('#forms').checked)p.set('forms','1');
  history.replaceState(null,'','#'+p.toString())}

// ---------- query parsing ----------
function parseQuery(q){
  const groups=[]; // each: {words:[...], phrase:bool}
  const re=/"([^"]+)"|(\S+)/g; let m;
  while((m=re.exec(q))){const w=(norm(m[1]||m[2]).match(TOK)||[]);if(!w.length)continue;
    if(m[1]&&w.length>1)groups.push({words:w,phrase:true});else for(const x of w)groups.push({words:[x],phrase:false});}
  return groups;
}
function shardKey(S,term){for(let n=term.length;n>=1;n--){const k=term.slice(0,n);if(n===term.length&&S[k+'\0'])return k+'\0';if(S[k])return k}return null}
function shardsFor(S,term,prefix){
  if(!prefix){const k=shardKey(S,term);return k?[k]:[]}
  return Object.keys(S).filter(k=>{const ex=k.endsWith('\0');const kk=ex?k.slice(0,-1):k;return kk.startsWith(term)||(!ex&&term.startsWith(kk))});
}
function loadShard(dir,S,k){const key=dir+'|'+k;
  if(!shardCache.has(key))shardCache.set(key,fetch(dir+'/'+S[k]).then(r=>{if(!r.ok)throw new Error('index '+r.status);return r.json()}));
  return shardCache.get(key);
}
function decode(flat){const m=new Map();let id=0;for(let i=0;i<flat.length;i+=2){id+=flat[i];m.set(id,flat[i+1])}return m}
async function postingsFor(word,prefix,bigram){
  const dir=bigram?'bi':'idx', S=bigram?DATA.bshards:DATA.shards;
  const ks=shardsFor(S,word,prefix); const out=new Map(); const terms=[];
  for(const k of ks){const sh=await loadShard(dir,S,k);
    if(!prefix){if(sh[word]){terms.push(word);for(const [d,n] of decode(sh[word]))out.set(d,(out.get(d)||0)+n)}}
    else for(const t in sh)if(t.startsWith(word)){terms.push(t);for(const [d,n] of decode(sh[t]))out.set(d,(out.get(d)||0)+n)}}
  return out;
}
async function phraseMap(words){ // docs containing every adjacent pair; tf = min pair count (exact for 2 words)
  const maps=await Promise.all(words.slice(1).map((w,i)=>postingsFor(words[i]+' '+w,false,true)));
  const out=new Map();
  for(const [d,n] of maps[0]){let m=n,ok=true;for(const x of maps.slice(1)){const v=x.get(d);if(!v){ok=false;break}m=Math.min(m,v)}if(ok)out.set(d,m)}
  return out;
}
// ---------- search ----------
async function search(q){
  const prefix=$('#forms').checked; const groups=parseQuery(q); if(!groups.length)return null;
  const units=[]; const seen=new Set();
  for(const g of groups){const label=g.phrase?'“'+g.words.join(' ')+'”':g.words[0];if(seen.has(label))continue;seen.add(label);
    units.push({label,phrase:g.phrase,words:g.words,pre:!g.phrase&&prefix&&g.words[0].length>=3})}
  await Promise.all(units.map(async u=>{u.map=u.phrase?await phraseMap(u.words):await postingsFor(u.words[0],u.pre,false)}));
  // bonus: adjacent unquoted words also scored as a phrase (ranks "holy spirit" by the phrase, not just the words)
  const bonus=[];
  for(let i=0;i+1<groups.length;i++)if(!groups[i].phrase&&!groups[i+1].phrase)bonus.push({map:await postingsFor(groups[i].words[0]+' '+groups[i+1].words[0],false,true)});
  const N=DATA.N, avg=DATA.avgdl, k1=1.2, b=0.75;
  const idf=u=>{const df=u.map.size;return Math.log(1+(N-df+.5)/(df+.5))};
  const bm=(u,tf,d)=>tf?idf(u)*tf*(k1+1)/(tf+k1*(1-b+b*d.words/avg)):0;
  let cand=null;
  for(const u of units){const ids=new Set(u.map.keys());cand=cand?new Set([...cand].filter(x=>ids.has(x))):ids}
  let partial=false;
  if(!cand.size&&units.length>1){partial=true;cand=new Set(units.flatMap(u=>[...u.map.keys()]))}
  const res=[];
  for(const id of cand){const d=DATA.docs[id];if(curShow!=='__all'&&d.show!==curShow)continue;
    let s=0;const counts={};
    for(const u of units){const tf=u.map.get(id)||0;counts[u.label]=tf;s+=bm(u,tf,d)}
    for(const u of bonus)s+=1.5*bm(u,u.map.get(id)||0,d);
    res.push({d,score:s,counts});}
  res.sort((a,b)=>b.score-a.score||(b.d.date||'').localeCompare(a.d.date||''));
  return {res,groups,units,uniq:units.map(u=>u.label),partial,prefix};
}
// highlight regex from query (matches raw transcript text)
function hlRegex(Q){
  const B='(?<![\\p{L}\\p{N}])', A="(?![\\p{L}\\p{N}]|['’][\\p{L}\\p{N}])";
  const wordPat=(w,pre)=>{const e=w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/'/g,"['’]");return pre?e+"[\\p{L}\\p{N}'’]*":e+A};
  const alts=Q.groups.map(g=>g.words.map(w=>wordPat(w,!g.phrase&&Q.prefix&&w.length>=3)).join('(?:[^\\p{L}\\p{N}]|\\[\\d\\d:\\d\\d:\\d\\d\\])+'));
  alts.sort((a,b)=>b.length-a.length);
  return new RegExp(B+'(?:'+alts.join('|')+')','giu');
}
function phraseRegex(Q){ // all words adjacent, in order
  if(Q.uniq.length<2&&!Q.groups.some(g=>g.phrase))return null;
  const words=Q.groups.length===1&&Q.groups[0].phrase?Q.groups[0].words:Q.groups.flatMap(g=>g.words);
  if(words.length<2)return null;
  return hlRegex({groups:[{words,phrase:true}],prefix:Q.prefix});
}
async function getText(id){
  if(!textCache.has(id))textCache.set(id,(async()=>{const r=await fetch(`t/${id}.txt.gz`);if(!r.ok)throw new Error('transcript '+r.status);
    const buf=new Uint8Array(await r.arrayBuffer());
    if(buf[0]===0x1f&&buf[1]===0x8b){
      if(!('DecompressionStream' in window))throw new Error('This browser cannot unpack transcripts; please update it.');
      const s=new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'));return await new Response(s).text()}
    return new TextDecoder().decode(buf)})());
  if(textCache.size>60){textCache.delete(textCache.keys().next().value)}
  return textCache.get(id);
}
// ---------- render ----------
async function run(){
  markTabs(); const q=$('#q').value.trim(); const st=$('#status'); $('#results').innerHTML=''; $('#more').hidden=true;
  if(!q){lastQuery=null;const list=curShow==='__all'?DATA.docs:DATA.byShow[curShow];
    lastResults=list.map(d=>({d}));st.textContent=`${list.length} episodes${curShow==='__all'?'':' in '+curShow}, newest first. Type a topic above to search.`;
    shown=0;renderMore();return}
  st.textContent='Searching…';
  try{const Q=await search(q);lastQuery=Q;lastResults=Q?Q.res:[];shown=0;
    if(!Q){st.textContent='Type a word or phrase to search.';return}
    const where=curShow==='__all'?'all shows':curShow;
    if(!lastResults.length){st.textContent=`No episodes in ${where} mention “${q.replace(/"/g,'')}”.`+(Q.prefix?'':' Try ticking “Match word beginnings”.');return}
    st.textContent=`${lastResults.length} episode${lastResults.length>1?'s':''} in ${where} mention “${q.replace(/"/g,'')}”${Q.partial?' (no episode has every word; showing episodes with any of them)':''}, best matches first.`;
    renderMore();
  }catch(e){st.textContent='Search failed: '+e.message+'. Check your connection and try again.'}
}
const io=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){io.unobserve(e.target);fillSnippet(e.target)}},{rootMargin:'300px'});
function renderMore(){
  const box=$('#results');const frag=document.createDocumentFragment();
  for(const r of lastResults.slice(shown,shown+PAGE)){const d=r.d;const c=document.createElement('article');c.className='card';c.dataset.id=d.id;
    const link=d.url||d.audio;const ltxt=d.url?'Listen to episode ↗':'Audio file ↗';
    let counts='';
    if(r.counts){const parts=lastQuery.units.map(u=>`${u.label}${u.pre?'…':''} ×${r.counts[u.label]}`);
      const tot=Object.values(r.counts).reduce((a,b)=>a+b,0);
      const single=lastQuery.units.length===1, u0=lastQuery.units[0];
      counts=`<div class="counts">${single?(u0.phrase?`${tot} time${tot===1?'':'s'} as a phrase`:`${tot} match${tot===1?'':'es'}`):esc(parts.join(' · '))}<span class="phr"></span></div>`}
    c.innerHTML=`<span class="show">${esc(d.show)}</span><h2>${esc(d.title)}</h2>
      <div class="meta">${fmtDate(d.date)}${d.ep?' · Ep '+esc(d.ep):''}${d.dur?' · '+fmtDur(d.dur):''}</div>${counts}
      ${r.counts?'<div class="snip">Loading where it comes up…</div>':''}
      <div class="actions">${link?`<a class="primary" href="${esc(link)}" target="_blank" rel="noopener">${ltxt}</a>`:''}<button type="button" class="read">Read transcript</button></div>`;
    c.querySelector('.read').onclick=()=>openViewer(d);
    frag.appendChild(c); if(r.counts)io.observe(c);}
  box.appendChild(frag); shown+=PAGE; $('#more').hidden=shown>=lastResults.length;
}
function lineStart(text,i){const s=text.lastIndexOf('\n',i);return s<0?0:s+1}
async function fillSnippet(card){
  const Q=lastQuery; if(!Q)return; const id=+card.dataset.id; const sn=card.querySelector('.snip');
  try{const text=await getText(id); if(Q!==lastQuery)return;
    const pr=phraseRegex(Q); let m=null;
    if(pr){const all=text.match(pr);const n=all?all.length:0;const ph=card.querySelector('.phr');
      if(ph&&!(Q.units.length===1&&Q.units[0].phrase&&Q.units[0].words.length===2))ph.textContent=Q.units.length===1&&Q.units[0].phrase?'':` · together as a phrase: ${n}`;
      if(Q.units.length===1&&Q.units[0].phrase&&Q.units[0].words.length>2){const c=card.querySelector('.counts');c.firstChild.textContent=`${n} time${n===1?'':'s'} as a phrase`} pr.lastIndex=0; m=pr.exec(text)}
    const re=hlRegex(Q); if(!m){re.lastIndex=0;m=re.exec(text)}
    if(!m){sn.textContent='(match is in a word form; open the transcript)';return}
    const ls=lineStart(text,m.index); const tsm=text.slice(ls,ls+12).match(/^\[(\d\d:\d\d:\d\d)\]/);
    let a=lineStart(text,Math.max(0,m.index-140)); let z=text.indexOf('\n',Math.min(text.length,m.index+m[0].length+160)); if(z<0)z=text.length;
    let piece=text.slice(a,z).replace(/\[\d\d:\d\d:\d\d\]\s*/g,'').replace(/\s+/g,' ');
    sn.innerHTML=(tsm?`<span class="ts">${tsm[1]}</span>`:'')+(a>0?'…':'')+highlight(piece,hlRegex(Q))+(z<text.length?'…':'');
  }catch(e){sn.textContent='Could not load the transcript ('+e.message+').'}
}
function highlight(s,re){let out='',last=0;re.lastIndex=0;let m;while((m=re.exec(s))){out+=esc(s.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;if(!m[0].length)re.lastIndex++}
  return out+esc(s.slice(last))}
// ---------- viewer ----------
let vMarks=[],vIdx=-1;
async function openViewer(d){
  const v=$('#viewer'); v.hidden=false; document.body.style.overflow='hidden';
  $('#vTitle').textContent=d.title; $('#vMeta').textContent=`${d.show} · ${fmtDate(d.date)}`;
  const link=d.url||d.audio; $('#vLink').href=link; $('#vLink').textContent=d.url?'Episode ↗':'Audio ↗';
  const body=$('#vBody'); body.textContent='Loading transcript…'; $('#vCount').textContent='';
  history.pushState({viewer:1},'',location.hash);
  try{const text=await getText(d.id);
    body.innerHTML=lastQuery?highlight(text,hlRegex(lastQuery)):esc(text);
    vMarks=[...body.querySelectorAll('mark')]; vIdx=-1;
    $('#vCount').textContent=lastQuery?`${vMarks.length} highlighted`:`${d.words.toLocaleString()} words`;
    body.scrollTop=0; if(vMarks.length)step(1);
  }catch(e){body.textContent='Could not load the transcript ('+e.message+').'}
}
function step(n){if(!vMarks.length)return;if(vIdx>=0)vMarks[vIdx].classList.remove('cur');vIdx=(vIdx+n+vMarks.length)%vMarks.length;
  const m=vMarks[vIdx];m.classList.add('cur');m.scrollIntoView({block:'center'});$('#vCount').textContent=`${vIdx+1} of ${vMarks.length}`}
function closeViewer(){$('#viewer').hidden=true;document.body.style.overflow=''}
$('#vClose').onclick=()=>{if(history.state&&history.state.viewer)history.back();else closeViewer()};
window.addEventListener('popstate',()=>{if(!$('#viewer').hidden)closeViewer()});
$('#vPrev').onclick=()=>step(-1); $('#vNext').onclick=()=>step(1);
$('#searchForm').onsubmit=e=>{e.preventDefault();$('#q').blur();writeState();run()};
$('#forms').onchange=()=>{writeState();if($('#q').value.trim())run()};
$('#more').onclick=renderMore;
// ---------- install / offline ----------
let deferred=null;
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferred=e;$('#installBtn').hidden=false});
$('#installBtn').onclick=async()=>{if(!deferred)return;deferred.prompt();await deferred.userChoice;deferred=null;$('#installBtn').hidden=true};
if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
init().catch(e=>{$('#stats').textContent='Could not load episode list: '+e.message});
