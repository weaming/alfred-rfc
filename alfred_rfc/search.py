#!/usr/bin/env python
# coding: utf-8
import sys
import os
import json
import argparse
from workflow import Workflow3
from workflow import ICON_WEB

default_fields = ['name', 'status', 'text', 'note_with_text']


def read_package_data(path):
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, path)
    with open(data_path) as f:
        return f.read()


data = read_package_data('rfc_list.json')
data = json.loads(data)


def search_rfc(query, limit):
    is_all = os.getenv('ALFRED_ALL')
    if is_all:
        return data

    results = search_values(data, query.split(' '), limit=limit)
    return results


def search_values(data, query_words, fields=None, limit=20):
    fields = fields or default_fields

    if len(query_words) == 1 and len(query_words[0]) <= 2:
        return []

    rv = []
    for item in data:
        # check limit
        if len(rv) >= limit:
            return rv

        text_list = []
        for k in item.keys():
            # check field
            if k not in fields:
                continue
            v = item[k]
            if v:
                text_list.append(v)

        text_full = ' '.join(text_list)
        if all(w.lower() in text_full.lower() for w in query_words):
            rv.append(item)

    return rv


def main_search_rfc(wf):
    if len(wf.args):
        query = wf.args[0]
    elif not all:
        return

    results = search_rfc(query, 1000)

    for i, r in enumerate(results, start=1):
        # see https://www.deanishe.net/alfred-workflow/api/index.html#workflow.Workflow.add_item
        out = dict(
            valid=True,
            title=r['name'],
            largetext=r['name'],
            subtitle='{} | {} ({})'.format(i, r['text'], r['status']),
            icon=ICON_WEB,
            uid=r['text'],
            quicklookurl=r['href'],
            arg=r['href'],
            copytext=r['href'],
        )

        wf.add_item(**out)

    # Send the results to Alfred as XML
    wf.send_feedback()


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='query text to search')
    parser.add_argument(
        '-l', '--limit', type=int, default=10, help='limit count of results')
    args = parser.parse_args()
    results = search_rfc(args.query, args.limit)

    print(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    if os.getenv('BY_ALFRED'):
        wf = Workflow3()
        sys.exit(wf.run(main_search_rfc))
    else:
        sys.exit(main_cli())


if __name__ == '__main__':
    main()
