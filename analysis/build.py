from charts import *

VERDICT={
 'Ortho Excellence':('res','Restrict hard','AI Max absorbed 73.5% of account spend and pushed an orthodontic practice into general dentistry: only 8.3% of its terms are orthodontically relevant, and 6 of its 7 conversions came from general-dental or competitor-practice searches, not orthodontic ones.'),
 'Holt Orthodontics':('res','Restrict','The largest absolute waste in the set — $500 on irrelevant/wasteful terms, including $297 on 205 bare street-address lookups. CPA is 48% worse than keyword traffic, and 2 of its 5.6 conversions came from clearly wasteful queries.'),
 'South Florida':('mon','Keep + monitor','The one account where AI Max expansion lands on-service: 79.5% relevant, 5.0% irrelevant, and only 10.2% of spend on bad terms. CPA is 27% worse than keyword traffic, but this is a general dental practice, so AI Max’s pull toward "dentist" queries is a feature, not a defect.'),
 'Sabinsky':('mon','Restrict / monitor','Zero conversions from AI Max on $95.83 and 10 clicks. That is a real red flag but not yet a verdict — 10 clicks cannot prove failure. Relevance is mediocre (44.2%) and CTR is a third of keyword traffic.'),
 'Goodman Ortho':('mon','Monitor','The cleanest AI Max profile (78.8% relevant, 2.3% irrelevant spend) and the only account where AI Max beat keyword CPA. But at $112 and 13 clicks the sample is far too small to act on in either direction.'),
}
def acct_block(name):
    a=A[name]; am=a['aimax']; st=a['std']; vc,vt,vw=VERDICT[name]
    segs=[(c,am['cats'][c]/am['terms']*100,f"{am['cats'][c]} terms · {money(am['catCost'][c])}") for c in CATS]
    segs_sp=[(c,(am['catCost'][c]/am['cost']*100 if am['cost'] else 0),money(am['catCost'][c])) for c in CATS]
    rows=[('Share of AI Max terms',segs,f"{am['terms']:,} terms"),('Share of AI Max spend',segs_sp,money(am['cost']))]
    mt=[('AI Max search terms',f"{am['terms']:,}",f"{a['termShare']}% of all terms"),
        ('Relevant (highly + acceptable)',f"{am['relPct']}%",f"vs {st['relPct']}% on keyword traffic"),
        ('Borderline / low intent',f"{am['borPct']}%",''),
        ('Irrelevant + clearly wasteful',f"{am['irrPct']}%",f"vs {st['irrPct']}% on keyword traffic"),
        ('Already excluded',f"{am['exclPct']}%",f"{am['excl']} of {am['terms']:,} terms"),
        ('AI Max spend',money(am['cost']),f"{a['spendShare']}% of account search spend"),
        ('AI Max clicks',f"{am['clicks']:,}",f"CTR {am['ctr']}% · CPC {money(am['cpc'])}"),
        ('AI Max conversions',f"{am['conv']:g}",f"{a['convShare']}% of account conversions"),
        ('AI Max CPA',m0(am['cpa']),f"vs {m0(st['cpa'])} on keyword traffic"),
        ('Spend on irrelevant/wasteful',money(am['irrSpend']),f"{am['irrSpendPct']}% of AI Max spend"),
        ('Bad terms still not excluded',f"{am['badActive']}",f"{money(am['badActiveSpend'])} already spent"),
        ('AI Max spend with zero conversions',money(am['zeroConvSpend']),f"{am['zeroConvPct']}% of AI Max spend")]
    mrows=''.join(f'<tr><td>{e(k)}</td><td><b>{e(v)}</b></td><td style="color:var(--ink-3);font-size:12px">{e(s)}</td></tr>' for k,v,s in mt)
    if a['convTerms']:
        crows=''.join(f'<tr><td class="term">{e(c["term"])}</td><td style="text-align:left"><span style="color:{CVAR[CATS.index(c["cat"])]};font-weight:600">●</span> {e(SHORT[c["cat"]])}</td>'
                      f'<td>{c["clicks"]}</td><td>{money(c["cost"])}</td><td><b>{c["conv"]:g}</b></td>'
                      f'<td style="text-align:left;font-size:11.5px;color:var(--ink-3)">{"excluded since" if c["excl"]=="Excluded" else "still active"}</td></tr>' for c in a['convTerms'])
        conv=f'''<div class="tw"><table><thead><tr><th>Converting AI Max search term</th><th style="text-align:left">Relevance</th><th>Clicks</th><th>Cost</th><th>Conv.</th><th style="text-align:left">Status</th></tr></thead><tbody>{crows}</tbody></table></div>'''
    else:
        conv='<div class="note crit"><h4>Zero AI Max conversions</h4><p>Not one of this account’s 285 AI Max search terms produced a conversion across the 30-day window. 10 clicks and $95.83 were spent with no lead. Sample size is small enough that this is a warning signal, not proof of failure.</p></div>'
    top=''.join(f'<tr><td class="term">{e(t["term"])}</td><td style="text-align:left"><span style="color:{CVAR[CATS.index(t["cat"])]};font-weight:600">●</span> {e(SHORT[t["cat"]])}</td>'
                f'<td>{t["clicks"]}</td><td>{money(t["cost"])}</td><td>{t["conv"]:g}</td></tr>' for t in a['topSpend'])
    return f'''
<article class="acct">
 <header>
  <div class="who"><h3>{e(name)}</h3><div class="ctx">{e(a['context'])}</div></div>
  <span class="chip {vc}"><i></i>{e(vt)}</span>
 </header>
 <div class="body">
  <div>{legend([(SHORT[c],CVAR[i]) for i,c in enumerate(CATS)])}<div class="chart-scroll">{stacked(rows,W=940,lw=168)}</div></div>
  <div class="two">
   <div><h4>AI Max scorecard</h4><div class="tw"><table class="sc"><tbody>{mrows}</tbody></table></div></div>
   <div><h4>Top AI Max spend</h4><div class="tw"><table><thead><tr><th>Search term</th><th style="text-align:left">Relevance</th><th>Clk</th><th>Cost</th><th>Conv</th></tr></thead><tbody>{top}</tbody></table></div></div>
  </div>
  <div><h4>Did AI Max convert?</h4>{conv}</div>
  <div class="verdict-line {vc}"><b>Verdict — {e(vt)}.</b> {vw}</div>
 </div>
</article>'''

