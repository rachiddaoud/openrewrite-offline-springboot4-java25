#!/usr/bin/env python3
"""Fusion additive : aucun fichier existant n'est remplace."""
import argparse, hashlib, zipfile
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--destination',type=Path,default=Path.home()/'.m2'/'repository')
a=parser.parse_args();dest=a.destination.expanduser().resolve()
archive=Path(__file__).resolve().with_name('rewrite-repo.zip')
added=same=0;conflicts=[]
with zipfile.ZipFile(archive) as z:
 for item in z.infolist():
  path=(dest/item.filename).resolve()
  if not path.is_relative_to(dest):raise ValueError('Chemin ZIP invalide')
  if item.is_dir():continue
  data=z.read(item)
  if path.exists():
   if path.read_bytes()==data:same+=1
   else:conflicts.append(item.filename)
   continue
  path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('xb') as f:f.write(data)
  added+=1
print(f'{added} fichiers ajoutes, {same} identiques, {len(conflicts)} existants differents conserves.')
if conflicts:
 print('Pour reproduire exactement les tests, importer dans un dossier vide et utiliser -Dmaven.repo.local. Fichiers conserves :')
 print('\n'.join(conflicts))
