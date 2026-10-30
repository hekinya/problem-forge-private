"""Export verified source data as a Hydro package."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

root = Path(__file__).resolve().parent
pid = 'ZXS2026B'
target = root / 'hydro' / f'B-{pid}'
assert not target.exists(), target
(target / 'additional_file').mkdir(parents=True)
(target / 'testdata').mkdir()
(target / 'problem.yaml').write_text(
    f'pid: {pid}\nowner: 1\ntitle: Yes-Yes?\ntag: []\nnSubmit: 0\nnAccept: 0\n', encoding='utf-8')
(target / 'problem_zh.md').write_text('![题面第 1 页](file://statement-01.png)\n', encoding='utf-8')
shutil.copy2(root/'statement-01.png', target/'additional_file/statement-01.png')
cases = []
for folder, prefix in [('samples','sample'), ('tests','case')]:
    for src in sorted((root/'data'/folder).glob('*.in')):
        stem = prefix + src.stem
        answer = src.with_suffix('.out')
        assert answer.is_file()
        shutil.copy2(src, target/'testdata'/f'{stem}.in')
        shutil.copy2(answer, target/'testdata'/f'{stem}.ans')
        cases.append(stem)
config = 'type: default\nchecker_type: default\ntime: 1s\nmemory: 256m\ncases:\n'
for stem in cases:
    config += f'  - input: {stem}.in\n    output: {stem}.ans\n'
(target/'testdata/config.yaml').write_text(config, encoding='utf-8')
archive = root/'hydro'/f'B-{pid}.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for file in sorted(target.rglob('*')):
        if file.is_file(): z.write(file, Path(target.name)/file.relative_to(target))
print(archive)
