#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nb2makefly.py
#
# Permit to migrate from Nanoblogger to Makefly

#####
## LICENSE
###

# Makefly, a static weblog engine using a BSD Makefile
# Copyright (C) 2012 DOSSMANN Olivier
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#####
## LIBRARIES
###
import sys
import re

#####
## VARIABLES
###
nanoblogger_conf = 'nb.conf'
sourcefile = 'test_01_raw.txt'
chars = {
    'é': 'e',
    'è': 'e',
    ' ': '_',
    ',': '_',
    ':': '_',
    '__': '_',
}

def main():
    """
    Extract data from 'sourcefile' and create 'targetfile' with all data:
    - title
    - description
    - creation date
    - etc.
    """
    # Open source file
    try:
        f = open(sourcefile, 'rb')
    except IOError, e:
        print(e)
        return 1
    try:
        text = f.read()
    except ValueError, e:
        print(e)
        return 1
    finally:
        f.close()

    # Some var
    content = ""
    meta = False
    title = ""
    description = ""
    date = ""
    timestamp = False
    # Parse source file content
    data = text.split("-----\n")
    content = data[1] or ""
    meta = data[0] and data[0].split("\n") or False
    # content data
    if content.startswith("BODY:"):
        content = content[5:]
    if content.endswith("END"):
        content = content[:-3]
    # meta data
    for element in meta:
        if element.startswith("TITLE:"):
            title = element[6:]
            continue
        if element.startswith("DESC:"):
            description = element[5:]
            continue
        if element.startswith("DATE:"):
            date = element[5:]
            continue
        if element.startswith("TIMESTAMP:"):
            timestamp = element[10:]
            continue
        if element.startswith("FORMAT:"):
            post_format = element[7:]
            continue
        if element.startswith("AUTHOR:"):
            author = element[7:]
            continue
        print("%s\n\tUnknown metadata: %s" % (sourcefile, element))
    # Mandatory metadata
    if not title:
        print("%s\n\tNo TITLE found!" % (sourcefile))
        return 1
    # Print result
    print title, description, date, timestamp, post_format, author

## NOTE FOR FORMAT:
# autobr : change all \n in <br/>
# raw : HTML file. So markdown use it as is.
# markdown : use it as is because Makefly use markdown ;)

## NOTES
# - remember that there is some IMG file. So we should copy them. => how to discover this?
#+ Perhaps it should be better to note "warning" there is a file to copy into static directory
# - If an error: display a message and go to next post
# - How to fetch categories and links with post in nanoblogger?

    # Prepare target file
    targetfile = title
    # Poor metachars replacement
    for el in chars:
        print el
        if el in targetfile:
            print targetfile, chars[el]
            targetfile = targetfile.replace(el, chars[el])

    print("title result: %s" % (targetfile))
    print re.escape(title)
    return 1

    # Write result
    try:
        t = open(targetfile, 'w')
    except IOError, e:
        print(e)
        return 1
    try:
        t.write(content)
    except ValueError, e:
        print(e)
        return 1
    finally:
        t.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