am,st=T['aimax'],T['std']
tot_cost=am['cost']+st['cost']; tot_conv=am['conv']+st['conv']
CE=M['catEfficiency']
def cpa(d): return d['cost']/d['conv'] if d['conv'] else None

# ---- cross-account matrix ----
xrows=''
for n in ORDER:
    a=A[n]; x=a['aimax']; s=a['std']; vc,vt,_=VERDICT[n]
    xrows+=(f'<tr><td><b>{e(n)}</b></td><td>{x["relPct"]}%</td><td>{x["borPct"]}%</td><td>{x["irrPct"]}%</td>'
            f'<td>{x["exclPct"]}%</td><td>{money(x["cost"])}</td><td>{x["conv"]:g}</td><td>{m0(x["cpa"])}</td>'
            f'<td style="color:var(--ink-3)">{m0(s["cpa"])}</td><td style="text-align:left"><span class="chip {vc}"><i></i>{e(vt)}</span></td></tr>')
xfoot=(f'<tr><td>All five accounts</td><td>{am["relPct"]}%</td><td>{am["borPct"]}%</td><td>{am["irrPct"]}%</td>'
       f'<td>{am["exclPct"]}%</td><td>{money(am["cost"])}</td><td>{am["conv"]:g}</td><td>{m0(am["cpa"])}</td>'
       f'<td>{m0(st["cpa"])}</td><td style="text-align:left">Restrict</td></tr>')

# ---- charts ----
rel_rows=[]
for n in ORDER:
    x=A[n]['aimax']
    rel_rows.append((n,[(c,x['cats'][c]/x['terms']*100,f"{x['cats'][c]} terms") for c in CATS],f"{x['terms']:,} AI Max terms"))
rel_rows.append(('ALL AI MAX',[(c,am['cats'][c]/am['terms']*100,f"{am['cats'][c]} terms") for c in CATS],f"{am['terms']:,} terms"))
rel_rows.append(('ALL KEYWORD-MATCHED',[(c,st['cats'][c]/st['terms']*100,f"{st['cats'][c]} terms") for c in CATS],f"{st['terms']:,} terms · the benchmark"))
chart_rel=stacked(rel_rows)

spend_rows=[]
for n in ORDER:
    x=A[n]['aimax']
    spend_rows.append((n,[(c,(x['catCost'][c]/x['cost']*100 if x['cost'] else 0),money(x['catCost'][c])) for c in CATS],money(x['cost'])+' AI Max spend'))
spend_rows.append(('ALL AI MAX',[(c,am['catCost'][c]/am['cost']*100,money(am['catCost'][c])) for c in CATS],money(am['cost'])))
spend_rows.append(('ALL KEYWORD-MATCHED',[(c,st['catCost'][c]/st['cost']*100,money(st['catCost'][c])) for c in CATS],money(st['cost'])+' · the benchmark'))
chart_spend=stacked(spend_rows)

chart_cpa=grouped([n.replace(' ','|',1) for n in ORDER]+['ALL|ACCOUNTS'],
    [A[n]['aimax']['cpa'] or 0 for n in ORDER]+[am['cpa']],
    [A[n]['std']['cpa'] or 0 for n in ORDER]+[st['cpa']], lambda v:f'${v:,.0f}')
