#!/usr/bin/env python3
# coding: utf-8

def search_rfc(query):
    pass

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default='http', help='query text to search')
    args = parser.parse_args()

    search_rfc(args.query)


if __name__ == '__main__':
	main()
