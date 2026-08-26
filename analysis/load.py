import pandas as pd, os
src='/root/.claude/uploads/c9375526-8d63-577c-9250-ab51f191fe5c/'
names={'07d0d350':'Ortho Excellence','6aae726a':'Sabinsky','c2f6ba81':'Goodman Ortho','f5ed2f99':'Holt Orthodontics','fe94a28b':'South Florida'}
def load():
    out=[]
    for f in sorted(os.listdir(src)):
        nm=names[f.split('-')[0]]
        df=pd.read_excel(src+f, skiprows=2)
        df['Account']=nm
        if 'Campaign' not in df.columns: df['Campaign']='(single campaign)'
        df=df[~df['Search term'].astype(str).str.startswith('Total:')]
        df=df[df['Match type'].notna()]
        for c in ['Clicks','Impr.','Cost','Conversions','Avg. CPC']:
            df[c]=pd.to_numeric(df[c],errors='coerce').fillna(0)
        df['Added/Excluded']=df['Added/Excluded'].fillna('None')
        df['is_aimax']=df['Match type']=='AI Max'
        out.append(df[['Account','Search term','Match type','Added/Excluded','Campaign','Ad group','Clicks','Impr.','Cost','Conversions','is_aimax']])
    return pd.concat(out,ignore_index=True)
