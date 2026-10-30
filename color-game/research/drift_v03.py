#!/usr/bin/env python3
"""DRIFT v0.3 prototype sim — Riven's package: harmony accrual (intensity-capped),
drift hungers harmony (slide resets harmony), frequency scales with board harmony,
diplomatic half-rent, finish-the-round. Interpretations logged in-output."""
import json, re, random
from decimal import Decimal, ROUND_HALF_UP

html = open('/root/.openclaw/workspace/creative/projects/color-game/index.html').read()
rows = re.findall(r'\["(\w+)","(\w+)",(-?\d),(\d)\]', html)
LEX = {i: {'w': w, 'f': f, 'v': int(v), 'i': int(n)} for i, (w, f, v, n) in enumerate(rows)}
SHARP = {frozenset(['CHAOS','ORDER']), frozenset(['EROS','GRIEF'])}
RICH = {frozenset(['LIFE','GRIEF']), frozenset(['NUMERAL','EROS']), frozenset(['LIFE','CHAOS']),
         frozenset(['ORDER','EROS']), frozenset(['GRIEF','NUMERAL']), frozenset(['ORDER','GRIEF'])}
RES = {frozenset(['Garden','Harvest']), frozenset(['Oath','Verdict']), frozenset(['Sum','Zero']),
        frozenset(['Dirge','Hollow']), frozenset(['Heat','Sweat']), frozenset(['Storm','Flood'])}
WIN, MAXT = 60, 24
THRESH = 0.50          # Riven ceiling
RESET_CD = 3           # interpretation: harmony reset = post-slide accrual cooldown (turns)
FREQ_K = 8             # interpretation: extra drift events per endTurn = totalBoardHarmony // FREQ_K
random.seed(7)

def fresh(n1, n2):
    return {"turn":0,"players":[{"name":n1,"score":0,"placed":0},{"name":n2,"score":0,"placed":0}],
            "enclaves":[None,None],"spent":[0,0],"bank":[0,0],"cool":[0]*64,
            "board":[None]*64,"log":[],"winner":None,"driftCycles":0}

def adj(b):
    out=[]
    for c in range(64):
        r,co=divmod(c,8)
        for dr,dc in ((0,1),(1,0)):
            r2,co2=r+dr,co+dc
            if r2<8 and co2<8 and b[c] and b[r2*8+co2]: out.append((c,r2*8+co2))
    return out

def meaning(b,a,bb):
    A,B=b[a],b[bb]; la,lb=LEX[A['tok']],LEX[B['tok']]
    if A['attuned'] or B['attuned']: return 0
    if la['f']==lb['f']:
        return 1 if frozenset([la['w'],lb['w']]) in RES else 0
    t = 3 if frozenset([la['f'],lb['f']]) in SHARP else (2 if frozenset([la['f'],lb['f']]) in RICH else 1)
    return t*(1+min(3,abs(A['v']-B['v'])))

def recompute(S):
    b=S['board']
    for p in S['players']: p['score']=0
    for a,bb in adj(b):
        m=meaning(b,a,bb)
        if m==0: continue
        oa,ob=b[a]['owner'],b[bb]['owner']
        if oa==ob: S['players'][oa]['score']+=m
        else: S['players'][oa]['score']+=m//2; S['players'][ob]['score']+=m//2
    for i,p in enumerate(S['players']):
        p['score']+=S['bank'][i]-S['spent'][i]
    ps=adj(b)
    S['drift']= round(sum(pull(b,a,bb) for a,bb in ps)/(4*len(ps)),4) if ps else 0

def pull(b,a,bb): return 4-min(4,abs(b[a]['v']-b[bb]['v']))

def harmony_of(b,c):
    """harmony(c) = count of same-field orthogonal neighbors."""
    if not b[c]: return 0
    f=LEX[b[c]['tok']]['f']; r,co=divmod(c,8); n=0
    for dr,dc in ((0,1),(0,-1),(1,0),(-1,0)):
        r2,c2=r+dr,co+dc
        if 0<=r2<8 and 0<=c2<8 and b[r2*8+c2] and LEX[b[r2*8+c2]['tok']]['f']==f: n+=1
    return n

