#!/usr/bin/env python

r"""Command-line tool to pretty-print JSON

Usage::

    $ curl -s http://localhost:8082/api/ldap | json_tool.py

This is a substitute for python's own json.tool which fails when headers are part of
the curl output (curl -i). 

By default, "links" field will be recursively removed from JSON. 
set JT_REMOVE_LINKS to "" in order to keep the field. 

"""

import os
import sys
import json

def remove_links(obj):
    if type(obj) is dict:
        if obj.has_key("links"):
            del obj["links"]

        for k, v in obj.iteritems():
            remove_links(v)

        return

    if type(obj) is list:
        for item in obj:
            remove_links(item)

        return

    return

def main():
    data = sys.stdin.read()

    body_start = data.find('\r\n\r\n')
    if body_start == -1:
        print data
        return

    headers = data[0:body_start]
    print(headers)
    print

    body_start += 4
    body = data[body_start:].strip()
    if not body:
        return

    if "text/html" in headers:
        print body
        return

    obj = json.loads(body)
    if os.environ.get("JT_REMOVE_LINKS", True):
        remove_links(obj)

    with sys.stdout as outfile:
        json.dump(obj, outfile, sort_keys=True, indent=4)
        outfile.write('\n')

if __name__ == '__main__':
    main()