chart_cvr=grouped([n.replace(' ','|',1) for n in ORDER]+['ALL|ACCOUNTS'],
    [A[n]['aimax']['cvr'] for n in ORDER]+[am['cvr']],
    [A[n]['std']['cvr'] for n in ORDER]+[st['cvr']], lambda v:f'{v:.1f}%', gh=150)
chart_irr=grouped([n.replace(' ','|',1) for n in ORDER]+['ALL|ACCOUNTS'],
    [A[n]['aimax']['irrSpendPct'] for n in ORDER]+[am['irrSpendPct']],
    [A[n]['std']['irrSpendPct'] for n in ORDER]+[st['irrSpendPct']], lambda v:f'{v:.0f}%', gh=150)
chart_excl=grouped([n.replace(' ','|',1) for n in ORDER]+['ALL|ACCOUNTS'],
    [A[n]['aimax']['exclPct'] for n in ORDER]+[am['exclPct']],
    [round(A[n]['aimax']['badActive']/A[n]['aimax']['terms']*100,1) for n in ORDER]+[round(am['badActive']/am['terms']*100,1)],
    lambda v:f'{v:.0f}%', gh=150, lA='Excluded', lB='Bad & still active')
chart_catcpa=hbars([(SHORT[c]+f"  ({CE[c]['conv']:g} conv)", CE[c]['cost']/CE[c]['conv'] if CE[c]['conv'] else 0, CVAR[i]) for i,c in enumerate(CATS)],
    W=470, lw=168, fmt=lambda v:f'${v:,.0f}' if v else 'no conv.')
chart_catspend=hbars([(SHORT[c], CE[c]['cost'], CVAR[i]) for i,c in enumerate(CATS)], W=470, lw=110, fmt=lambda v:f'${v:,.0f}')

LEG5=legend([(SHORT[c],CVAR[i]) for i,c in enumerate(CATS)])
LEG2=legend([('AI Max','var(--aim)'),('Keyword-matched (standard)','var(--std)')])
covrows=''.join(f'<tr><td>{e(n)}</td><td>{money(A[n]["coverage"]["visibleSpend"])}</td><td>{money(A[n]["coverage"]["totalSpend"])}</td>'
                f'<td><b>{A[n]["coverage"]["pct"]}%</b></td><td>{A[n]["coverage"]["visibleConv"]:g}</td>'
                f'<td>{A[n]["coverage"]["totalConv"]:g}</td><td><b>{A[n]["coverage"]["convPct"]}%</b></td></tr>' for n in ORDER)

