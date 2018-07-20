#!/usr/bin/env python3
# coding: utf-8
import os
import json


def read_package_data(path):
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, path)
    with open(data_path) as f:
        return f.read()


data = read_package_data('rfc_list.json')
data = json.loads(data)
default_fields = ['text', 'status', 'note_with_text']


def search_rfc(query, limit):
    results = search_values(data, query, limit=limit)
    print(results)


def search_values(data, query, fields=None, limit=20):
    fields = fields or default_fields

    if len(query) <= 2:
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

            if v and query.lower() in v.lower():
                rv.append(item)
                break
    return rv


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default='http', help='query text to search')
    parser.add_argument(
        '-l', '--limit', type=int, default=20, help='limit count of results')
    args = parser.parse_args()

    search_rfc(args.query, args.limit)


if __name__ == '__main__':
    main()
