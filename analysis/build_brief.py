from charts import *
am,st=T['aimax'],T['std']; CE=M['catEfficiency']
tot_cost=am['cost']+st['cost']; tot_conv=am['conv']+st['conv']
SA={'Ortho Excellence':'Ortho Exc.','Holt Orthodontics':'Holt','South Florida':'S. Florida','Sabinsky':'Sabinsky','Goodman Ortho':'Goodman'}
V={'Ortho Excellence':('res','Restrict hard'),'Holt Orthodontics':('res','Restrict'),
   'South Florida':('mon','Keep + monitor'),'Sabinsky':('mon','Restrict / monitor'),
   'Goodman Ortho':('mon','Monitor')}
WHY={'Ortho Excellence':'73.5% of account spend at 8.3% relevance; 6 of 7 conversions were general-dental, not ortho.',
 'Holt Orthodontics':'Largest absolute waste: $500 off-target, incl. $297 on 205 bare street addresses. CPA 48% worse.',
 'South Florida':'Only account where AI Max lands on-service — it is a general dental practice. 27% already negated.',
 'Sabinsky':'Zero conversions on $96 / 10 clicks. A red flag, but too few clicks to call it a failure.',
 'Goodman Ortho':'Cleanest profile and the only CPA win — but $112 and 13 clicks. Not actionable either way.'}
def cpa_of(d): return d['cost']/d['conv'] if d['conv'] else None

def pfoot(n):
    return (f'<div class="pfoot"><span>AI Max Search Term Audit · {am["terms"]+st["terms"]:,} terms classified · '
            f'{e(M["dateRange"].split("(")[0].strip())}</span><span>Page {n} of 3</span></div>')
def phead(t):
    return f'<div class="phead"><div class="t">{e(t)}</div><div class="t">Orthodontic &amp; dental · Google Ads</div></div>'

LEG5=legend([(SHORT[c],CVAR[i]) for i,c in enumerate(CATS)])
LEG2=legend([('AI Max','var(--aim)'),('Keyword-matched (standard)','var(--std)')])

# ---- charts ----
rel_rows=[(n,[(c,A[n]['aimax']['cats'][c]/A[n]['aimax']['terms']*100,f"{A[n]['aimax']['cats'][c]} terms") for c in CATS],
           f"{A[n]['aimax']['terms']:,} terms") for n in ORDER]
rel_rows.append(('ALL AI MAX',[(c,am['cats'][c]/am['terms']*100,f"{am['cats'][c]} terms") for c in CATS],f"{am['terms']:,} terms"))
rel_rows.append(('KEYWORD-MATCHED',[(c,st['cats'][c]/st['terms']*100,f"{st['cats'][c]} terms") for c in CATS],'the benchmark'))
c_rel=stacked(rel_rows,W=980,rh=31,lw=176)

sp_rows=[(n,[(c,(A[n]['aimax']['catCost'][c]/A[n]['aimax']['cost']*100 if A[n]['aimax']['cost'] else 0),money(A[n]['aimax']['catCost'][c])) for c in CATS],money(A[n]['aimax']['cost'])) for n in ORDER]
sp_rows.append(('ALL AI MAX',[(c,am['catCost'][c]/am['cost']*100,money(am['catCost'][c])) for c in CATS],money(am['cost'])))
sp_rows.append(('KEYWORD-MATCHED',[(c,st['catCost'][c]/st['cost']*100,money(st['catCost'][c])) for c in CATS],'the benchmark'))
c_spend=stacked(sp_rows,W=980,rh=30,lw=176)

c_cpa=grouped([SA[n] for n in ORDER]+['ALL'],
  [A[n]['aimax']['cpa'] or 0 for n in ORDER]+[am['cpa']],
  [A[n]['std']['cpa'] or 0 for n in ORDER]+[st['cpa']], lambda v:f'${v:,.0f}', W=470, gh=102)
c_irr=grouped([SA[n] for n in ORDER]+['ALL'],
  [A[n]['aimax']['irrSpendPct'] for n in ORDER]+[am['irrSpendPct']],
  [A[n]['std']['irrSpendPct'] for n in ORDER]+[st['irrSpendPct']], lambda v:f'{v:.0f}%', W=470, gh=102)
