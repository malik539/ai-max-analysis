import re
ORTHO_ACCOUNTS = {'Goodman Ortho','Holt Orthodontics','Ortho Excellence','Sabinsky'}

def rx(words):
    """word-boundary-safe matcher; entries may be multi-word phrases or prefixes ending in *"""
    parts=[]
    for w in words:
        w=w.strip()
        if w.endswith('*'): parts.append(r'\b'+re.escape(w[:-1])+r'\w*')
        else: parts.append(r'\b'+re.escape(w)+r'\b')
    return re.compile('|'.join(parts), re.I)

BRAND = {
 'Goodman Ortho': rx(['goodman']),
 'Holt Orthodontics': rx(['holt','drholt']),
 'Ortho Excellence': rx(['orthodontic excellence','ortho excellence','orthodontics excellence','excellence orthodontic*']),
 'Sabinsky': rx(['sabinsky','sabinski']),
 'South Florida': rx(['south florida dental','south florida dentistry','south florida dental centre','south florida dental center']),
}

ORTHO = rx(['brace*','bracket*','invisalign','invisilign','invisalgin','invisiline','invisilive','invisible line','invisible brace*',
 'aligner*','clearcorrect','clear correct','spark aligner*','ortodoncia','frenos','frenillos','ortho','orthodont*','ortodont*',
 'orthodonist*','orthodintist*','retainer*','expander*','marpe','rpe','herbst','overbite','underbite','crossbite','openbite','open bite',
 'crooked teeth','straighten*','teeth straightening','straight teeth','crowded teeth','gap teeth','teeth gap','bite correction',
 'jaw alignment','headgear','itero','damon','tmj','tmd','jaw pain','elastics','spacers','malocclusion','impacted canine'])

DENTAL = rx(['dentist*','dental','dentista*','dentistry','odontolog*','odontolo*','muela*','diente*','denture*','dentadura*',
 'teeth cleaning','cleaning','cavity','cavities','caries','filling*','crown*','root canal','extraction*','extract','tooth','teeth',
 'toothache','emergency dent*','implant*','wisdom teeth','wisdom tooth','veneer*','whitening','blanqueamiento','gum*','encias',
 'periodont*','endodont*','oral surg*','oral surgeon*','maxillofacial','smile makeover','bonding','deep clean*','scaling','x ray',
 'x rays','xray*','abscess','chipped','broken tooth','molar*','canine','enamel','plaque','tartar','floss*','sedation','nitrous',
 'pediatric dent*','kids dent*','childrens dent*',"children's dent*",'family dent*','mouthguard','night guard','dds','dmd',
 'prosthodont*','myofunctional','frenectomy','tongue tie','bruxism','halitosis','bad breath','cleaning and exam','oral health',
 'sleep apnea','snoring','mouth','sedation dent*','oral care','dentures'])

OTHER_MED = rx(['optometr*','chiroprac*','obgyn','ob gyn','urgent care','hospital','dermatolog*','physical therapy','orthopedic*',
 'orthopaedic*','podiatr*','primary care','plastic surgery','botox','med spa','medspa','pediatrician*','cardiolog*','ihss',
 'sutter health','planned parenthood','veterinar*','pharmacy','eye doctor*','eye doctors','eye care','eye appointment','eye exam',
 'vision center','lasik','hearing aid*','audiolog*','dialysis','mental health','psychiatr*','urologist*','emergency room',
 'blood test','labcorp','quest diagnostics','walmart','target','dmv','social security','food stamps','unemployment','er',
 'medical clinic','walk in clinic','aesthetic*','esthetic*','wellness center','massage','acupuncture','weight loss','clinica medica'])

JOB_INFO = rx(['job*','jobs','career*','hiring','salary','salaries','employment','resume','university','college','course*',
 'training','certification','how to become','wikipedia','definition','meaning','reddit','coupon*','groupon','free'])

INSURANCE_NET = rx(['deltacare','delta dental','metlife','cigna','aetna','united healthcare','unitedhealthcare','guardian dental',
 'humana','ameritas','medicaid','medi cal','medical','molina','apple health','simplyhealthcare','sunshine health','providers',
 'in network','hmo','ppo','dhmo','1199','onesmile','savings plan','discount plan','insurance'])

