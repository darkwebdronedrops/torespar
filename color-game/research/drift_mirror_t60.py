#!/usr/bin/env python3
"""DRIFT mirror-match harness: anti-blitz candidates vs pure greedy blitz.
Engine-faithful: LEX parsed from the live engine; meaning/pull/recompute/driftCheck
ported line-for-line from color-game/index.html (v0.2 + S.spent + enclaveHum patches)."""
import json, re, random
from decimal import Decimal, ROUND_HALF_UP

html = open('/root/.openclaw/workspace/creative/projects/color-game/index.html').read()
rows = re.findall(r'\["(\w+)","(\w+)",(-?\d),(\d)\]', html)
LEX = {i: {'w': w, 'f': f, 'v': int(v)} for i, (w, f, v, _) in enumerate(rows)}
W2ID = {d['w']: i for i, d in LEX.items()}
SHARP = {frozenset(['CHAOS','ORDER']), frozenset(['EROS','GRIEF'])}
RICH = {frozenset(['LIFE','GRIEF']), frozenset(['NUMERAL','EROS']), frozenset(['LIFE','CHAOS']),
         frozenset(['ORDER','EROS']), frozenset(['GRIEF','NUMERAL']), frozenset(['ORDER','GRIEF'])}
RES = {frozenset(['Garden','Harvest']), frozenset(['Oath','Verdict']), frozenset(['Sum','Zero']),
        frozenset(['Dirge','Hollow']), frozenset(['Heat','Sweat']), frozenset(['Storm','Flood'])}
WIN, MAXT = 60, 24
random.seed(42)

def fresh(nameA, nameB):
    return {"turn":0,"driftCycles":0,"drift":0.0,"winScore":WIN,"maxTurns":MAXT,
            "players":[{"name":nameA,"hue":185,"score":0,"placed":0},
                       {"name":nameB,"hue":345,"score":0,"placed":0}],
            "enclaves":[None,None],"spent":[0,0],
            "board":[None]*64,"log":[],"winner":None}

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

def enclave_cells(center):
    r,c=divmod(center,8); out=[]
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            r2,c2=r+dr,c+dc
            if 0<=r2<8 and 0<=c2<8: out.append(r2*8+c2)
    return out

def enclave_hum(b,S,a,bb):
    A,B=b[a],b[bb]; la,lb=LEX[A['tok']],LEX[B['tok']]
    if A['attuned'] or B['attuned']: return 0
    if la['f']!=lb['f']: return 0
    for e in S['enclaves']:
        if e is None: continue
        cells=enclave_cells(e)
        if a in cells and bb in cells: return 2
    return 0

def pull(b,a,bb):
    return 4-min(4,abs(b[a]['v']-b[bb]['v']))

def recompute(S):
    b=S['board']
    for p in S['players']: p['score']=0
    for a,bb in adj(b):
        m=meaning(b,a,bb)
        if m==0: m=enclave_hum(b,S,a,bb)
        if m==0: continue
        oa,ob=b[a]['owner'],b[bb]['owner']
        if oa==ob: S['players'][oa]['score']+=m
        else:
            S['players'][oa]['score']+=m//2; S['players'][ob]['score']+=m//2
    for i,p in enumerate(S['players']):
        p['score']-=S['spent'][i]
    ps=adj(b)
    S['drift']= round(sum(pull(b,a,bb) for a,bb in ps)/(4*len(ps)),4) if ps else 0

def drift_immune(S,cell):
    p=S['board'][cell]
    if p['locked']: return True
    e=S['enclaves'][p['owner']]
    return e is not None and cell in enclave_cells(e)

def drift_check(S):
    if S['drift']<0.60 or not adj(S['board']): return None
    best=None; bp=-1; b=S['board']
    for a,bb in adj(b):
        for x in (a,bb):
            y=bb if x==a else a
            if drift_immune(S,x): continue
            if b[x]['v']==b[y]['v']: continue
            p=pull(b,x,y)
            if p>bp: bp=p; best=x
    if best is None: return None
    br,bc=divmod(best,8); tgt=None; tp=-1
    for dr,dc in ((0,1),(0,-1),(1,0),(-1,0)):
        r2,c2=br+dr,bc+dc
        if 0<=r2<8 and 0<=c2<8:
            n=r2*8+c2
            if b[n]:
                p=pull(b,best,n)
                if p>tp: tp=p; tgt=n
    if tgt is None: return None
    toward = 1 if b[tgt]['v']>b[best]['v'] else -1
    before=b[best]['v']
    b[best]['v']=max(-2,min(2,before+toward))
    S['driftCycles']+=1
    return (LEX[b[best]['tok']]['w'], before, b[best]['v'], LEX[b[tgt]['tok']]['w'])

