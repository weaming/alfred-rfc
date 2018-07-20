#!/usr/bin/env python3
# coding: utf-8
"""
Author       : weaming
Created Time : 2018-07-20 10:36:02

Get list from partial html text from https://tools.ietf.org/rfc/
"""
import re
import sys
import json
from pprint import pprint


def read_lines(path):
    text = open(path).read().strip()
    lines = text.split('\n\n')
    return [
        l.strip().replace('\n', ' ').replace('   ', ' ').replace('  ', ' ')
        for l in lines
    ]


def get_rfc_json():
    lines = read_lines('rfc_list.html')
    return [process_line(l, n) for n, l in enumerate(lines, start=1)]


def get_link_pattern(link_href_name, link_text_name):
    return r'(<a href="(?P<{}>.+?)">(?P<{}>.+?)</a>)'.format(
        link_href_name, link_text_name)


line_pattern = r'<a href="(?P<href>.+?)">(?P<text>.+?)</a> (?P<note>.+?)( \(?P<updates>Update[(s)|(d by)] (.+?)\))?( \(Status: (?P<status>.+?)\) \(DOI: (?P<doi>.+?)\))?$'
line_prog = re.compile(line_pattern)

note_pattern = get_link_pattern('href', 'text')
note_prog = re.compile(note_pattern)

def process_line(line, n):
    link = line.split('</a>', 1)[0]
    matched = line_prog.match(line)
    if not matched:
        print(line)
        sys.exit(1)

    matched_dict = matched.groupdict()
    for x in ['updates', 'note']:
        if x in matched_dict:
            note_text = matched_dict[x]
            replaced_text = note_prog.sub(r'\2', note_text)
            matched_dict['{}_with_url'.format(x)] = replaced_text

            replaced_text = note_prog.sub(r'\3', note_text)
            matched_dict['{}_with_text'.format(x)] = replaced_text
    return matched_dict


def main():
    js = get_rfc_json()
    # pprint(js)
    with open('rfc_list.json', 'w') as out:
        out.write(json.dumps(js, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