c_catcpa=hbars([(f"{SHORT[c]} · {CE[c]['conv']:g} conv", CE[c]['cost']/CE[c]['conv'] if CE[c]['conv'] else 0, CVAR[i]) for i,c in enumerate(CATS)],
  W=490, rh=21, lw=178, fmt=lambda v:f'${v:,.0f}')
c_excl=grouped([SA[n] for n in ORDER]+['ALL'],
  [A[n]['aimax']['exclPct'] for n in ORDER]+[am['exclPct']],
  [round(A[n]['aimax']['badActive']/A[n]['aimax']['terms']*100,1) for n in ORDER]+[round(am['badActive']/am['terms']*100,1)],
  lambda v:f'{v:.0f}%', W=470, gh=102)

xrows=''.join(
 f'<tr><td><b>{e(n)}</b></td><td>{A[n]["aimax"]["relPct"]}%</td>'
 f'<td>{A[n]["aimax"]["irrPct"]}%</td><td>{A[n]["aimax"]["exclPct"]}%</td>'
 f'<td>{money(A[n]["aimax"]["cost"])}</td>'
 f'<td>{A[n]["aimax"]["conv"]:g}</td><td>{m0(A[n]["aimax"]["cpa"])}</td>'
 f'<td style="color:var(--ink-3)">{m0(A[n]["std"]["cpa"])}</td>'
 f'<td style="text-align:left"><span class="chip {V[n][0]}"><i></i>{e(V[n][1])}</span></td></tr>' for n in ORDER)
xfoot=(f'<tr><td>All five accounts</td><td>{am["relPct"]}%</td><td>{am["irrPct"]}%</td>'
 f'<td>{am["exclPct"]}%</td><td>{money(am["cost"])}</td><td>{am["conv"]:g}</td><td>{m0(am["cpa"])}</td>'
 f'<td>{m0(st["cpa"])}</td><td style="text-align:left">Restrict</td></tr>')
vstrip=''.join(f'<div class="vrow"><span class="chip {V[n][0]}"><i></i>{e(V[n][1])}</span>'
  f'<b>{e(n)}</b><span class="w">{WHY[n]}</span></div>' for n in ORDER)
wcards=''.join(f'<div class="why"><b>{e(n)}</b> <span>{WHY[n]}</span></div>' for n in ORDER)

