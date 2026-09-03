#!/usr/bin/env python3
"""Detecta clases usadas en el HTML que nunca se definieron en el CSS,
y variables var(--x) sin declarar. Corre esto antes de cada push."""
import re, sys
from pathlib import Path

f = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
s = f.read_text(encoding='utf-8')

css = '\n'.join(re.findall(r'<style>(.*?)</style>', s, re.S))
definidas = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
usadas = set()
for attr in re.findall(r'class="([^"]+)"', s):
    usadas.update(attr.split())

# clases con valor semantico: se ignoran utilidades de una letra
# se descartan los literales de plantilla de JS: ${x} no es una clase
huerfanas = sorted(c for c in usadas - definidas if len(c) > 2 and '${' not in c)

vars_def = set(re.findall(r'--([\w-]+)\s*:', css))
vars_uso = set(re.findall(r'var\(--([\w-]+)', s))
vars_huerfanas = sorted(vars_uso - vars_def)

fallo = False
if huerfanas:
    fallo = True
    print("CLASES SIN CSS (%d):" % len(huerfanas))
    for c in huerfanas:
        print("  .%s  — usada %d vez(ces)" % (c, s.count('"%s' % c) + s.count(' %s"' % c)))
if vars_huerfanas:
    fallo = True
    print("VARIABLES SIN DECLARAR (%d):" % len(vars_huerfanas))
    for v in vars_huerfanas:
        print("  --%s  — usada %d vez(ces)" % (v, s.count('var(--%s)' % v)))

if not fallo:
    print("OK · todas las clases y variables usadas están definidas")
sys.exit(1 if fallo else 0)