BODY=f'''
<div class="wrap">
<header class="mast">
 <p class="eyebrow">Google Ads · Search terms forensic audit</p>
 <h1>Is AI Max helping or hurting?</h1>
 <p class="lede">Every AI Max search term across five orthodontic and dental accounts, classified by real patient intent and matched against what it cost and what it produced. The short answer: AI Max is buying competitors’ names and street addresses, and it is doing so at a 40% worse cost per lead.</p>
 <div class="meta">
  <span><b>Window</b> {e(M['dateRange'].split('(')[0].strip())}</span>
  <span><b>Accounts</b> 5</span>
  <span><b>Search terms analysed</b> {am['terms']+st['terms']:,}</span>
  <span><b>Spend analysed</b> {money(tot_cost)}</span>
  <span><b>Conversions</b> {tot_conv:g}</span>
 </div>
</header>

<section>
 <div class="shead"><div class="n">Before the numbers</div><div><h2>Three limits on this data</h2></div></div>
 <div class="note"><h4>1 · Google withholds 29–45% of the spend behind “Other search terms”</h4>
  <p>Named search terms account for only 55–71% of each account’s search spend. The rest sits in Google’s privacy-thresholded “Other search terms” bucket and <b>cannot be attributed to AI Max or to keyword matching</b>. Every figure in this report describes the visible portion. Holt is the weakest case: 45% of conversions are invisible.</p>
  <div class="tw" style="margin-top:12px"><table><thead><tr><th>Account</th><th>Named-term spend</th><th>Total search spend</th><th>Visible</th><th>Named conv.</th><th>Total conv.</th><th>Visible</th></tr></thead><tbody>{covrows}</tbody></table></div></div>
 <div class="note"><h4>2 · No conversion values or conversion-action names in the export</h4>
  <p>The reports carry a single blended <span class="mono">Conversions</span> column with no value and no action breakdown, so <b>primary conversions (booked consults, calls) cannot be separated from secondary ones</b> (form starts, clicks-to-call, page events). Holt’s fractional counts (0.64, 5.64) confirm several actions are being counted together. Treat every “conversion” below as a lead signal of unknown quality — which matters, because AI Max’s converting terms look lower-quality than its counts suggest.</p></div>
 <div class="note"><h4>3 · One 30-day window, and only 267 AI Max clicks in total</h4>
  <p>All five files cover the identical window ({e(M['dateRange'].split('(')[0].strip())}), so cross-account comparison is fair. But 267 AI Max clicks and {am['conv']:g} conversions is <b>thin for efficiency conclusions and ample for relevance conclusions</b>. The relevance findings rest on {am['terms']:,} classified terms and are robust. The per-account CPA rankings rest on 0–7 conversions each and are not. Goodman ($112, 13 clicks) and Sabinsky ($96, 10 clicks) are too small to judge on performance at all.</p></div>
</section>

<section>
 <div class="shead"><div class="n">01</div><div><h2>The headline</h2></div></div>
 <div class="tiles">
  <div class="tile"><div class="k">AI Max share of search spend</div><div class="v">{am['cost']/tot_cost*100:.0f}%</div><div class="s">{money(am['cost'])} of {money(tot_cost)}</div></div>
  <div class="tile"><div class="k">AI Max share of conversions</div><div class="v">{am['conv']/tot_conv*100:.0f}%</div><div class="s">{am['conv']:g} of {tot_conv:g} — it buys more than it returns</div></div>
  <div class="tile"><div class="k">AI Max cost per conversion</div><div class="v bad">{m0(am['cpa'])}</div><div class="s">vs {m0(st['cpa'])} on keyword traffic — <b>{(am['cpa']/st['cpa']-1)*100:.0f}% worse</b></div></div>
  <div class="tile"><div class="k">AI Max terms that are relevant</div><div class="v bad">{am['relPct']:.0f}%</div><div class="s">vs {st['relPct']:.0f}% on keyword traffic</div></div>
  <div class="tile"><div class="k">AI Max spend on bad terms</div><div class="v bad">{money(am['irrSpend'])}</div><div class="s">{am['irrSpendPct']}% of AI Max spend, vs {st['irrSpendPct']}% on keyword traffic</div></div>
 </div>
 <p style="margin-top:24px">Three findings hold across every account, and they are what the rest of this report evidences:</p>
 <ul>
  <li><b>AI Max is a competitor-name and address engine, not a demand-discovery engine.</b> {am['namedSpendPct']}% of AI Max spend went to queries naming a specific practice, provider, or street address — versus {st['namedSpendPct']}% of keyword-matched spend. 249 terms were <em>bare street addresses</em> with no service word at all, costing {money(337.90)}.</li>
  <li><b>It expands toward general dentistry.</b> Across all five accounts the AI Max vocabulary is dominated by “dental” (957 uses) and “dentist” (388) against “orthodontist/orthodontics/braces/Invisalign” combined (574). For the four orthodontic practices that is off-service traffic. For South Florida — a general dental practice — it is exactly on-service, which is why that account scores 79.5% relevant while Ortho Excellence scores 8.3%.</li>
  <li><b>Relevance predicts efficiency.</b> AI Max terms we classified <em>Highly Relevant</em> converted at {m0(CE['Highly Relevant']['cost']/CE['Highly Relevant']['conv'])} — <b>better than the {m0(st['cpa'])} keyword benchmark</b>. Everything below that line converted at {m0(CE['Borderline / Low Intent']['cost']/CE['Borderline / Low Intent']['conv'])}–{m0(CE['Clearly Wasteful']['cost']/CE['Clearly Wasteful']['conv'])}. AI Max is not broken; it is unrestrained.</li>
 </ul>
</section>

<section>
 <div class="shead"><div class="n">02</div><div><h2>Search-term relevance</h2></div></div>
 <p>Every AI Max term was classified on <b>likely patient intent</b>, not keyword similarity — a search for a rival orthodontist’s name is in the right vertical but the wrong intent, and a bare street address is neither. The bottom two rows are the control: the same classifier applied to the keyword-matched traffic in the same accounts.</p>
 <figure class="fig">{LEG5}<div class="chart-scroll">{chart_rel}</div>
  <figcaption><b>Share of search terms by intent class.</b> Keyword-matched traffic is 81.4% relevant and 6.1% irrelevant. AI Max traffic is 41.3% relevant and 24.7% irrelevant — a four-fold increase in off-target terms. Ortho Excellence is the extreme case: 8.3% relevant.</figcaption></figure>
 <figure class="fig">{LEG5}<div class="chart-scroll">{chart_spend}</div>
  <figcaption><b>Share of AI Max spend by intent class</b> — the same picture weighted by money rather than term count. This is the chart that matters: 27.0% of AI Max spend ({money(am['irrSpend'])}) bought irrelevant or wasteful clicks, against 1.8% ({money(st['irrSpend'])}) on keyword traffic.</figcaption></figure>
 <div class="note"><h4>How terms were classified</h4>
  <p><b>Highly relevant</b> — the account’s core service plus local or commercial intent (“orthodontist near me”, “braces cost”, own brand). <b>Relevant / acceptable</b> — core service without a geo or buying modifier. <b>Borderline / low intent</b> — right vertical, wrong intent: competitor practice and provider names, general dentistry on an orthodontic account, insurance-network lookups. <b>Irrelevant</b> — a different dental specialty than the practice sells (oral surgery, endodontics, veneers, dentures on an ortho account). <b>Clearly wasteful</b> — bare addresses and phone numbers, non-dental medicine, out-of-market geography, mail-order aligner brands. Relevance is judged per account: “emergency dentist” is highly relevant for South Florida and irrelevant for Sabinsky.</p></div>
</section>

<section>
 <div class="shead"><div class="n">03</div><div><h2>AI Max vs. standard search traffic</h2></div></div>
 <p>Same accounts, same window, same conversion tracking — the only variable is whether Google matched the query to a keyword or generated it through AI Max.</p>
 <div class="tw" style="margin-bottom:20px"><table>
  <thead><tr><th>Metric</th><th>AI Max</th><th>Keyword-matched</th><th>Difference</th></tr></thead><tbody>
  <tr><td>Search terms</td><td>{am['terms']:,}</td><td>{st['terms']:,}</td><td style="color:var(--ink-3)">+{(am['terms']/st['terms']-1)*100:.0f}% more terms</td></tr>
  <tr><td>Impressions</td><td>{am['impr']:,}</td><td>{st['impr']:,}</td><td style="color:var(--ink-3)">−{(1-am['impr']/st['impr'])*100:.0f}%</td></tr>
  <tr><td>Clicks</td><td>{am['clicks']:,}</td><td>{st['clicks']:,}</td><td style="color:var(--ink-3)">−{(1-am['clicks']/st['clicks'])*100:.0f}%</td></tr>
  <tr><td>CTR</td><td>{am['ctr']}%</td><td>{st['ctr']}%</td><td style="color:var(--crit-ink)">−{(1-am['ctr']/st['ctr'])*100:.0f}%</td></tr>
  <tr><td>Avg. CPC</td><td>{money(am['cpc'])}</td><td>{money(st['cpc'])}</td><td style="color:var(--good-ink)">−{(1-am['cpc']/st['cpc'])*100:.0f}% (cheaper clicks)</td></tr>
  <tr><td>Cost</td><td>{money(am['cost'])}</td><td>{money(st['cost'])}</td><td style="color:var(--ink-3)">{am['cost']/tot_cost*100:.0f}% of spend</td></tr>
  <tr><td>Conversions</td><td>{am['conv']:g}</td><td>{st['conv']:g}</td><td style="color:var(--ink-3)">{am['conv']/tot_conv*100:.0f}% of conversions</td></tr>
  <tr><td>Conversion rate</td><td>{am['cvr']}%</td><td>{st['cvr']}%</td><td style="color:var(--crit-ink)">−{(1-am['cvr']/st['cvr'])*100:.0f}%</td></tr>
  <tr><td>Cost per conversion</td><td><b>{m0(am['cpa'])}</b></td><td><b>{m0(st['cpa'])}</b></td><td style="color:var(--crit-ink)"><b>+{(am['cpa']/st['cpa']-1)*100:.0f}% worse</b></td></tr>
  <tr><td>Relevant terms</td><td>{am['relPct']}%</td><td>{st['relPct']}%</td><td style="color:var(--crit-ink)">−{st['relPct']-am['relPct']:.1f} pts</td></tr>
  <tr><td>Irrelevant + wasteful terms</td><td>{am['irrPct']}%</td><td>{st['irrPct']}%</td><td style="color:var(--crit-ink)">{am['irrPct']/st['irrPct']:.1f}× more</td></tr>
  <tr><td>Spend on irrelevant terms</td><td>{money(am['irrSpend'])} ({am['irrSpendPct']}%)</td><td>{money(st['irrSpend'])} ({st['irrSpendPct']}%)</td><td style="color:var(--crit-ink)">{am['irrSpendPct']/st['irrSpendPct']:.0f}× more</td></tr>
  <tr><td>Named-entity spend (competitors, addresses)</td><td>{am['namedSpendPct']}%</td><td>{st['namedSpendPct']}%</td><td style="color:var(--crit-ink)">+{am['namedSpendPct']-st['namedSpendPct']:.1f} pts</td></tr>
  <tr><td>Spend producing zero conversions</td><td>{am['zeroConvPct']}%</td><td>{st['zeroConvPct']}%</td><td style="color:var(--crit-ink)">+{am['zeroConvPct']-st['zeroConvPct']:.1f} pts</td></tr>
  </tbody></table></div>
 <figure class="fig">{LEG2}<div class="chart-scroll">{chart_cpa}</div>
  <figcaption><b>Cost per conversion by account.</b> AI Max is more expensive per lead in four of five accounts. Goodman is the exception, and it rests on two conversions from a single search term — not a result to act on. Sabinsky has no AI Max bar because it produced no conversions.</figcaption></figure>
 <figure class="fig">{LEG2}<div class="chart-scroll">{chart_cvr}</div>
  <figcaption><b>Conversion rate by account.</b> AI Max converts worse everywhere except Goodman. The aggregate gap — {am['cvr']}% vs {st['cvr']}% — is the most reliable number here, because it pools all {am['clicks']+st['clicks']} clicks.</figcaption></figure>
 <figure class="fig"><div class="legend"><span><i style="background:var(--aim)"></i>AI Max</span><span><i style="background:var(--std)"></i>Keyword-matched</span></div><div class="chart-scroll">{chart_irr}</div>
  <figcaption><b>Percentage of spend on irrelevant or clearly wasteful search terms.</b> This is the cleanest separation in the dataset and does not depend on conversion counts at all — keyword traffic stays near zero in every account while AI Max ranges from 2% to 35%.</figcaption></figure>
</section>

<section>
 <div class="shead"><div class="n">04</div><div><h2>Where the money went — and what came back</h2></div></div>
 <div class="two">
  <figure class="fig"><h4>AI Max spend by intent class</h4><div class="chart-scroll">{chart_catspend}</div>
   <figcaption>Only {money(CE['Highly Relevant']['cost'])} of {money(am['cost'])} — {CE['Highly Relevant']['cost']/am['cost']*100:.0f}% — went to unambiguously on-target searches.</figcaption></figure>
  <figure class="fig"><h4>AI Max cost per conversion by intent class</h4><div class="chart-scroll">{chart_catcpa}</div>
   <figcaption>Highly relevant AI Max traffic beats the {m0(st['cpa'])} keyword benchmark. Everything else is 1.2–2.1× worse.</figcaption></figure>
 </div>
 <div class="note crit" style="margin-top:20px"><h4>The conversions AI Max did produce are not all real orthodontic leads</h4>
  <p>Of the {am['conv']:g} AI Max conversions across all five accounts, only <b>{CE['Highly Relevant']['conv']:g} came from highly relevant searches</b>. The rest include a Sacramento hospital lookup (<span class="mono">sutter health hospital sacramento</span>, $23.61), a bare street address (<span class="mono">140 roseville pkwy suite 150…</span>, $28.20), and — at Ortho Excellence — six conversions from general-dentistry and competitor-dental searches (<span class="mono">dentist tacoma</span>, <span class="mono">rewards dental tacoma</span>, <span class="mono">dental clinic near me</span>) on an account that sells orthodontics. An irrelevant term that converts is still worth investigating rather than keeping: with no conversion-action data we cannot tell whether these are booked consults or form abandons, and a “dentist near me” lead at an orthodontic practice is very likely unqualified.</p>
  <p style="margin-top:10px"><b>Incrementality:</b> we checked every converting AI Max term against the vocabulary its own account already reached through keywords. Six of the 17 contained <em>no</em> word the account wasn’t already matching — they are duplicated intent, not discovery. Of the rest, the “new” vocabulary is almost entirely proper nouns: <span class="mono">caring</span>, <span class="mono">tree</span>, <span class="mono">sutter</span>, <span class="mono">ossman</span>, <span class="mono">ngo</span>. AI Max found new <em>names</em>, not new <em>demand</em>.</p></div>
</section>

<section>
 <div class="shead"><div class="n">05</div><div><h2>Exclusion coverage — is anyone guarding the gate?</h2></div></div>
 <p>Only <b>{am['excl']} of {am['terms']:,} AI Max terms ({am['exclPct']}%)</b> have been negated. More important than the headline rate is what is <em>still running</em>: {am['badActive']} irrelevant or clearly wasteful AI Max terms carry no negative, and have already spent {money(am['badActiveSpend'])}. A further {money(am['badExclSpend'])} was spent on bad terms <em>before</em> the negative was applied — exclusion is retrospective, so it recovers nothing.</p>
 <figure class="fig"><div class="legend"><span><i style="background:var(--aim)"></i>Excluded</span><span><i style="background:var(--std)"></i>Irrelevant/wasteful &amp; still active</span></div><div class="chart-scroll">{chart_excl}</div>
  <figcaption><b>Exclusion coverage vs. unguarded waste.</b> South Florida is the only account being actively defended (27.0% excluded, and it is also the account with least to defend against). Ortho Excellence is the inverse: 4.5% excluded while 34.4% of its terms are off-target — 460 bad terms running unchecked. Note that {am['exclRel']} <em>relevant</em> AI Max terms have also been negated across the set, so some exclusion work is cutting into good traffic.</figcaption></figure>
</section>

<section>
 <div class="shead"><div class="n">06</div><div><h2>Account files</h2></div></div>
 <p style="margin-bottom:26px">Each account is judged against the services it actually sells, using its own keywords, ad groups, and campaign structure as the reference for what “relevant” means.</p>
 {''.join(acct_block(n) for n in ORDER)}
</section>

<section>
 <div class="shead"><div class="n">07</div><div><h2>Cross-account summary</h2></div></div>
 <div class="tw"><table>
  <thead><tr><th>Account</th><th>Relevant</th><th>Borderline</th><th>Irrelevant</th><th>Excluded</th><th>AI Max spend</th><th>Conv.</th><th>AI Max CPA</th><th>Keyword CPA</th><th style="text-align:left">Recommendation</th></tr></thead>
  <tbody>{xrows}</tbody><tfoot>{xfoot}</tfoot></table></div>
 <div class="tiles" style="margin-top:26px">
  <div class="tile"><div class="k">Total AI Max search terms</div><div class="v">{am['terms']:,}</div><div class="s">{am['terms']/(am['terms']+st['terms'])*100:.0f}% of all search terms</div></div>
  <div class="tile"><div class="k">Overall relevant</div><div class="v">{am['relPct']}%</div><div class="s">{am['cats']['Highly Relevant']+am['cats']['Relevant / Acceptable']:,} terms</div></div>
  <div class="tile"><div class="k">Overall borderline</div><div class="v">{am['borPct']}%</div><div class="s">{am['cats']['Borderline / Low Intent']:,} terms</div></div>
  <div class="tile"><div class="k">Overall irrelevant</div><div class="v bad">{am['irrPct']}%</div><div class="s">{am['cats']['Irrelevant']+am['cats']['Clearly Wasteful']:,} terms</div></div>
  <div class="tile"><div class="k">Overall exclusion rate</div><div class="v bad">{am['exclPct']}%</div><div class="s">{am['excl']} terms negated</div></div>
  <div class="tile"><div class="k">Total AI Max spend</div><div class="v">{money(am['cost'])}</div><div class="s">{am['cost']/tot_cost*100:.0f}% of {money(tot_cost)} search spend</div></div>
  <div class="tile"><div class="k">Spend on irrelevant searches</div><div class="v bad">{money(am['irrSpend'])}</div><div class="s">{am['irrSpendPct']}% of AI Max spend</div></div>
  <div class="tile"><div class="k">Total AI Max conversions</div><div class="v">{am['conv']:g}</div><div class="s">of which {CE['Highly Relevant']['conv']:g} from highly relevant searches</div></div>
  <div class="tile"><div class="k">Overall AI Max CPA</div><div class="v bad">{m0(am['cpa'])}</div><div class="s">keyword benchmark {m0(st['cpa'])}</div></div>
  <div class="tile"><div class="k">AI Max spend that produced no conversion</div><div class="v bad">{am['zeroConvPct']}%</div><div class="s">{money(am['zeroConvSpend'])} · keyword traffic {st['zeroConvPct']}%</div></div>
 </div>
</section>

<section>
 <div class="shead"><div class="n">08</div><div><h2>Expert verdict</h2></div></div>
 <div class="final">
  <p class="eyebrow">Overall verdict</p>
  <div class="big">Keep AI Max enabled — under tight controls.<br>Restrict it hard on Ortho Excellence and Holt.</div>
  <p style="max-width:70ch">Disabling AI Max across the board is not what this data supports. The highly relevant slice of AI Max traffic converted at {m0(CE['Highly Relevant']['cost']/CE['Highly Relevant']['conv'])} against a {m0(st['cpa'])} keyword benchmark — it is the <em>unrestrained</em> 59% of AI Max traffic that destroys the average, not the mechanism. But leaving it as-is is also indefensible: it is currently spending {am['cost']/tot_cost*100:.0f}% of search budget to return {am['conv']/tot_conv*100:.0f}% of conversions.</p>
  <div class="rule"></div>
  <div class="two" style="gap:30px">
   <div>
    <h4 style="color:var(--ink)">What AI Max is doing</h4>
    <ul style="font-size:14.5px">
     <li><b>Discovering valuable incremental searches?</b> <span style="color:var(--crit-ink)">Barely.</span> Six of 17 converting terms contained no vocabulary the account already reached; the “new” words it found were competitors’ proper nouns.</li>
     <li><b>Producing conversions efficiently?</b> <span style="color:var(--crit-ink)">No.</span> {m0(am['cpa'])} vs {m0(st['cpa'])}; {am['cvr']}% CVR vs {st['cvr']}%; {am['zeroConvPct']}% of its spend returned nothing.</li>
     <li><b>Duplicating existing intent?</b> <span style="color:var(--warn-ink)">Partly</span> — and where it duplicates, it performs fine. That is the salvageable part.</li>
     <li><b>Generating excessive irrelevant traffic?</b> <span style="color:var(--crit-ink)">Yes.</span> {am['irrPct']}% of terms vs {st['irrPct']}%; 249 bare street addresses; 4× the off-target rate of keyword matching.</li>
     <li><b>Creating unnecessary spend?</b> <span style="color:var(--crit-ink)">Yes — {money(am['irrSpend'])}</span> in 30 days, annualising to roughly {money(am['irrSpend']*12)} across these five accounts alone.</li>
     <li><b>Requiring too much manual exclusion?</b> <span style="color:var(--crit-ink)">Yes, at current settings.</span> {am['badActive']} bad terms are still unguarded, and negatives only ever recover money after it is spent.</li>
    </ul>
   </div>
   <div>
    <h4 style="color:var(--ink)">Do this next</h4>
    <ul style="font-size:14.5px">
     <li><b>Ortho Excellence — restrict hard, this week.</b> AI Max is 73.5% of its search spend at 8.3% relevance. Either turn it off in the Puyallup/Bonney Lake campaign or add brand-exclusion + a general-dentistry negative list before the next billing cycle. This account is the single biggest source of waste per dollar in the set.</li>
     <li><b>Holt — restrict.</b> Add a numeric/address negative pattern immediately: 205 address terms cost {money(296.66)} and returned one questionable conversion. Then negate the non-dental specialties (veneers, endodontics, wisdom teeth, optometry).</li>
     <li><b>Deploy a shared negative list</b> across all four orthodontic accounts: general-dentistry services, other dental specialties, non-dental medical, DTC aligner brands, and street-address patterns. This single list addresses {money(am['irrSpend']+am['borSpend']*0.5)}+ of the observed waste.</li>
     <li><b>Turn on brand exclusions</b> so AI Max stops conquesting competitor practice names by default — {am['namedSpendPct']}% of its spend is named-entity traffic.</li>
     <li><b>Fix conversion tracking before the next review.</b> Without conversion values and action names, no one can tell a booked consult from a form start — and that is the difference between “AI Max works” and “AI Max fills the CRM with junk”.</li>
     <li><b>Re-measure in 60–90 days.</b> Goodman and Sabinsky need volume before any verdict; do not disable either on 10–13 clicks.</li>
    </ul>
   </div>
  </div>
  <div class="rule"></div>
  <p class="eyebrow">Confidence level</p>
  <div style="display:flex;flex-wrap:wrap;gap:12px 26px;align-items:center;margin-bottom:12px">
   <span class="chip info" style="font-size:13px"><i style="background:var(--crit)"></i>High — relevance &amp; waste findings</span>
   <span class="chip info" style="font-size:13px"><i style="background:var(--warn)"></i>Medium — account-level CPA rankings</span>
   <span class="chip info" style="font-size:13px"><i style="background:var(--ink-3)"></i>Low — Goodman &amp; Sabinsky individually</span>
  </div>
  <p style="max-width:70ch;margin-bottom:0"><b>High confidence</b> that AI Max is generating materially more irrelevant traffic and unnecessary spend: that rests on {am['terms']:,} classified terms and {money(am['cost'])} of spend, it reproduces in all five accounts, and it does not depend on conversion counts. <b>Medium confidence</b> on the efficiency verdict: {am['conv']:g} AI Max conversions in one 30-day window is a thin base, 29–45% of spend is hidden in “Other search terms”, and conversion quality cannot be verified without action-level data. <b>Low confidence</b> on Goodman and Sabinsky individually — 13 and 10 clicks respectively. Nothing here justifies a global shutdown; everything here justifies tight controls now and a re-read in 60–90 days.</p>
 </div>
</section>

<p class="foot">Source: Google Ads search terms reports, five accounts, {e(M['dateRange'])}.<br>
{am['terms']+st['terms']:,} search terms classified by account-specific intent rules; every spend and conversion figure reconciles exactly to the “Total: Search terms” line of each source file.<br>
Relevance classification is analyst judgement applied at scale, not a Google-supplied label — the category boundaries are stated in §02 so they can be argued with.</p>
</div>
<div class="tip" id="tip"></div>
<script>
(function(){{
 var t=document.getElementById('tip');
 document.addEventListener('mouseover',function(ev){{
  var el=ev.target.closest('[data-tip]');
  if(!el){{t.classList.remove('on');return;}}
  t.textContent=el.getAttribute('data-tip');t.classList.add('on');
 }});
 document.addEventListener('mousemove',function(ev){{
  if(!t.classList.contains('on'))return;
  var x=ev.clientX+14,y=ev.clientY+16;
  if(x+t.offsetWidth>innerWidth-8)x=ev.clientX-t.offsetWidth-14;
  if(y+t.offsetHeight>innerHeight-8)y=ev.clientY-t.offsetHeight-14;
  t.style.left=x+'px';t.style.top=y+'px';
 }});
}})();
</script>
'''
open('/home/user/ai-max-analysis/report/ai-max-audit.html','w').write(open('/home/user/ai-max-analysis/analysis/head.html').read()+BODY)
print('written', len(BODY))
