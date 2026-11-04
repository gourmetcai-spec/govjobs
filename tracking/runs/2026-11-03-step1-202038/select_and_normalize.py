import json,re
from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parent
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('p','li','br','div','h2','h3'):self.parts.append('\n')
 def handle_data(self,d):self.parts.append(d)
def plain(s):p=Plain();p.feed(s);return re.sub(r'\n\s*\n+','\n',''.join(p.parts)).strip()
a=json.loads((R/'new-native-controls.json').read_text());selected=[];decisions=[]
extras={'891275000','891288700','891239200','890446100','891357100','891376800','891290300','891264500','891296600','891354400','891445900','890755200','891369800','889812300','891220800'}
for n in a:
 codes={x['Code'] for x in n.get('JobCategoryCode',[])};yes=bool(codes&{'0501','0505','0510','0560','2210','1550','1560','1515','0110'}) or n['DocumentID'] in extras
 f=R/'announcements'/(n['DocumentID']+'.json');reason='Related finance/quantitative/IT occupation; prepare with uncertainty' if yes else 'Duties/occupation outside established finance/quantitative/IT/software/AI tracks'
 if f.exists():
  d=json.loads(f.read_text());locs=[x.get('address',{}).get('addressRegion','').strip() for x in d.get('jobLocation',[])]
  if locs and not set(locs)&{'MD','VA','DC'}:yes=False;reason='Official listed work locations do not include DC, Maryland or Virginia'
 if yes:selected.append(n['DocumentID'])
 decisions.append({'control':n['DocumentID'],'title':n['Title'],'agency':n['Agency'],'prepare':yes,'reason':reason,'official_evidence':str(f) if f.exists() else None})
frbsel={'R025992','R025936','R026010','R025997','R025954','R025987','R025906','R025914','R025916','R025881','R025594','R025422','R025663','R025812','R025945','R025986','R025976','R025977','R025978','R025980','R025918','R025924','R025917','R025885'}
native=[n for n in json.loads((R/'native-unique.json').read_text()) if not n['DocumentID'].startswith('R')];frbdec=[]
for n in json.loads((R/'frb/unique.json').read_text()):
 req=n['bulletFields'][0];info=json.loads((R/'frb'/(req+'.json')).read_text())['jobPostingInfo'];yes=req in frbsel
 frbdec.append({'control':req,'title':info['title'],'prepare':yes,'reason':'Related finance/quantitative/IT role; student eligibility unverified for internships' if yes else 'Outside target role families: legal, HR, communications, graphic/UX design, facilities/building or general administration'})
 if not yes:continue
 raw=plain(info['jobDescription']);jp={'@type':'JobPosting','normalization_note':'Derived from official Workday jobPostingInfo; unmodified source retained in frb/'+req+'.json','title':info['title'],'hiringOrganization':'Board of Governors of the Federal Reserve System','datePosted':info['startDate'],'validThrough':info.get('endDate'),'jobLocation':[{'address':{'addressLocality':'Washington','addressRegion':'DC'}}],'description':info['jobDescription'],'responsibilities':'','qualifications':info['jobDescription'],'educationRequirements':'See official minimum education and qualifications in description.'}
 (R/'announcements'/(req+'.json')).write_text(json.dumps(jp,indent=2));(R/'announcements'/(req+'.txt')).write_text(raw+'\n')
 native.append({'DocumentID':req,'PositionID':req,'Title':info['title'],'Agency':'Board of Governors of the Federal Reserve System','custom_url':info['externalUrl'],'HiringPath':[{'Code':'public','SearchDisplay':'See Board qualifications; internship enrollment requirements remain unverified'}],'SalaryDisplay':None,'LocationDisplay':'Washington, DC (Federal Reserve Board; team attendance policy needs verification)'})
 selected.append(req)
(R/'native-unique.json').write_text(json.dumps(native,indent=2));(R/'selected-controls.json').write_text(json.dumps(selected,indent=2));(R/'screening-new.json').write_text(json.dumps(decisions+frbdec,indent=2));(R/'review-cards.json').write_text('[]');print('Selected USAJOBS',len(selected)-len(frbsel),'FRB',len(frbsel),'total',len(selected))
