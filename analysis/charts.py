import json, html
M=json.load(open('/home/user/ai-max-analysis/data/metrics.json'))
A=M['accounts']; T=M['total']
ORDER=['Ortho Excellence','Holt Orthodontics','South Florida','Sabinsky','Goodman Ortho']
CATS=['Highly Relevant','Relevant / Acceptable','Borderline / Low Intent','Irrelevant','Clearly Wasteful']
CVAR=['var(--r1)','var(--r2)','var(--r3)','var(--r4)','var(--r5)']
SHORT={'Highly Relevant':'Highly rel.','Relevant / Acceptable':'Relevant','Borderline / Low Intent':'Borderline','Irrelevant':'Irrelevant','Clearly Wasteful':'Wasteful'}
e=html.escape
def money(v): return '—' if v is None else f'${v:,.0f}' if abs(v)>=100 else f'${v:,.2f}'
def m0(v): return '—' if v is None else f'${v:,.0f}'

def legend(items):
    return '<div class="legend">'+''.join(f'<span><i style="background:{c}"></i>{e(l)}</span>' for l,c in items)+'</div>'

def stacked(rows, W=980, rh=38, lw=176, title_vals=True):
    """rows: [(label, [(catname, pct, absval)], sublabel)]"""
    H=len(rows)*rh+26
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" width="{W}" style="width:100%;height:auto">']
    bw=W-lw-56
    for i,(lab,segs,sub) in enumerate(rows):
        y=i*rh+4; bh=19
        s.append(f'<text class="lbl" x="0" y="{y+13}" font-size="12.5" font-weight="600" fill="var(--ink)">{e(lab)}</text>')
        if sub: s.append(f'<text x="0" y="{min(y+26,y+rh-4)}" font-size="9.5" fill="var(--ink-3)">{e(sub)}</text>')
        if lab.startswith('ALL') and i>0 and not rows[i-1][0].startswith('ALL'):
            s.append(f'<line x1="0" x2="{W}" y1="{y-4}" y2="{y-4}" stroke="var(--rule-2)" stroke-width="1"/>')
        x=lw
        for j,(cat,pct,val) in enumerate(segs):
            w=bw*pct/100
            if w<=0: continue
            ww=max(w-2,0.8)
            s.append(f'<rect class="seg" x="{x:.1f}" y="{y+2}" width="{ww:.1f}" height="{bh}" fill="{CVAR[CATS.index(cat)]}" rx="1.5" '
                     f'data-tip="{e(cat)} — {pct:.1f}% · {val}"><title>{e(cat)}: {pct:.1f}% ({e(str(val))})</title></rect>')
            if w>44 and title_vals:
                fill=f'var(--on{j+1})'
                s.append(f'<text x="{x+ww/2:.1f}" y="{y+16}" font-size="10.5" font-weight="600" text-anchor="middle" fill="{fill}">{pct:.0f}%</text>')
            x+=w
    s.append('</svg>')
    return ''.join(s)

def hbars(items, W=470, rh=34, lw=150, fmt=lambda v:f'{v}', color='var(--aim)', maxv=None):
    mx=maxv or max([v for _,v,_ in items]+[1e-9])
    H=len(items)*rh+8
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" width="{W}" style="width:100%;height:auto">']
    bw=W-lw-62
    for i,(lab,v,col) in enumerate(items):
        y=i*rh+4; w=max(bw*v/mx,1.2)
        s.append(f'<text class="lbl" x="0" y="{y+17}" font-size="11.5" fill="var(--ink-2)">{e(lab)}</text>')
        s.append(f'<rect class="bar-anim" x="{lw}" y="{y+5}" width="{w:.1f}" height="16" rx="2" fill="{col or color}"/>')
        s.append(f'<text x="{lw+w+7:.1f}" y="{y+17}" font-size="11.5" font-weight="600" fill="var(--ink)">{e(fmt(v))}</text>')
    s.append('</svg>')
    return ''.join(s)

def grouped(labels, sA, sB, fmt, W=980, gh=190, lA='AI Max', lB='Standard'):
    """vertical grouped bars, single scale"""
    mx=max(max(sA),max(sB),1e-9)*1.18
    n=len(labels); pad=54; bw=(W-pad-14)/n
    s=[f'<svg viewBox="0 0 {W} {gh+46}" role="img" width="{W}" style="width:100%;height:auto">']
    for k in range(5):
        y=gh-gh*k/4
        s.append(f'<line x1="{pad}" x2="{W-6}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--grid)" stroke-width="1"/>')
        s.append(f'<text x="{pad-8}" y="{y+3.5:.1f}" font-size="9.5" text-anchor="end" fill="var(--ink-3)">{fmt(mx*k/4)}</text>')
    for i,lb in enumerate(labels):
        cx=pad+bw*i+bw/2; w=min(bw*0.29,44)
        for j,(v,c) in enumerate([(sA[i],'var(--aim)'),(sB[i],'var(--std)')]):
            h=max(gh*v/mx,1.2); x=cx-w-1+j*(w+2)
            s.append(f'<rect x="{x:.1f}" y="{gh-h:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" fill="{c}" '
                     f'data-tip="{e(lb)} · {(lA if j==0 else lB)}: {e(fmt(v))}"><title>{e(lb)} {(lA if j==0 else lB)}: {e(fmt(v))}</title></rect>')
            s.append(f'<text x="{x+w/2:.1f}" y="{gh-h-5:.1f}" font-size="9.5" font-weight="600" text-anchor="middle" fill="var(--ink-2)">{e(fmt(v))}</text>')
        for k,part in enumerate(lb.split('|')):
            s.append(f'<text class="lbl" x="{cx:.1f}" y="{gh+16+k*12:.1f}" font-size="10.5" text-anchor="middle" fill="var(--ink-2)">{e(part)}</text>')
    s.append(f'<line x1="{pad}" x2="{W-6}" y1="{gh}" y2="{gh}" stroke="var(--axis)" stroke-width="1.5"/></svg>')
    return ''.join(s)