def used_tokens(S):
    return {c['tok'] for c in S['board'] if c}

def place_gain(S, me, cell, tok):
    """score delta for `me` if tok placed at cell (delta vs current)."""
    before=S['players'][me]['score']
    S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
    recompute(S)
    after=S['players'][me]['score']
    S['board'][cell]=None
    recompute(S)
    return after-before

def best_gain(S, me):
    """opponent's best immediate gain this turn (for denial math)."""
    g=-99; best=None
    for cell in range(64):
        if S['board'][cell]: continue
        for tok,d in LEX.items():
            if tok in used_tokens(S): continue
            gain=place_gain(S,me,cell,tok)
            if gain>g: g=gain; best=(cell,tok)
    return g,best

def legal_places(S):
    out=[]
    for cell in range(64):
        if S['board'][cell]: continue
        for tok,d in LEX.items():
            if tok in used_tokens(S): continue
            out.append((cell,tok))
    return out

def blitz_move(S, me):
    """pure greedy: max own immediate gain; tie-break toward higher resulting drift."""
    cands=[]
    for cell,tok in legal_places(S):
        gain=place_gain(S,me,cell,tok)
        cands.append((gain,cell,tok))
    cands.sort(key=lambda x:-x[0])
    top=cands[0][0]
    pool=[c for c in cands if c[0]==top]
    # tie-break: resulting global drift
    best=None; bd=-1
    for gain,cell,tok in pool:
        S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
        recompute(S); d=S['drift']
        S['board'][cell]=None; recompute(S)
        if d>bd: bd=d; best=(cell,tok)
    return best

def anti_move(S, me, style, hist):
    opp=1-me
    cands=[]
    for cell,tok in legal_places(S):
        gain=place_gain(S,me,cell,tok)
        cands.append((gain,cell,tok))
    cands.sort(key=lambda x:-x[0])
    top=cands[0][0]
    def commit(cell,tok):
        S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
        S['players'][me]['placed']+=1
    if style=='control':
        commit(*cands[0][1:]); return {'style':'control'}
    if style=='block':
        # deny: opponent's convergence square if their best gain >= 8 and our cost <= 3
        ogain, (ocell, otok) = best_gain(S, opp)
        if ogain>=8 and not S['board'][ocell]:
            my_here = place_gain(S,me,ocell, otok if otok not in used_tokens(S) else None) if False else None
            # cost = best gain forgone by taking ocell with our best word there
            alt = max((place_gain(S,me,ocell,t) for t in LEX if t not in used_tokens(S)), default=-99)
            forgone = top - alt
            if forgone<=3:
                best_tok = max(LEX, key=lambda t: place_gain(S,me,ocell,t))
                commit(ocell, best_tok); return {'style':'block','denied':ogain,'forgone':forgone}
        commit(*cands[0][1:]); return {'style':'block','denied':0}
    if style=='seeder':
        # pick highest-drift placement within 70% of best gain
        thresh = top*0.7
        pool=[c for c in cands if c[0]>=thresh]
        best=None; bd=-1
        for gain,cell,tok in pool:
            S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
            recompute(S); d=S['drift']
            S['board'][cell]=None; recompute(S)
            if d>bd: bd=d; best=(cell,tok)
        commit(*best); return {'style':'seeder','gain':place_gain(S,me,*best),'drift_after':bd}
    if style=='fortress':
        # if we have a token scoring 0 with >=2 same-field neighbors, attune it (cost −2 real)
        for cell,c in enumerate(S['board']):
            if c and c['owner']==me and not c['attuned']:
                ns=[n for n in (cell-8,cell+8,cell-1,cell+1) if 0<=n<64 and S['board'][n]
                    and LEX[S['board'][n]['tok']]['f']==LEX[c['tok']]['f']]
                if len(ns)>=2:
                    c['attuned']=True; c['locked']=True
                    S['enclaves'][me]=cell; S['spent'][me]+=2
                    recompute(S)
                    return {'style':'fortress','attuned':LEX[c['tok']]['w']}
        commit(*cands[0][1:]); return {'style':'fortress','attuned':None}
    if style=='disrupt':
        # every 3rd placement: if a MOVE breaks an opponent sole-pair worth >=6, do it
        if S['players'][me]['placed']%3==2:
            b=S['board']
            for cell,c in enumerate(b):
                if c and c['owner']==me:
                    for n in (cell-8,cell+8,cell-1,cell+1):
                        if 0<=n<64 and b[n] is None:
                            victim=None; saved=0
                            before=S['players'][opp]['score']
                            b[n]=c; b[cell]=None
                            recompute(S); after=S['players'][opp]['score']
                            b[cell]=c; b[n]=None; recompute(S)
                            if before-after>=6:
                                b[n]=c; b[cell]=None; recompute(S)
                                return {'style':'disrupt','broke':before-after}
        commit(*cands[0][1:]); return {'style':'disrupt'}
    if style=='hybrid':
        # block if cheap, else seed
        ogain,(ocell,otok)=best_gain(S,opp)
        if ogain>=10 and not S['board'][ocell]:
            alt=max((place_gain(S,me,ocell,t) for t in LEX if t not in used_tokens(S)), default=-99)
            if top-alt<=2:
                best_tok=max(LEX,key=lambda t: place_gain(S,me,ocell,t))
                commit(ocell,best_tok); return {'style':'hybrid-block','denied':ogain}
        return anti_move(S,me,'seeder',hist)
    commit(*cands[0][1:]); return {'style':style}

