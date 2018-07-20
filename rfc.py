#!/usr/bin/env python3
# coding: utf-8
"""
Author       : weaming
Created Time : 2018-07-20 10:36:02

Get list from partial html text from https://tools.ietf.org/rfc/
"""
import re
import sys
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
    return [process_line(l) for l in lines]


def get_link_pattern(prefix, link_href_name, link_text_name):
    return r'\({} (<a href="(?P<{}>.+?)">(?P<{}>.+?)</a>(, )?)+\)'.format(
        prefix, link_href_name, link_text_name)


line_pattern = r'<a href="(?P<href>.+?)">(?P<text>.+?)</a> (?P<note>.+?)( \(Status: (?P<status>.+?)\) (?P<doi>.+?))?$'
line_prog = re.compile(line_pattern)

note_pattern = r'(.+?)( {})?( {})? (.+?)$'.format(
    get_link_pattern('Obsoletes', 'obsoletes_href', 'obsoletes_text'),
    get_link_pattern('Updated by', 'updated_by_href', 'updated_by_text'),
)
note_prog = re.compile(note_pattern)


def process_line(line):
    link = line.split('</a>', 1)[0]
    matched = line_prog.match(line)
    if not matched:
        print(line)
        sys.exit(1)

    matched_dict = matched.groupdict()
    if 'note' in matched_dict:
        note_text = matched_dict['note']
        note_matched = note_prog.match(note_text)
        if not note_matched:
            print(note_pattern)
            print(note_text)
            sys.exit(1)

        note_matched_dict = note_matched.groupdict()
        if ('Updaetd' in note_text or 'Obsoletes' in note_text) and all(
                x is None for x in note_matched_dict.values()):
            print(note_pattern)
            print(note_text)
            sys.exit(1)

        matched_dict['note'] = note_matched_dict
    return matched_dict


def main():
    js = get_rfc_json()
    pprint(js)


if __name__ == '__main__':
    main()
