#!/usr/bin/env python3
"""Collect saved resume PDFs without changing originals or ledger state."""
import hashlib
import json
import shutil
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync():
    destination = ROOT / 'resumes'
    destination.mkdir(exist_ok=True)
    with sqlite3.connect(ROOT / 'tracking/jobs.sqlite3') as conn:
        jobs = [json.loads(row[0]) for row in conn.execute('SELECT data FROM jobs ORDER BY id')]
    entries, missing = [], []
    for job in jobs:
        current = job.get('artifacts', {}).get('resume_pdf', {})
        current_path = ROOT / current['path'] if current.get('path') else None
        folder = ROOT / job['application_directory'] if job.get('application_directory') else None
        sources = set(folder.rglob('resume-xuewu-cai__*.pdf')) if folder and folder.is_dir() else set()
        if current_path and current_path.is_file():
            sources.add(current_path)
        if not sources:
            missing.append({'id': job['id'], 'employer': job['employer'], 'title': job['title'], 'status': job['status'], 'reason': 'No saved resume PDF'})
        elif not current_path or not current_path.is_file():
            missing.append({'id': job['id'], 'employer': job['employer'], 'title': job['title'], 'status': job['status'], 'reason': 'Current resume PDF is not recorded or missing; historical files may exist'})
        for source in sorted(sources):
            source.relative_to(ROOT)
            digest = sha(source)
            is_current = current_path == source
            if is_current and current.get('sha256') and digest != current['sha256']:
                raise ValueError(f'Current resume hash differs from ledger: {source}')
            name = job['id'] + '__' + source.name
            if len(name.encode()) > 240:
                name = job['id'] + '__' + source.stem[:160] + '__' + hashlib.sha256(source.name.encode()).hexdigest()[:12] + '.pdf'
            copy = destination / name
            if copy.exists() and sha(copy) != digest:
                copy = destination / (job['id'] + '__' + source.stem[:160] + '__' + digest[:12] + '.pdf')
                if copy.exists() and sha(copy) != digest:
                    raise ValueError(f'Preserved library file conflicts with source hash: {copy}')
            if not copy.exists():
                shutil.copyfile(source, copy)
            if sha(copy) != digest:
                raise ValueError(f'PDF collection copy failed verification: {copy}')
            entries.append({'id': job['id'], 'employer': job['employer'], 'title': job['title'], 'status': job['status'], 'resume_status': job.get('resume_status'), 'version_label': 'current' if is_current else 'historical', 'source': str(source.relative_to(ROOT)), 'path': str(copy.relative_to(ROOT)), 'sha256': digest})
    entries.sort(key=lambda e: (e['employer'], e['title'], e['version_label'] != 'current', e['source']))
    manifest = {'entries': entries, 'missing': missing}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    def cell(value):
        return str(value or 'Not recorded').replace('|', '/').replace('\n', ' ')
    lines = ['# Customized resume PDF collection', '', 'Copies are SHA-256 verified against their per-job originals. **Current** is determined by the ledger; historical versions remain available. Preparation status is shown separately from version status.', '', '| Agency / position | Stable ID | Version | Preparation status | PDF | Original |', '|---|---|---|---|---|---|']
    for entry in entries:
        lines.append(f'| {cell(entry["employer"])} — {cell(entry["title"])} | `{entry["id"]}` | **{entry["version_label"]}** | {cell(entry["resume_status"] or entry["status"])} | [PDF]({Path(entry["path"]).name}) | [Original](../{entry["source"]}) |')
    lines += ['', f'{len(entries)} saved PDF version(s).', '', '## Missing or unrecorded current PDFs', '']
    lines += [f'- `{entry["id"]}` — {entry["employer"]}: {entry["title"]}. {entry["reason"]}; job status: {entry["status"]}.' for entry in missing] or ['None.']
    lines += ['', 'See [all unsubmitted jobs](../tracking/unsubmitted-jobs.md), [job queue](../tracking/job-queue.md) and [daily updates](../tracking/daily-updates/index.md).', '']
    (destination / 'index.md').write_text('\n'.join(lines))
    return manifest


if __name__ == '__main__':
    result = sync()
    print(f'Collected {len(result["entries"])} PDF versions; {len(result["missing"])} jobs have missing or unrecorded current PDFs.')