def play_game(style, anti_first, names=("Anti","Blitz")):
    S=fresh(names[0] if anti_first else names[1], names[1] if anti_first else names[0])
    # seats: index 0 = first mover
    S['log'].append({"t":"sys","m":f"Mirror game: {style} ({'first' if anti_first else 'second'}) vs blitz."})
    actions=[]; maxdrift=0.0
    while S['turn']<S['maxTurns']:
        me=S['turn']%2
        is_anti = (me==0)==anti_first
        if is_anti:
            info=anti_move(S,me,style,actions)
        else:
            cell,tok=blitz_move(S,me); info={'style':'blitz','word':LEX[tok]['w']}
            S['board'][cell]={"tok":tok,"owner":me,"locked":False,"attuned":False,"v":LEX[tok]['v']}
            S['players'][me]['placed']+=1
        recompute(S)
        ev=drift_check(S)
        if ev: recompute(S)
        maxdrift=max(maxdrift,S['drift'])
        actions.append({'turn':S['turn'],'by':S['players'][me]['name'],'info':info,'drift':S['drift'],'ev':ev})
        S['turn']+=1
        w=[p for p in S['players'] if p['score']>=S['winScore']]
        if w:
            S['winner']=w[0]['name']; break
    else:
        S['winner']=max(S['players'],key=lambda p:p['score'])['name']
    return S,actions,maxdrift

results=[]
schedule=[('block',True),('block',False),('seeder',True),('seeder',False),
          ('fortress',True),('disrupt',False),('control',True),('hybrid',False)]
for style,first in schedule:
    S,acts,md=play_game(style,first)
    anti_name=S['players'][0]['name']
    anti_score=S['players'][0]['score']; blitz_score=S['players'][1]['score']
    anti_won = S['winner']==anti_name
    results.append({'style':style,'anti_first':first,'winner':S['winner'],
        'anti':anti_score,'blitz':blitz_score,'plies':S['turn'],
        'driftEvents':S['driftCycles'],'maxDrift':md,
        'notes':[a['info'] for a in acts if a['info'].get('style')!='blitz' and len(str(a['info']))>10][:6]})
    print(f"{style:9s} anti-{'1st' if first else '2nd'} | {S['winner']:5s} {anti_score}-{blitz_score} | plies {S['turn']:2d} | driftEv {S['driftCycles']} | maxDrift {md:.3f}")
json.dump(results,open('/tmp/drift_mirror_results_t60.json','w'),indent=1)
print("DONE")
