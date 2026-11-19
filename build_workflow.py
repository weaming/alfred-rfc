#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent


def main():
    sources = {
        'info.plist': ROOT / 'workflow/info.plist',
        'icon.png': ROOT / 'workflow/icon.png',
        'search.py': ROOT / 'alfred_rfc/search.py',
        'rfc_list.json': ROOT / 'rfc_list.json',
    }
    with ZipFile(ROOT / 'SearchRFCs.alfredworkflow', 'w', compression=ZIP_DEFLATED) as archive:
        for name, source in sources.items():
            archive.write(source, name)


if __name__ == '__main__':
    main()
