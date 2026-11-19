#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
import argparse
import json
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree

INDEX_URL = 'https://www.rfc-editor.org/rfc-index.xml'
NAMESPACE = {'rfc': 'https://www.rfc-editor.org/rfc-index'}
INDEX_PATH = Path(__file__).resolve().parent / 'rfc_list.json'


def parse_index(source):
    records = []
    for entry in ElementTree.parse(source).getroot().findall('rfc:rfc-entry', NAMESPACE):
        doc_id = entry.findtext('rfc:doc-id', namespaces=NAMESPACE)
        title = entry.findtext('rfc:title', namespaces=NAMESPACE)
        if not doc_id or not title:
            continue

        number = int(doc_id.removeprefix('RFC'))
        abstract = entry.find('rfc:abstract', NAMESPACE)
        note = ' '.join(' '.join(abstract.itertext()).split()) if abstract is not None else ''
        records.append(
            (
                number,
                {
                    'text': f'RFC{number}',
                    'name': title,
                    'status': entry.findtext('rfc:current-status', 'UNKNOWN', NAMESPACE),
                    'note_with_text': note,
                    'href': f'https://www.rfc-editor.org/rfc/rfc{number}.html',
                },
            )
        )

    if not records:
        raise ValueError('RFC Editor index contains no RFC entries')
    return [record for _, record in sorted(records, key=lambda pair: pair[0])]


def main():
    parser = argparse.ArgumentParser(description='Refresh the bundled RFC Editor index.')
    parser.add_argument('xml', nargs='?', type=Path, help='local RFC Editor XML index')
    args = parser.parse_args()
    with args.xml.open('rb') if args.xml else urlopen(INDEX_URL, timeout=30) as source:
        records = parse_index(source)

    lines = ',\n'.join(json.dumps(record, ensure_ascii=False) for record in records)
    INDEX_PATH.write_text(f'[\n{lines}\n]\n', encoding='utf-8')
    print(f'Indexed {len(records)} RFCs')


if __name__ == '__main__':
    main()