DTC = rx(['byte','smiledirectclub','smile direct club','smiledirect','candid','alignerco','smileie','snap on smile','pop on veneer*',
 'diy brace*','at home aligner*','impress','newsmile','strayt','sdc'])

ADDR = re.compile(r'^\s*\d{2,6}\s+[a-z0-9\.\'\- ]{0,40}?\b(ave|avenue|st|street|rd|road|blvd|boulevard|dr|drive|ln|lane|way|pkwy|parkway|ct|court|hwy|highway|pl|place|ter|terrace|cir|circle|suite|ste|loop|trail|plaza)\b', re.I)
NUMSTART = re.compile(r'^\s*\d{2,6}\s+\w')
PHONE = re.compile(r'^\s*\(?\d{3}\)?[\s\-]?\d{3}([\s\-]?\d{4})?\s*$')
ZIP = re.compile(r'\b\d{5}\b')

GEO_LOCAL = {
 'Goodman Ortho': rx(['bronx','riverdale','yonkers','manhattan','new york','ny','nyc','westchester','pelham','kingsbridge','fordham','white plains','mount vernon','throgs neck','morris park','parkchester']),
 'Holt Orthodontics': rx(['sacramento','folsom','rocklin','roseville','granite bay','elk grove','citrus heights','fair oaks','carmichael','orangevale','loomis','lincoln','auburn','antelope','natomas','rancho cordova','west sacramento','north highlands','davis','woodland','placer','el dorado hills','galt','wilton','arden','ca','california']),
 'Ortho Excellence': rx(['bonney lake','puyallup','sumner','tacoma','auburn','enumclaw','buckley','orting','graham','lake tapps','federal way','kent','edgewood','milton','spanaway','lakewood','parkland','pierce','wa','washington']),
 'Sabinsky': rx(['princeton','hillsborough','plainsboro','montgomery','belle mead','skillman','somerset','franklin park','east brunswick','south brunswick','monmouth junction','kendall park','lawrenceville','west windsor','nj','new jersey','edison','piscataway','bridgewater','flemington','manville','rocky hill','pennington','trenton','somerville']),
 'South Florida': rx(['coral springs','parkland','margate','coconut creek','tamarac','sunrise','plantation','fort lauderdale','ft lauderdale','pompano','deerfield','boca','boca raton','broward','weston','davie','lauderhill','north lauderdale','miramar','boynton','delray','fl','florida']),
}
GEO_FAR = {
 'Goodman Ortho': rx(['hackensack','new jersey','nj','connecticut','philadelphia','boston','california','texas','florida','miami','chicago','atlanta','houston','dallas','los angeles','india','uk','canada','toronto','london']),
 'Holt Orthodontics': rx(['indiana','fort wayne','texas','houston','dallas','austin','chicago','illinois','ohio','georgia','atlanta','phoenix','arizona','denver','colorado','las vegas','nevada','utah','oregon','portland','boise','idaho','new york','florida','miami','carmel indiana','san diego','los angeles','san francisco','san jose','fresno','bakersfield','long beach','irvine','anaheim','oakland','berkeley','india','uk','canada','toronto','london','mexico city','turkey','dubai','new jersey','washington','seattle']),
 'Ortho Excellence': rx(['tukwila','seattle','burien','renton','bellevue','everett','olympia','lacey','shoreline','mercer island','oakland','california','texas','fort wayne','indiana','chicago','new york','florida','india','uk','canada','arizona','oregon','portland','idaho','nevada']),
 'Sabinsky': rx(['new york','nyc','brooklyn','queens','staten island','bronx','philadelphia','california','texas','florida','chicago','india','uk','canada','atlanta','boston','connecticut']),
 'South Florida': rx(['miami','orlando','tampa','jacksonville','naples','fort myers','key west','georgia','atlanta','new york','texas','california','chicago','india','uk','canada','colombia','venezuela','cuba']),
}
# a name-like navigational query: 1-4 tokens, no service/geo/number signal
NAMEY = re.compile(r'^[a-z\'\.\&\- ]{3,40}$', re.I)
PRACTICEY = rx(['smiles','smile','ortho','dental','dentistry','care','associates','clinic','center','centre','group','family','kids','children'])