def total_harmony(b): return sum(harmony_of(b,c) for c in range(64) if b[c])

def accrue(S):
    """per-token harmony income, intensity-capped, cross-owner half-rent, cooldown-aware.
    Interpretation: income = sum over own tokens of min(harmony, intensity); a token with
    any same-field cross-owner neighbor earns half (diplomatic rent, both sides)."""
    b=S['board']; inc=[0,0]
    for c in range(64):
        if not b[c]: continue
        own=b[c]['owner']
        if S['cool'][c]>0: continue
        h=harmony_of(b,c); cap=LEX[b[c]['tok']]['i']
        base=min(h,cap)
        if base==0: continue
        cross=any(LEX[b[n]['tok']]['f']==LEX[b[c]['tok']]['f'] and b[n]['owner']!=own
                  for n in (c-8,c+8,c-1,c+1) if 0<=n<64 and b[n])
        inc[own]+= base//2 if cross else base
    for i in (0,1): S['bank'][i]+=inc[i]

def enclave_cells(center):
    r,c=divmod(center,8); out=[]
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if 0<=r+dr<8 and 0<=c+dc<8: out.append((r+dr)*8+c+dc)
    return out

def drift_immune(S,cell):
    p=S['board'][cell]
    if p['locked']: return True
    e=S['enclaves'][p['owner']]
    return e is not None and cell in enclave_cells(e)

def hunger_drift(S):
    """one drift event: slide the most HARMONIOUS eligible token; reset its harmony (cooldown)."""
    b=S['board']; best=None; bh=-1
    for c in range(64):
        if not b[c] or drift_immune(S,c): continue
        h=harmony_of(b,c)
        if h>bh or (h==bh and best is not None and pull(b,c,c+1 if c+1<64 and b[c+1] else c)>0):
            bh=h; best=c
    if best is None or bh==0: return None
    r,co=divmod(best,8); tgt=None; tp=-1
    for dr,dc in ((0,1),(0,-1),(1,0),(-1,0)):
        r2,c2=r+dr,co+dc
        if 0<=r2<8 and 0<=c2<8:
            n=r2*8+c2
            if b[n]:
                p=pull(b,best,n)
                if p>tp: tp=p; tgt=n
    if tgt is None: return None
    toward = 1 if b[tgt]['v']>b[best]['v'] else -1
    before=b[best]['v']
    b[best]['v']=max(-2,min(2,before+toward))
    S['cool'][best]=RESET_CD   # harmony reset
    S['driftCycles']+=1
    return (LEX[b[best]['tok']]['w'], before, b[best]['v'], bh, b[best]['owner'])

def used(S): return {c['tok'] for c in S['board'] if c}

def place_gain(S, me, cell, tok):
    before=S['players'][me]['score']
    S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
    recompute(S); after=S['players'][me]['score']
    S['board'][cell]=None; recompute(S)
    return after-before

def legal(S):
    return [(c,t) for c in range(64) if not S['board'][c] for t in LEX if t not in used(S)]

def greedy(S, me, deny=False):
    opp=1-me; cands=sorted(((place_gain(S,me,c,t),c,t) for c,t in legal(S)), key=lambda x:-x[0])
    top=cands[0][0]
    if deny:
        # deny: opponent's best square if their gain>=8 and our forgone<=3
        og=-99; oc=None
        for g,c,t in cands: pass
        for c in range(64):
            if S['board'][c]: continue
            for t in LEX:
                if t in used(S): continue
                g=place_gain(S,opp,c,t)
                if g>og: og=g; oc=c
        if og>=8 and oc is not None:
            alt=max((place_gain(S,me,oc,t) for t in LEX if t not in used(S)), default=-99)
            if top-alt<=3:
                bt=max(LEX,key=lambda t: place_gain(S,me,oc,t))
                return oc,bt,{'denied':og}
    pool=[c for c in cands if c[0]==top]
    best=None; bd=-1
    for g,c,t in pool:
        S['board'][c]={"tok":t,"owner":me,"locked":False,"attuned":False,"v":LEX[t]['v']}
        recompute(S); d=S['drift']
        S['board'][c]=None; recompute(S)
        if d>bd: bd=d; best=(c,t)
    return best[0],best[1],{}

