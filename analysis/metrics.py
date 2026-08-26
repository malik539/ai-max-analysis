from load import load
from classify import classify
import pandas as pd
pd.set_option('display.width',260)
d=load()
d[['cat','why']]=d.apply(lambda r: pd.Series(classify(r['Search term'],r['Account'])),axis=1)
d.to_pickle('/tmp/all.pkl')
REL=['Highly Relevant','Relevant / Acceptable']
BAD=['Irrelevant','Clearly Wasteful']
def blk(g):
    n=len(g); cost=g.Cost.sum(); cl=g.Clicks.sum(); im=g['Impr.'].sum(); cv=g.Conversions.sum()
    rel=g[g.cat.isin(REL)]; irr=g[g.cat.isin(BAD)]; bor=g[g.cat=='Borderline / Low Intent']
    return pd.Series({'terms':n,'impr':im,'clicks':cl,'cost':round(cost,2),'conv':round(cv,2),
      'CTR%':round(cl/im*100,2) if im else 0,'CPC':round(cost/cl,2) if cl else 0,
      'CVR%':round(cv/cl*100,2) if cl else 0,'CPA':round(cost/cv,2) if cv else None,
      'rel%':round(len(rel)/n*100,1),'bor%':round(len(bor)/n*100,1),'irr%':round(len(irr)/n*100,1),
      'relSp':round(rel.Cost.sum(),2),'borSp':round(bor.Cost.sum(),2),'irrSp':round(irr.Cost.sum(),2),
      'irrSp%':round(irr.Cost.sum()/cost*100,1) if cost else 0,
      'excl':int((g['Added/Excluded']=='Excluded').sum()),'excl%':round((g['Added/Excluded']=='Excluded').sum()/n*100,1)})
if __name__=='__main__':
    print('===== AI MAX ====='); print(d[d.is_aimax].groupby('Account').apply(blk,include_groups=False).to_string())
    print(); print('===== NON-AI-MAX ====='); print(d[~d.is_aimax].groupby('Account').apply(blk,include_groups=False).to_string())
    print(); print('===== TOTALS by type ====='); print(d.groupby('is_aimax').apply(blk,include_groups=False).to_string())