def classify(term, account):
    raw = str(term).lower().strip()
    ortho_acct = account in ORTHO_ACCOUNTS
    tok = raw.split()

    is_ortho  = bool(ORTHO.search(raw))
    is_dental = bool(DENTAL.search(raw))
    is_svc    = is_ortho or is_dental
    local     = bool(GEO_LOCAL[account].search(raw))
    far       = bool(GEO_FAR[account].search(raw))
    brandown  = bool(BRAND[account].search(raw))

    # --- 1. own brand ---
    if brandown: return 'Highly Relevant','Own brand / branded navigational'

    # --- 2. clearly wasteful ---
    if PHONE.match(raw): return 'Clearly Wasteful','Phone-number lookup'
    if (ADDR.search(raw) or (NUMSTART.match(raw) and ZIP.search(raw))) and not is_svc:
        return 'Clearly Wasteful','Bare street address (navigational, no service intent)'
    if OTHER_MED.search(raw) and not is_svc:
        return 'Clearly Wasteful','Non-dental medical / other vertical'
    if JOB_INFO.search(raw) and not is_svc:
        return 'Clearly Wasteful','Job / education / info-only query'
    if far and not local:
        return 'Clearly Wasteful','Out-of-market geography'
    if DTC.search(raw) and not is_svc:
        return 'Clearly Wasteful','DTC mail-order aligner brand (not a local patient)'

    # --- 3. insurance / network lookups ---
    if INSURANCE_NET.search(raw) and not is_svc:
        return 'Borderline / Low Intent','Insurance/network lookup, no service intent'

    # --- 4. service-bearing queries ---
    if is_svc:
        if DTC.search(raw): return 'Borderline / Low Intent','DTC mail-order aligner brand'
        if ortho_acct:
            if is_ortho:
                if re.search(r'\b(dds|dmd)\b', raw): return 'Borderline / Low Intent','Competitor provider name'
                if INSURANCE_NET.search(raw) and not re.search(r'\b(cost|price|how much|pay|afford)\b',raw):
                    return 'Relevant / Acceptable','Ortho + insurance/coverage question'
                if local or 'near me' in raw or re.search(r'\b(cost|price|how much|cheap|afford|best|top|payment|plan|consult|free consultation|open|appointment)\b', raw):
                    return 'Highly Relevant','Core orthodontic service + local/commercial intent'
                return 'Relevant / Acceptable','Core orthodontic service, no geo/commercial modifier'
            # dental but not ortho, on an ortho account
            if re.search(r'\b(oral surg\w*|maxillofacial|endodont\w*|periodont\w*|prosthodont\w*|wisdom teeth|wisdom tooth|root canal|implant\w*|denture\w*|dentadura|veneer\w*|whitening|blanqueamiento|extraction\w*|deep clean\w*|scaling|abscess|crown\w*|filling\w*|cavity|cavities|sleep apnea|snoring|frenectomy|tongue tie|dentist)\b', raw):
                return 'Irrelevant','Different dental specialty / non-orthodontic service'
            return 'Borderline / Low Intent','General dentistry (adjacent, not orthodontics)'
        else:  # South Florida general dental
            if re.search(r'\b(dds|dmd)\b', raw): return 'Borderline / Low Intent','Competitor provider name'
            if local or 'near me' in raw or re.search(r'\b(emergency|cost|price|how much|cheap|afford|best|payment|plan|open|today|now|appointment|urgent|cerca)\b', raw):
                return 'Highly Relevant','Core dental service + local/commercial intent'
            return 'Relevant / Acceptable','Dental service, no geo/commercial modifier'

    # --- 5. no service word: practice / person name navigational ---
    if PRACTICEY.search(raw):
        return 'Borderline / Low Intent','Competitor practice-name navigational (no service intent)'
    if NAMEY.match(raw) and 1 <= len(tok) <= 4:
        return 'Borderline / Low Intent','Person/practice-name navigational (no service intent)'
    return 'Irrelevant','No dental or orthodontic intent'