P1=f'''<div class="page">
{phead('Page 1 — Verdict & evidence')}
<p class="eyebrow">Google Ads · AI Max search-term audit · executive brief</p>
<h1>AI Max is buying competitors’ names,<br>not new patients.</h1>
<div class="verdictbox">
 <p class="eyebrow" style="margin-bottom:0">Overall verdict</p>
 <div class="big">Keep AI Max enabled — under tight controls.<br>Restrict it hard on Ortho Excellence and Holt.</div>
 <div class="kv"><b>Why not disable</b><span>The highly relevant slice of AI Max converted at {m0(cpa_of(CE["Highly Relevant"]))} — better than the {m0(st['cpa'])} keyword benchmark. The mechanism works; it is the unrestrained {100-am['relPct']:.0f}% that destroys the average.</span></div>
 <div class="kv"><b>Why not leave it</b><span>AI Max takes {am['cost']/tot_cost*100:.0f}% of search spend to return {am['conv']/tot_conv*100:.0f}% of conversions, at a {(am['cpa']/st['cpa']-1)*100:.0f}% worse cost per lead.</span></div>
 <div class="kv"><b>Confidence</b><span><b>High</b> on relevance &amp; waste ({am['terms']:,} classified terms, reproduces in all five accounts, independent of conversion counts). <b>Medium</b> on efficiency ({am['conv']:g} conversions, 30 days). <b>Low</b> on Goodman &amp; Sabinsky individually (13 and 10 clicks).</span></div>
</div>
<div class="tiles">
 <div class="tile"><div class="k">AI Max share of spend</div><div class="v">{am['cost']/tot_cost*100:.0f}%</div><div class="s">{money(am['cost'])} of {money(tot_cost)}</div></div>
 <div class="tile"><div class="k">Share of conversions</div><div class="v">{am['conv']/tot_conv*100:.0f}%</div><div class="s">{am['conv']:g} of {tot_conv:g} — buys more than it returns</div></div>
 <div class="tile"><div class="k">Cost per conversion</div><div class="v bad">{m0(am['cpa'])}</div><div class="s">vs {m0(st['cpa'])} keyword — {(am['cpa']/st['cpa']-1)*100:.0f}% worse</div></div>
 <div class="tile"><div class="k">Terms that are relevant</div><div class="v bad">{am['relPct']:.0f}%</div><div class="s">vs {st['relPct']:.0f}% on keyword traffic</div></div>
 <div class="tile"><div class="k">Spend on bad terms</div><div class="v bad">{money(am['irrSpend'])}</div><div class="s">{am['irrSpendPct']}% of AI Max spend vs {st['irrSpendPct']}%</div></div>
</div>
<div class="sec">
 <h2>What AI Max actually bought</h2>
 <p><b>{am['namedSpendPct']}% of AI Max spend went to queries naming a specific practice, provider, or street address</b> — against {st['namedSpendPct']}% of keyword-matched spend. 249 terms were bare street addresses with no service word at all, costing {money(337.90)}. Its vocabulary skews to “dental” (957 uses) and “dentist” (388) over all orthodontic terms combined (574): on-service for one general dental practice, off-service for four orthodontists.</p>
 <figure>{LEG5}{c_rel}
 <figcaption><b>Share of AI Max search terms by patient intent, per account.</b> Bottom two rows are the control: all AI Max traffic, then the same classifier applied to keyword-matched traffic in the same accounts. Keyword traffic is {st['relPct']}% relevant and {st['irrPct']}% off-target; AI Max is {am['relPct']}% relevant and {am['irrPct']}% off-target — a four-fold increase. Ortho Excellence is the extreme: {A['Ortho Excellence']['aimax']['relPct']}% relevant.</figcaption></figure>
</div>
<div class="sec">
 <h2>Verdict by account</h2>
 <div class="vstrip">{vstrip}</div>
</div>
{pfoot(1)}
</div>'''

