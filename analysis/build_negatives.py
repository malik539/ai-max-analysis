"""Sabinsky negative-keyword recommendation, derived from data/classified_search_terms.csv."""
import pandas as pd, re
d=pd.read_csv('/home/user/ai-max-analysis/data/classified_search_terms.csv')
s=d[d.Account=='Sabinsky'].copy()
BAD=['Irrelevant','Clearly Wasteful']; REL=['Highly Relevant','Relevant / Acceptable']

# (negative, match type, tier, rationale) — phrase negatives verified for zero relevant collateral
TIERS=[
 ('1 · Other dental specialties (not orthodontics)',[
  ('oral surgeon','Phrase'),('oral surgery','Phrase'),('oral and facial surgery','Phrase'),
  ('maxillofacial','Phrase'),('endodontist','Phrase'),('endodontics','Phrase'),('endodontic','Phrase'),
  ('periodontist','Phrase'),('periodontics','Phrase'),('prosthodontist','Phrase'),('prosthodontics','Phrase'),
  ('wisdom tooth','Phrase'),('wisdom teeth','Phrase'),('cavity','Phrase'),('cavities','Phrase'),
  ('teeth whitening','Phrase'),('veneers','Phrase'),('veneer','Phrase'),
  ('root canal','Phrase'),('denture','Phrase'),('dentures','Phrase'),('dental implant','Phrase'),
  ('tooth extraction','Phrase'),('tooth filling','Phrase'),('dental crown','Phrase')]),
 ('2 · General dentistry (see the trade-off note)',[
  ('dentist','Phrase'),('dentists','Phrase'),('dental office','Phrase'),('dental clinic','Phrase'),
  ('emergency dentist','Phrase'),('cosmetic dentist','Phrase'),('holistic dentist','Phrase'),
  ('pediatric dentist','Phrase'),('family dentist','Phrase')]),
 ('3 · DTC mail-order aligner brands',[
  ('byte','Phrase'),('candid','Phrase'),('smiledirectclub','Phrase'),('smile direct','Phrase'),
  ('alignerco','Phrase'),('smileie','Phrase'),('impress aligners','Phrase')]),
 ('4 · Out-of-market geography',[
  ('bronx','Phrase'),('new york','Phrase'),('nyc','Phrase'),('brooklyn','Phrase'),('queens','Phrase'),
  ('boston','Phrase'),('philadelphia','Phrase'),('newark','Phrase'),('north bergen','Phrase'),
  ('new hope pa','Phrase')]),
 ('5 · Non-dental verticals',[
  ('costco','Phrase'),('eye appointment','Phrase'),('eye doctor','Phrase'),('optometrist','Phrase'),
  ('chiropractor','Phrase'),('urgent care','Phrase'),('dermatologist','Phrase')]),
 ('6 · Competitor provider names',[
  ('d m d','Phrase'),('dmd','Phrase'),('daniel greenberg','Exact'),('nathan c steele','Exact'),
  ('freda and suriano bloomfield nj','Exact'),('pearly whites berkeley heights nj','Exact')]),
 ('7 · Navigational address lookups (exact only)',[
  ('213 summerhill rd east brunswick nj','Exact'),('520 lawrence square blvd','Exact'),
  ('746 livingston ave north brunswick nj 08902','Exact'),('8407 kennedy blvd north bergen','Exact')]),
]
DO_NOT=[('dds','Would block your own brand term "keith a sabinsky dds", plus "radiant orthodontics tiffany chen dds mds". Never negate dds on this account.'),
 ('3m clarity','3M Clarity is a ceramic bracket / aligner brand — this is orthodontic intent. Our classifier misfiled it; do not negate.'),
 ('oral medicine specialist near me','Orthodontists commonly treat orofacial pain and TMD, and this account already draws relevant TMJ traffic. Monitor rather than block.'),
 ('orofacial pain specialist near me','Same as above — orofacial pain is within orthodontic scope.'),
 ('pa (as a standalone negative)','Would block "orthodontist langhorne pa". Use the exact phrase "new hope pa" instead.'),
 ('sleep apnea','"sleep apnea orthodontics near me" is relevant and has already taken $15.28 of spend.'),
 ('tmj','All six TMJ terms in this account are relevant orthodontic queries.')]

rows=[]
for tier,negs in TIERS:
    for neg,mt in negs:
        pat=rf'\b{re.escape(neg)}' if mt=='Phrase' else rf'^{re.escape(neg)}$'
        hit=s[s['Search term'].str.contains(pat,case=False,na=False,regex=True)]
        rows.append(dict(Tier=tier,**{'Negative keyword':neg,'Match type':mt,
          'Terms blocked (30d)':len(hit),
          'Off-target blocked':int(hit.cat.isin(BAD).sum()),
          'Relevant blocked':int(hit.cat.isin(REL).sum()),
          'Impressions':int(hit['Impr.'].sum()),'Clicks':int(hit.Clicks.sum()),
          'Cost':round(float(hit.Cost.sum()),2),'Conversions':float(hit.Conversions.sum()),
          'Example terms':' ; '.join(hit[hit.cat.isin(BAD)]['Search term'].astype(str).unique()[:6])}))
neg_df=pd.DataFrame(rows)
neg_df.to_csv('/home/user/ai-max-analysis/negatives/sabinsky-negative-keywords.csv',index=False)

# the raw off-target term list, still active
notx=s[s.cat.isin(BAD)&(s['Added/Excluded']!='Excluded')].copy()
notx=notx[~notx['Search term'].isin(['3m clarity','oral medicine specialist near me','orofacial pain specialist near me'])]
notx=notx.sort_values(['cat','Cost','Impr.'],ascending=[True,False,False])
notx[['Search term','Match type','cat','why','Ad group','Impr.','Clicks','Cost','Conversions']].rename(
  columns={'cat':'Relevance class','why':'Reason','Match type':'Matched via'}
).to_csv('/home/user/ai-max-analysis/negatives/sabinsky-offtarget-search-terms.csv',index=False)

pd.DataFrame(DO_NOT,columns=['Do NOT negate','Why']).to_csv(
  '/home/user/ai-max-analysis/negatives/sabinsky-do-not-negate.csv',index=False)
print('negatives:',len(neg_df),'| off-target terms listed:',len(notx))
print(neg_df.groupby('Tier')[['Terms blocked (30d)','Off-target blocked','Relevant blocked']].sum().to_string())
