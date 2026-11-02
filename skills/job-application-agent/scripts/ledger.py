#!/usr/bin/env python3
"""Persistent local ledger; run from workspace root. Does not submit applications."""
import argparse, datetime, hashlib, json, re, sqlite3
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

STATES = {'discovered','needs_verification','eligible','skipped','draft','awaiting_confirmation','approved','submitting','submission_unknown','applied','closed','rejected','withdrawn'}
def normalized(s):
    return re.sub(r'\s+', ' ', s.strip().casefold())
def canonical(url):
    u = urlsplit(url.strip())
    if u.scheme not in {'http','https'} or not u.netloc:
        raise ValueError('Expected an absolute HTTP(S) job URL')
    params = [(k,v) for k,v in parse_qsl(u.query, keep_blank_values=True)
              if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid','ref','source','trk'}]
    return urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path.rstrip('/'),urlencode(sorted(params)),''))
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, identity TEXT UNIQUE NOT NULL, data TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS events (time TEXT NOT NULL, job_id TEXT NOT NULL, data TEXT NOT NULL)')
    return c

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',default='tracking/jobs.sqlite3')
    s=p.add_subparsers(dest='command',required=True)
    s.add_parser('list')
    a=s.add_parser('add'); a.add_argument('file')
    a=s.add_parser('update'); a.add_argument('id'); a.add_argument('file')
    args=p.parse_args()
    with connect(args.db) as c:
        if args.command=='list':
            print(json.dumps([json.loads(r[0]) for r in c.execute('SELECT data FROM jobs ORDER BY id')],indent=2)); return
        d=json.loads(Path(args.file).read_text())
        if not isinstance(d,dict): raise ValueError('Input must be an object')
        if args.command=='add':
            for k in ('employer','title','canonical_url'):
                if not d.get(k): raise ValueError('Missing '+k)
            d['canonical_url']=canonical(d['canonical_url'])
            identity=normalized(d['employer'])+'|'+('req:'+normalized(str(d['requisition_id'])) if d.get('requisition_id') else 'url:'+d['canonical_url'])
            # Also catch matching URLs when one source omitted the requisition ID.
            for old_id,old_identity,raw in c.execute('SELECT id,identity,data FROM jobs'):
                old=json.loads(raw)
                urls=[old['canonical_url']]+old.get('aliases',[])
                if identity==old_identity or d['canonical_url'] in [canonical(x) for x in urls]:
                    print(json.dumps({'id':old_id,'duplicate':True,'status':old['status']})); return
            key=hashlib.sha256(identity.encode()).hexdigest()[:16]
            d.update(id=key,created_at=now(),updated_at=now())
            d.setdefault('status','discovered')
            if d['status'] not in STATES: raise ValueError('Invalid status')
            if d['status']!='discovered': raise ValueError('New jobs must start as discovered')
            c.execute('INSERT INTO jobs VALUES (?,?,?)',(key,identity,json.dumps(d)))
        else:
            r=c.execute('SELECT data FROM jobs WHERE id=?',(args.id,)).fetchone()
            if not r: raise ValueError('Unknown job ID')
            old=json.loads(r[0]); key=args.id
            if {'id','employer','requisition_id','canonical_url','created_at'} & d.keys():
                raise ValueError('Identity fields are immutable; reconcile aliases instead')
            if d.get('status',old['status']) not in STATES: raise ValueError('Invalid status')
            if old['status'] in {'submitting','submission_unknown','applied','rejected','withdrawn'} and d.get('status',old['status']) not in {'submitting','submission_unknown','applied','rejected','withdrawn'}:
                raise ValueError('Cannot reset a submission record to the preparation queue')
            merged={**old,**d,'updated_at':now()}
            status=merged['status']
            if status in {'approved','submitting'}:
                if not all(merged.get(k) for k in ('approval_reference','approved_packet_sha256','packet_sha256')):
                    raise ValueError('Approval evidence and packet hashes required')
                if merged['packet_sha256']!=merged['approved_packet_sha256']:
                    raise ValueError('Approval is invalid for the current packet')
            if status=='submitting' and old['status']!='approved':
                raise ValueError('Submission requires approved state; uncertain attempts must be reconciled')
            if status=='applied' and not all(merged.get(k) for k in ('receipt_evidence','submitted_at','approval_reference','approved_packet_sha256')):
                raise ValueError('Submission evidence and approval reference required')
            d=merged
            c.execute('UPDATE jobs SET data=? WHERE id=?',(json.dumps(d),key))
        c.execute('INSERT INTO events VALUES (?,?,?)',(now(),key,json.dumps(d)))
        print(json.dumps({'id':key,'duplicate':False,'status':d['status']}))

if __name__=='__main__':
    main()
