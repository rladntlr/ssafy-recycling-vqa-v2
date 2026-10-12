"""Validate only publishable sources; never print matched secret contents."""
import ast
import json
import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
errors=[]
count=0
patterns=[r'hf_[A-Za-z0-9]{20,}', r'gh[pousr]_[A-Za-z0-9]{20,}',
          r'(?i)(?:password|hf_token)\s*=\s*[\"\x27][^\"\x27\n]{4,}[\"\x27]']
for p in (root/'notebooks').glob('*.ipynb'):
    n=json.loads(p.read_text(encoding='utf-8'))
    for i,c in enumerate(n['cells']):
        s=''.join(c['source'])
        if c['cell_type']=='code':
            try: ast.parse(s)
            except SyntaxError: errors.append(f'{p.name}: cell {i}: syntax')
            if c.get('outputs') or c.get('execution_count') is not None:
                errors.append(f'{p.name}: cell {i}: saved output')
        if any(re.search(pattern,s) for pattern in patterns):
            errors.append(f'{p.name}: cell {i}: credential-like literal')
    count+=1
for p in (root/'scripts').glob('*.py'):
    s=p.read_text(encoding='utf-8'); ast.parse(s)
    if any(re.search(pattern,s) for pattern in patterns): errors.append(f'{p.name}: credential-like literal')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {count} notebooks; syntax, cleared outputs, credential patterns; scripts syntax')
