from pathlib import Path
import hashlib,importlib.util,json,re
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('b','skills/job-application-agent/scripts/build_step1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.freddie[0]=b.freddie[0].replace('CRT program','CRT (Credit Risk Transfer) program');expected=b.freddie+b.research+b.quant+b.senior+b.aquilent;norm=lambda s:re.sub(r'\s+',' ',s).strip();checks=[]
for o in json.loads((R/'outcomes.json').read_text()):
 p=Path(o['artifacts']['resume_pdf']['path']);d=PdfReader(p);assert len(d.pages)==2;text='\n'.join(x.extract_text() for x in d.pages)
 for bullet in expected:assert norm(bullet) in norm(text),(o['id'],bullet)
 assert d.metadata.title=='Xuewu Cai — Resume';assert not re.search('tailored for|targeted for|customized for|AI-generated|AI-assisted|AI-updated',text,re.I);assert 'Director, Financial Engineering/Inv&Capital Market' in text
 bounds=[]
 for page in d.pages:
  def visitor(t,cm,tm,font,size):
   if t.strip():bounds.append((tm[4]*cm[0]+tm[5]*cm[2]+cm[4],tm[4]*cm[1]+tm[5]*cm[3]+cm[5]))
  page.extract_text(visitor_text=visitor)
 assert all(20<=x<=590 and 15<=y<=780 for x,y in bounds),o['id']
 for a in o['artifacts'].values():assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
 checks.append({'id':o['id'],'pages':2,'baseline_bullets':20,'bounds_valid':True,'text_metadata_hashes_valid':True})
unique={}
for p in R.glob('*__page*.png'):unique.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),p)
images=list(unique.values());boards=[]
for k in range(0,len(images),12):
 subset=images[k:k+12];canvas=Image.new('RGB',(1836,2460),'#ddd');draw=ImageDraw.Draw(canvas)
 for i,p in enumerate(subset):
  img=Image.open(p).convert('RGB');img.thumbnail((600,780));x=(i%3)*612;y=(i//3)*615;img.thumbnail((450,582));x+=80;canvas.paste(img,(x,y+22));draw.text(((i%3)*612+5,y+5),p.stem[-70:],fill='black')
 out=R/('review-board-'+str(k//12+1)+'.jpg');canvas.save(out,quality=92);boards.append(str(out))
(R/'new-validation.json').write_text(json.dumps({'resumes':checks,'unique_rendered_images':len(images),'boards':boards},indent=2));print('Validated',len(checks),'PDFs; unique images',len(images),'boards',len(boards))