P2=f'''<div class="page">
{phead('Page 2 — Performance vs. standard search')}
<div class="sec">
 <h2>AI Max vs. keyword-matched traffic</h2>
 <p style="margin-bottom:3.4mm">Same accounts, same window, same conversion tracking. The only variable is whether Google matched the query to a keyword or generated it through AI Max.</p>
 <div class="tw"><table>
 <thead><tr><th>Metric</th><th>AI Max</th><th>Keyword-matched</th><th style="text-align:left">Read</th></tr></thead><tbody>
 <tr><td>Search terms</td><td>{am['terms']:,}</td><td>{st['terms']:,}</td><td style="text-align:left;color:var(--ink-3)">AI Max adds {(am['terms']/st['terms']-1)*100:.0f}% more terms</td></tr>
 <tr><td>Clicks</td><td>{am['clicks']:,}</td><td>{st['clicks']:,}</td><td style="text-align:left;color:var(--ink-3)">{am['clicks']/(am['clicks']+st['clicks'])*100:.0f}% of clicks</td></tr>
 <tr><td>CTR</td><td>{am['ctr']}%</td><td>{st['ctr']}%</td><td style="text-align:left;color:var(--crit-ink)">−{(1-am['ctr']/st['ctr'])*100:.0f}% — weaker query-to-ad match</td></tr>
 <tr><td>Avg. CPC</td><td>{money(am['cpc'])}</td><td>{money(st['cpc'])}</td><td style="text-align:left;color:var(--good-ink)">−{(1-am['cpc']/st['cpc'])*100:.0f}% — clicks are cheaper</td></tr>
 <tr><td>Cost</td><td>{money(am['cost'])}</td><td>{money(st['cost'])}</td><td style="text-align:left;color:var(--ink-3)">{am['cost']/tot_cost*100:.0f}% of search spend</td></tr>
 <tr><td>Conversions</td><td>{am['conv']:g}</td><td>{st['conv']:g}</td><td style="text-align:left;color:var(--ink-3)">{am['conv']/tot_conv*100:.0f}% of conversions</td></tr>
 <tr><td>Conversion rate</td><td>{am['cvr']}%</td><td>{st['cvr']}%</td><td style="text-align:left;color:var(--crit-ink)">−{(1-am['cvr']/st['cvr'])*100:.0f}% — cheap clicks that don’t convert</td></tr>
 <tr><td><b>Cost per conversion</b></td><td><b>{m0(am['cpa'])}</b></td><td><b>{m0(st['cpa'])}</b></td><td style="text-align:left;color:var(--crit-ink)"><b>+{(am['cpa']/st['cpa']-1)*100:.0f}% worse per lead</b></td></tr>
 <tr><td>Relevant terms</td><td>{am['relPct']}%</td><td>{st['relPct']}%</td><td style="text-align:left;color:var(--crit-ink)">−{st['relPct']-am['relPct']:.1f} points</td></tr>
 <tr><td>Irrelevant + wasteful terms</td><td>{am['irrPct']}%</td><td>{st['irrPct']}%</td><td style="text-align:left;color:var(--crit-ink)">{am['irrPct']/st['irrPct']:.1f}× more off-target</td></tr>
 <tr><td>Spend on irrelevant terms</td><td>{money(am['irrSpend'])} ({am['irrSpendPct']}%)</td><td>{money(st['irrSpend'])} ({st['irrSpendPct']}%)</td><td style="text-align:left;color:var(--crit-ink)">{am['irrSpendPct']/st['irrSpendPct']:.0f}× more waste</td></tr>
 <tr><td>Named-entity spend</td><td>{am['namedSpendPct']}%</td><td>{st['namedSpendPct']}%</td><td style="text-align:left;color:var(--crit-ink)">competitors &amp; addresses</td></tr>
 <tr><td>Spend with zero conversions</td><td>{am['zeroConvPct']}%</td><td>{st['zeroConvPct']}%</td><td style="text-align:left;color:var(--crit-ink)">{money(am['zeroConvSpend'])} returned nothing</td></tr>
 </tbody></table></div>
</div>
<div class="sec two" style="gap:5mm">
 <figure><h4>Cost per conversion, by account</h4>{LEG2}{c_cpa}
  <figcaption>AI Max costs more per lead in four of five accounts. Sabinsky has no bar — it produced no conversions at all.</figcaption></figure>
 <figure><h4>Share of spend on off-target terms</h4>{LEG2}{c_irr}
  <figcaption>The cleanest separation in the dataset, and it does not depend on conversion counts. Keyword traffic stays near zero everywhere.</figcaption></figure>
</div>
<div class="sec two" style="gap:5mm">
 <figure><h4>AI Max cost per conversion, by intent class</h4>{c_catcpa}
  <figcaption>Relevance predicts efficiency. Highly relevant AI Max traffic beats the {m0(st['cpa'])} keyword benchmark; everything below it runs 1.2–2.1× worse. This is the case for restricting rather than disabling.</figcaption></figure>
 <figure><h4>Exclusion coverage vs. unguarded waste</h4>
  <div class="legend"><span><i style="background:var(--aim)"></i>Terms excluded</span><span><i style="background:var(--std)"></i>Off-target &amp; still active</span></div>{c_excl}
  <figcaption>Only {am['excl']} of {am['terms']:,} AI Max terms ({am['exclPct']}%) are negated. {am['badActive']} off-target terms still carry no negative and have spent {money(am['badActiveSpend'])}. Exclusion is retrospective — it recovers nothing already spent.</figcaption></figure>
</div>
<div class="note crit">
 <h4>The conversions AI Max did produce are not all real leads</h4>
 <p>Of {am['conv']:g} AI Max conversions, only <b>{CE['Highly Relevant']['conv']:g} came from highly relevant searches</b>. The rest include a hospital lookup (<span class="mono">sutter health hospital sacramento</span>, $23.61), a bare address (<span class="mono">140 roseville pkwy suite 150…</span>, $28.20) and, at Ortho Excellence, six conversions from general-dental searches (<span class="mono">dentist tacoma</span>, <span class="mono">dental clinic near me</span>) on an account that sells orthodontics. <b>Incrementality:</b> six of the 17 converting terms contained no word the account already reached through keywords — the rest is duplicated intent, and the “new” vocabulary is almost entirely competitors’ proper nouns. AI Max found new <em>names</em>, not new <em>demand</em>.</p>
</div>
{pfoot(2)}
</div>'''

