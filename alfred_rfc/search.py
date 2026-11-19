import argparse
import json
import os
import re
from pathlib import Path

INDEX_PATH = Path(__file__).with_name('rfc_list.json')
SEARCH_FIELDS = ('name', 'status', 'text', 'note_with_text')


def search_rfc(query, limit):
    query = query.strip().casefold()
    show_all = bool(os.getenv('ALFRED_ALL'))
    if not show_all and (not query or limit <= 0):
        return []

    records = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    if show_all:
        return records

    number = re.fullmatch(r'(?:rfc\s*)?0*(\d+)', query)
    if number:
        identifier = f'RFC{number[1]}'
        return [record for record in records if record['text'] == identifier]

    if len(query) < 3:
        return []

    words = query.split()
    matches = []
    for record in reversed(records):
        contents = ' '.join(record[field] or '' for field in SEARCH_FIELDS).casefold()
        if all(word in contents for word in words):
            matches.append(record)
            if len(matches) == limit:
                break
    return matches


def alfred_item(record):
    url = record['href']
    return {
        'uid': record['text'],
        'title': record['name'],
        'subtitle': f'{record["text"]} · {record["status"]}',
        'arg': url,
        'quicklookurl': url,
        'text': {'copy': url, 'largetype': record['name']},
    }


def main():
    parser = argparse.ArgumentParser(description='Search the RFC Editor index.')
    parser.add_argument('--alfred', action='store_true', default=bool(os.getenv('BY_ALFRED')))
    parser.add_argument('-l', '--limit', type=int)
    parser.add_argument('query', nargs='?', default='')
    args = parser.parse_args()

    limit = args.limit if args.limit is not None else (50 if args.alfred else 10)
    results = search_rfc(args.query, limit)
    output = {'items': [alfred_item(record) for record in results]} if args.alfred else results
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
