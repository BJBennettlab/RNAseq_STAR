#!/usr/bin/env python3
"""Fetch a selected GENCODE mouse release, check published MD5, and record SHA-256."""
import argparse
import gzip
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path


def digest(path, algorithm='sha256'):
    with path.open('rb') as f:
        return hashlib.file_digest(f, algorithm).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--release',required=True)
    p.add_argument('--rrna',type=Path,required=True)
    a=p.parse_args(); a.directory.mkdir(parents=True,exist_ok=True)
    base=f'https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_{a.release}'
    manifest=urllib.request.urlopen(base+'/MD5SUMS',timeout=60).read().decode('ascii')
    md5={line.split()[1].lstrip('*'):line.split()[0] for line in manifest.splitlines() if len(line.split())==2}
    report=a.directory/'reference_manifest.json'
    old=json.loads(report.read_text()) if report.exists() else {}
    recorded=old.get('files',{}) if old.get('release')==a.release else {}
    outputs={}
    for name in ['GRCm39.primary_assembly.genome.fa',f'gencode.v{a.release}.annotation.gtf']:
        dest=a.directory/name; expected=md5[name+'.gz']
        previous=recorded.get(name,{})
        if dest.exists():
            if previous.get('source_md5')!=expected or previous.get('sha256')!=digest(dest):
                raise ValueError(f'Existing reference lacks matching provenance: {dest}')
        else:
            part=dest.with_name(name+'.download.part');unpacked=dest.with_name(name+'.unpacked.part')
            with urllib.request.urlopen(base+'/'+name+'.gz',timeout=120) as src, part.open('wb') as dst:
                shutil.copyfileobj(src,dst,8*1024*1024)
            if digest(part,'md5')!=expected:
                raise ValueError(f'Published MD5 mismatch: {name}')
            with gzip.open(part,'rb') as src, unpacked.open('wb') as dst:
                shutil.copyfileobj(src,dst,8*1024*1024)
            unpacked.replace(dest);part.unlink()
        outputs[name]={'source_url':base+'/'+name+'.gz','source_md5':expected,'sha256':digest(dest),'bytes':dest.stat().st_size}
        report.write_text(json.dumps({'assembly':'GRCm39','release':a.release,'files':{**recorded, **outputs}},indent=2)+'\n')
    rrna=a.directory/'mouse_rrna.fasta'
    if rrna.exists() and digest(rrna)!=digest(a.rrna):
        raise ValueError('Existing rRNA reference differs from the repository copy')
    if not rrna.exists():shutil.copyfile(a.rrna,rrna)
    outputs[rrna.name]={'source':'repository References/mouse_rrna.fasta','sha256':digest(rrna),'bytes':rrna.stat().st_size}
    report.write_text(json.dumps({'assembly':'GRCm39','release':a.release,'files':outputs},indent=2)+'\n')
    (a.directory/'GENCODE_MD5SUMS.txt').write_text(manifest)
    print('References verified:',report)


if __name__=='__main__':main()