P3=f'''<div class="page">
{phead('Page 3 — Account verdicts & actions')}
<div class="sec">
 <h2>Account-by-account</h2>
 <p style="margin-bottom:3.4mm">Relevance is judged per account, against the services each practice actually advertises — “emergency dentist” is highly relevant for South Florida and irrelevant for Sabinsky.</p>
 <div class="tw"><table class="acct">
 <thead><tr><th>Account</th><th>Relevant</th><th>Irrelevant</th><th>Excluded</th><th>AI Max spend</th><th>Conv.</th><th>AI Max CPA</th><th>Keyword CPA</th><th style="text-align:left">Verdict</th></tr></thead>
 <tbody>{xrows}</tbody><tfoot>{xfoot}</tfoot></table></div>
</div>
<div class="sec">
 <h2>Where the AI Max money went</h2>
 <figure>{LEG5}{c_spend}
  <figcaption><b>Page 1’s picture weighted by money rather than term count — the chart that matters.</b> {am['irrSpendPct']}% of AI Max spend ({money(am['irrSpend'])}) bought irrelevant or wasteful clicks, against {st['irrSpendPct']}% ({money(st['irrSpend'])}) on keyword traffic. Only {money(CE['Highly Relevant']['cost'])} — {CE['Highly Relevant']['cost']/am['cost']*100:.0f}% — went to unambiguously on-target searches.</figcaption></figure>
</div>
<div class="sec two wide" style="gap:5mm">
 <div>
  <h2>Do this next</h2>
  <ul style="font-size:8pt">
   <li><b>Ortho Excellence — restrict hard, this week.</b> {A['Ortho Excellence']['spendShare']}% of search spend at {A['Ortho Excellence']['aimax']['relPct']}% relevance. Turn AI Max off in the Puyallup/Bonney Lake campaign, or add brand exclusions plus a general-dentistry negative list before the next billing cycle.</li>
   <li><b>Holt — add an address/numeric negative pattern now.</b> 205 address terms cost {money(296.66)} for one questionable conversion. Then negate non-dental specialties: veneers, endodontics, wisdom teeth, optometry.</li>
   <li><b>Deploy one shared negative list</b> across all four ortho accounts — general dentistry, other dental specialties, non-dental medical, DTC aligner brands, address patterns. It addresses most of the {money(am['irrSpend'])} waste.</li>
   <li><b>Turn on brand exclusions</b> — {am['namedSpendPct']}% of AI Max spend is competitor and address traffic.</li>
   <li><b>Fix conversion tracking</b> before the next review: no values or action names means nobody can tell a booked consult from a form start.</li>
   <li><b>Re-measure in 60–90 days.</b> Do not disable Goodman or Sabinsky on 10–13 clicks.</li>
  </ul>
 </div>
 <div>
  <h2>Three limits on this data</h2>
  <div class="note"><h4>1 · Google withholds 29–45% of the spend</h4>
   <p>Named terms cover only 55–71% of each account’s search spend; the rest sits in the privacy-thresholded “Other search terms” bucket, attributable to neither AI Max nor keywords. Holt is weakest — 45% of its conversions are invisible.</p></div>
  <div class="note"><h4>2 · No conversion values or action names</h4>
   <p>One blended <span class="mono">Conversions</span> column, so booked consults cannot be separated from form starts. Treat every conversion here as a lead signal of unknown quality.</p></div>
  <div class="note"><h4>3 · One 30-day window, 267 AI Max clicks</h4>
   <p>Ample for relevance conclusions, thin for efficiency ones. Goodman ($112) and Sabinsky ($96) are too small to judge on performance at all.</p></div>
 </div>
</div>
{pfoot(3)}
</div>'''

open('/home/user/ai-max-analysis/report/ai-max-brief.html','w').write(
  open('/home/user/ai-max-analysis/analysis/brief_head.html').read()+P1+P2+P3)
print('brief written')
