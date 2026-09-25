"""Reject unexpected deployment files. This is a packaging gate, not anonymization."""
import hashlib
import json
from pathlib import Path

ALLOWED = {'index.html', 'style.css', 'app.mjs', 'geometry.mjs', 'site.mjs'}


def check(root):
    root = Path(root).resolve()
    files = list(root.rglob('*'))
    if any(p.is_symlink() for p in files):
        raise ValueError('Deployment must not contain symbolic links')
    actual = {p.relative_to(root).as_posix() for p in files if p.is_file()}
    if actual != ALLOWED:
        raise ValueError('Deployment file allowlist mismatch')
    size = sum((root / name).stat().st_size for name in actual)
    if size >= 150000:
        raise ValueError('Deployment exceeds size budget')
    return {'bytes': size, 'files': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                   for name in sorted(actual)}}


if __name__ == '__main__':
    print(json.dumps(check(Path(__file__).resolve().parents[1] / 'web'), indent=2))