def harmony_seeker(S, me):
    """v0.3 strategy: place to maximize own harmony income next accrual (within 60% of best standing gain)."""
    cands=sorted(((place_gain(S,me,c,t),c,t) for c,t in legal(S)), key=lambda x:-x[0])
    pool=[c for c in cands if c[0]>=0]
    if not pool: pool=cands[:3]
    best=None; bh=-1; bg=-10**9
    for g,c,t in pool:
        S['board'][c]={"tok":t,"owner":me,"locked":False,"attuned":False,"v":LEX[t]['v']}
        h=0
        for cc in range(64):
            if S['board'][cc] and S['board'][cc]['owner']==me and S['cool'][cc]==0:
                hh=harmony_of(S['board'],cc); h+=min(hh,LEX[S['board'][cc]['tok']]['i'])
        S['board'][c]=None; recompute(S)
        if h>bh or (h==bh and g>bg): bh=h; bg=g; best=(c,t)
    return best[0],best[1],{'harmony_next':bh}

def attuner(S, me):
    for cell,c in enumerate(S['board']):
        if c and c['owner']==me and not c['attuned'] and harmony_of(S['board'],cell)>=2:
            c['attuned']=True; c['locked']=True; S['enclaves'][me]=cell; S['spent'][me]+=2
            return None,None,{'attuned':LEX[c['tok']]['w']}
    return greedy(S, me, deny=True)[0:2]+({'attune_skip':1},)

def end_turn(S):
    for c in range(64):
        if S['cool'][c]>0: S['cool'][c]-=1
    accrue(S)
    recompute(S)
    evs=[]
    if S['drift']>=THRESH:
        n=1+total_harmony(S['board'])//FREQ_K
        for _ in range(n):
            e=hunger_drift(S)
            if e: evs.append(e)
    if evs: recompute(S)
    return evs

def play(p1_style, p2_style, n1="P1", n2="P2"):
    S=fresh(n1,n2)
    while S['turn']<MAXT:
        me=S['turn']%2; style=p1_style if me==0 else p2_style
        if style=='blitz': c,t,info=greedy(S,me)
        elif style=='deny': c,t,info=greedy(S,me,deny=True)
        elif style=='harmony': c,t,info=harmony_seeker(S,me)
        elif style=='fortress': c,t,info=attuner(S,me)
        else: c,t,info=greedy(S,me)
        if c is not None:
            S['board'][c]={"tok":t,"owner":me,"locked":False,"attuned":False,"v":LEX[t]['v']}
            S['players'][me]['placed']+=1
        evs=end_turn(S)
        S['turn']+=1
        w=[p for p in S['players'] if p['score']>=WIN]
        if w: S['winner']=w[0]['name']; break
    else:
        S['winner']=max(S['players'],key=lambda p:p['score'])['name']
    S['final']=tuple(p['score'] for p in S['players'])
    return S

def mirror_bias(games=40):
    """seat bias check with finish-the-round: alternate who starts; report P1/P2 win rates."""
    p1w=p2w=0; tot_ev=0
    for g in range(games):
        first='deny' if g%2==0 else 'blitz'
        S=play(first,'blitz')
        tot_ev+=S['driftCycles']
        if S['winner']=="P1": p1w+=1
        else: p2w+=1
    return p1w,p2w,tot_ev

if __name__=="__main__":
    print("=== v0.3 battery: anti-blitz candidates vs blitz (threshold 0.50, hunger-drift) ===")
    sched=[('deny','blitz'),('blitz','deny'),('harmony','blitz'),('blitz','harmony'),
           ('fortress','blitz'),('blitz','fortress'),('deny','harmony'),('harmony','deny')]
    for a,b in sched:
        S=play(a,b,a,b)
        print(f"{a:9s} vs {b:9s} | {S['winner']:8s} {S['final'][0]}-{S['final'][1]} | plies {S['turn']:2d} | driftEv {S['driftCycles']}")
    print("=== seat bias (deny vs blitz, alternating start, 40 games) ===")
    p1w,p2w,ev=mirror_bias()
    print(f"P1 wins {p1w}/40, P2 wins {p2w}/40, total drift events {ev}")
    print("DONE")
