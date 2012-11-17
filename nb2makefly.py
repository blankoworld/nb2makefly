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
extension = '.md'

def accentued_char_replacement(string):
    """
    This replaces some special chars in string by non accentued chars.
    """
    xlate = {
        0xc0:'A', 0xc1:'A', 0xc2:'A', 0xc3:'A', 0xc4:'A', 0xc5:'A',
        0xc6:'Ae', 0xc7:'C',
        0xc8:'E', 0xc9:'E', 0xca:'E', 0xcb:'E',
        0xcc:'I', 0xcd:'I', 0xce:'I', 0xcf:'I',
        0xd0:'Th', 0xd1:'N',
        0xd2:'O', 0xd3:'O', 0xd4:'O', 0xd5:'O', 0xd6:'O', 0xd8:'O',
        0xd9:'U', 0xda:'U', 0xdb:'U', 0xdc:'U',
        0xdd:'Y', 0xde:'th', 0xdf:'ss',
        0xe0:'a', 0xe1:'a', 0xe2:'a', 0xe3:'a', 0xe4:'a', 0xe5:'a',
        0xe6:'ae', 0xe7:'c',
        0xe8:'e', 0xe9:'e', 0xea:'e', 0xeb:'e',
        0xec:'i', 0xed:'i', 0xee:'i', 0xef:'i',
        0xf0:'th', 0xf1:'n',
        0xf2:'o', 0xf3:'o', 0xf4:'o', 0xf5:'o', 0xf6:'o', 0xf8:'o',
        0xf9:'u', 0xfa:'u', 0xfb:'u', 0xfc:'u',
        0xfd:'y', 0xfe:'th', 0xff:'y',
        0xa1:'!', 0xa2:'{cent}', 0xa3:'{pound}', 0xa4:'{currency}',
        0xa5:'{yen}', 0xa6:'|', 0xa7:'{section}', 0xa8:'{umlaut}',
        0xa9:'{C}', 0xaa:'{^a}', 0xab:'<<', 0xac:'{not}',
        0xad:'-', 0xae:'{R}', 0xaf:'_', 0xb0:'{degrees}',
        0xb1:'{+/-}', 0xb2:'{^2}', 0xb3:'{^3}', 0xb4:"'",
        0xb5:'{micro}', 0xb6:'{paragraph}', 0xb7:'*', 0xb8:'{cedilla}',
        0xb9:'{^1}', 0xba:'{^o}', 0xbb:'>>',
        0xbc:'{1/4}', 0xbd:'{1/2}', 0xbe:'{3/4}', 0xbf:'?',
        0xd7:'*', 0xf7:'/'
    }
    r = ''
    for i in string:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += i
    return r

def replace_all(text, dic):
    """
    Replace chars from given dic
    """
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def format_string(string):
    """
    Format string as wanted for makefly
    """
    dic = {
        ' ': '_', 
        '?': '_',
        '!': '_',
        }
    res = string
    # delete special chars
    string_wo_acc = accentued_char_replacement(string)
    # replace some chars by a '_'
    string_replaced = replace_all(string_wo_acc, dic)
    # delete double '__'
    string_double_deleted = string_replaced.replace('__', '_')
    # search if '_' is at begin or at end
    regex = re.match('^_?(.*)_?$', string_double_deleted)
    if regex:
        res = regex.group(1)
    else:
        res = string_double_deleted
    # return res in lowercase
    return res.lower()

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
    #print title, description, date, timestamp, post_format, author

## NOTE FOR FORMAT:
# autobr : change all \n in <br/>
# raw : HTML file. So markdown use it as is.
# markdown : use it as is because Makefly use markdown ;)

## NOTES
# - remember that there is some IMG file. So we should copy them. => how to discover this?
#+ Perhaps it should be better to note "warning" there is a file to copy into static directory
# - If an error: display a message and go to next post
# - How to fetch categories and links with post in nanoblogger?

    # Metachars replacement
    new_title = format_string(title)
    # Some changes
    targetfile = new_title or None
    if not targetfile:
        print "Error: No targetfile!"
        return 1

    # Write result
    try:
        t = open('%s%s' % (targetfile, extension), 'w')
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
