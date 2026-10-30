"""Validate source data and cross-check both accepted solutions."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
files = sorted((root / 'data').rglob('*.in'))
for path in files:
    lines = path.read_text(encoding='utf-8').splitlines()
    count = int(lines[0])
    words = lines[1:]
    assert 1 <= count <= 50 and count == len(words)
    assert all(1 <= len(s) <= 50 and s.isascii() and s.isalpha() for s in words)
    expected = path.with_suffix('.out').read_text(encoding='utf-8').split()
    cpp = subprocess.check_output([str(root/'solution.exe')], input=path.read_bytes()).decode().split()
    python = subprocess.check_output([sys.executable, str(root/'solution2.py')], input=path.read_bytes()).decode().split()
    assert expected == cpp == python, path
print(f'Validated {len(files)} files')
