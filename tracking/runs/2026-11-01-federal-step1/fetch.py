import urllib.request,json,sys,re,datetime,subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('p','div','li','h1','h2','h3','br','dt','dd'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
for item in json.loads(Path(sys.argv[1]).read_text()):
 try:
  raw=subprocess.check_output(['curl','-fLsS','--max-time','30',item['url']],text=True);status=200
  (ROOT/(item['name']+'.html')).write_text(raw)
  p=Text();p.feed(raw);txt=re.sub(r'[ \t]+',' ',''.join(p.parts));txt=re.sub(r'\n\s*\n','\n',txt)
  (ROOT/(item['name']+'.txt')).write_text(txt)
  result={**item,'status':status,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'characters':len(raw)}
 except Exception as e:result={**item,'error':str(e)}
 with (ROOT/'fetch-audit.jsonl').open('a') as f:f.write(json.dumps(result)+'\n')
 print(json.dumps(result))
