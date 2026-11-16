import json,gzip,re,random,collections,unicodedata,os,sys
OUT='site'; D=json.load(open(f'{OUT}/docs.json'))
TS=re.compile(r'^\[\d\d:\d\d:\d\d\]\s*', re.M); TOK=re.compile(r"[^\W_]+(?:['’][^\W_]+)*")
norm=lambda s: unicodedata.normalize('NFC', s).casefold().replace('’',"'")
docs=D['docs']; N=len(docs); problems=[]
assert [d['id'] for d in docs]==list(range(N))
for k,f in list(D['shards'].items()):
    if not os.path.exists(f'{OUT}/idx/{f}'): problems.append('missing shard '+f)
for k,f in list(D['bshards'].items()):
    if not os.path.exists(f'{OUT}/bi/{f}'): problems.append('missing bshard '+f)
toks={}; words=0
for d in docs:
    p=f"{OUT}/t/{d['id']}.txt.gz"
    t=gzip.open(p).read().decode()
    tk=TOK.findall(norm(TS.sub('',t))); toks[d['id']]=tk
    if len(tk)!=d['words']: problems.append(f"word count mismatch id{d['id']}")
    if len(tk)<500: problems.append(f"short transcript id{d['id']} ep{d['ep']} {len(tk)} words")
    words+=len(tk)
assert words==D['totalWords'], (words,D['totalWords'])
def shard_for(S,term):
    for n in range(len(term),0,-1):
        k=term[:n]
        if n==len(term) and k+'\0' in S: return S[k+'\0']
        if k in S: return S[k]
cache={}
def post(dir,S,term):
    f=shard_for(S,term)
    if f not in cache: cache[f]=json.load(open(f'{OUT}/{dir}/{f}'))
    flat=cache[f].get(term)
    if flat is None: return {}
    out={};i=0
    for j in range(0,len(flat),2): i+=flat[j]; out[i]=flat[j+1]
    return out
random.seed(11)
AL={v:k for k,vs in D.get('aliases',{}).items() for v in vs}
vocab=collections.Counter(); 
for tk in toks.values(): vocab.update(tk)
terms=random.sample(sorted(vocab),400)+['jesus','forgiveness','conlee','evren','ephesians','calvary','epstein','khazarian','podbean','godcast','kilted']
bad=0
for w in terms:
    exp={}
    for i,tk in toks.items():
        n=sum(1 for x in tk if x==w or AL.get(x)==w)
        if n: exp[i]=n
    got=post('idx',D['shards'],w)
    if exp!=got: bad+=1; problems.append(f'unigram mismatch {w}: exp {len(exp)} docs got {len(got)}')
pairs=[]
for _ in range(150):
    i=random.randrange(N); tk=toks[i]; j=random.randrange(len(tk)-1); pairs.append(tk[j]+' '+tk[j+1])
pairs+=['holy spirit','born again','brothers and','and a','the conlee','kilted christian','msm liars','book of']
for p in pairs:
    a,b=p.split(' ')
    exp={}
    for i,tk in toks.items():
        ta=[AL.get(x,x) for x in tk]
        n=sum(1 for k in range(len(tk)-1) if (tk[k],tk[k+1])==(a,b) or ((ta[k],ta[k+1])==(a,b) and (tk[k],tk[k+1])!=(a,b)))
        if n: exp[i]=n
    got=post('bi',D['bshards'],p)
    if exp!=got: problems.append(f'bigram mismatch {p!r}: exp {len(exp)} got {len(got)}')
print('checked',len(terms),'terms and',len(pairs),'bigrams;',len(problems),'problems')
for x in problems[:40]: print(' ',x)
