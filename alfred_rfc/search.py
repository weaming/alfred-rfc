#!/usr/bin/env python
# coding: utf-8
import sys
import os
import json
import argparse
from workflow import Workflow3
from workflow import ICON_WEB

default_fields = ['text', 'status', 'note_with_text', 'name']


def read_package_data(path):
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, path)
    with open(data_path) as f:
        return f.read()


data = read_package_data('rfc_list.json')
data = json.loads(data)


def search_rfc(query, limit):
    results = search_values(data, query.split(' '), limit=limit)
    return results


def search_values(data, query_words, fields=None, limit=20):
    fields = fields or default_fields

    if len(query_words) == 1 and len(query_words[0]) <= 2:
        return []

    rv = []
    for item in data:
        for k in item.keys():
            # check limit
            if len(rv) >= limit:
                return rv

            # check field
            if k not in fields:
                continue
            v = item[k]

            if v and all(w.lower() in v.lower() for w in query_words):
                rv.append(item)
                break
    return rv


def main_search_rfc(wf, all=False):
    if len(wf.args):
        query = wf.args[0]
    elif not all:
        return

    if all:
        results = data
    else:
        results = search_rfc(query, 30)

    for r in results:
        # see https://www.deanishe.net/alfred-workflow/api/index.html#workflow.Workflow.add_item
        out = dict(
            valid=True,
            title=r['name'],
            subtitle='{} ({})'.format(r['text'], r['status']),
            icon=ICON_WEB,
            uid=r['text'],
            quicklookurl=r['href'],
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
        is_all = os.getenv('ALFRED_ALL')
        sys.exit(wf.run(main_search_rfc, all=is_all))
    else:
        sys.exit(main_cli())


if __name__ == '__main__':
    main()
