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
import os
import sys
import re
import datetime

#####
## VARIABLES
###
limit = 0
# Nanoblogger
nanoblogger_conf = 'nb.conf'
datadir = 'data'
data_ext = '.txt'
cat_ext = '.db'
# Makefly
extension = '.md'
db_ext = '.mk'
default_type = 'news'
default_tag = 'old_nanoblogger'
targetdir = 'src'
dbtargetdir = 'db'

def listdir(directory, ext):
    """
    Return directory listing
    """
    res = []
    dirList=os.listdir(directory)
    for fname in dirList:
        if fname.endswith(ext):
            res.append(fname)
    return res

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
        if ord(i) in xlate:
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
    for el in dic:
        text = text.replace(el, dic[el])
    return text

def format_string(string):
    """
    Format string as wanted for makefly
    """
    dic = {
        ' ' : '_', 
        '?' : '_',
        '!' : '_',
        ':' : '_',
        '{' : '_',
        '}' : '_',
        '/' : '_',
        '\\': '_',
        ',' : '_',
        ';' : '_',
        '(' : '_',
        ')' : '_',
        '\'': '_',
        '<' : '_',
        '>' : '_',
        '|' : '_',
        }
    res = string
    # delete special chars
    string_wo_acc = accentued_char_replacement(string)
    # replace some chars by a '_'
    string_replaced = replace_all(string_wo_acc, dic)
    # delete double '__'
    while '__' in string_replaced:
        string_replaced = string_replaced.replace('__', '_')
    string_double_deleted = string_replaced
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
    # Search DATE_FORMAT in nanoblogger conf
    date_format = False
    with open(nanoblogger_conf, 'r') as conf:
        for line in conf:
            regex_conf = re.match('^DATE_FORMAT=[\'"](.*)[\'"]$', line)
            if regex_conf:
                date_format = regex_conf.group(1)
    if not date_format:
        print("Error: no date format found in Nanoblogger configuration!")
        return 1

    # List data directory
    posts = listdir(datadir, data_ext)
    if not posts:
        print("Warning: no posts found in this directory: %s!" % datadir)

    for num, postfile in enumerate(posts):
        if limit and num >= limit:
            print "STOP."
            return 1
        path = datadir + '/' + postfile
        # Open source file
        try:
            f = open(path, 'rb')
        except IOError as e:
            print(e)
            continue
        try:
            text = f.read()
        except ValueError as e:
            print(e)
            continue
        finally:
            f.close()

        # INFO
        print('INFO: %s' % postfile)
        # Some var
        content = ""
        meta = False
        title = ""
        description = ""
        date = ""
        timestamp = False
        # Parse source file content
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        data = text.split("-----\n")
        if len(data) > 1:
            content = data[1]
        try:
            meta = data[0] and str(data[0].encode('utf-8')).split("\n") or False
        except UnicodeEncodeError as e:
            print('Encode/decode error: "%s"' % e)
        # content data
        if content.startswith("BODY:"):
            content = content[5:]
        if content.endswith("END"):
            content = content[:-3]
        # meta data
        for element in meta:
            if element.startswith("TITLE:"):
                title = element[6:].strip().decode('utf-8')
                continue
            if element.startswith("DESC:"):
                description = element[5:].strip().decode('utf-8')
                continue
            if element.startswith("DATE:"):
                date = element[5:].strip()
                continue
            if element.startswith("TIMESTAMP:"):
                timestamp = element[10:].strip()
                continue
            if element.startswith("FORMAT:"):
                post_format = element[7:].strip()
                continue
            if element.startswith("AUTHOR:"):
                author = element[7:].strip()
                continue
            print("\tUnknown metadata: %s" % (element))
        # Mandatory metadata
        if not title:
            print("\n\tNo TITLE found!")
            continue

        # Search tags
        tags = None

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
            print("\tError: No targetfile!")
            continue

        # Write src file result (content)
        try:
            t = open('%s%s' % (targetdir + '/' + targetfile, extension), 'w')
        except IOError as e:
            print("\t%s" % e)
            continue
        try:
            t.write(content.encode('utf-8'))
            print("\tsource file: OK")
        except ValueError as e:
            print("\t%s" % e)
            continue
        finally:
            t.close()

        # Create timestamp
        meta_timestamp = False
        date_to_change = timestamp or False
        if not date_to_change:
            date_to_change = date
        try:
            meta_timestamp = datetime.datetime.strptime(date_to_change, '%Y-%m-%d %H:%M:%S').strftime('%s')
        except ValueError as e:
            try:
                meta_timestamp = datetime.datetime.strptime(date_to_change, date_format).strftime('%s')
            except Exception as e:
                print("\tDate error: %s" % e)
                continue
        if not meta_timestamp:
            print("\tError: Date problem!")
            continue

        # Write db file result (meta info)
        try:
            d = open('%s%s' % (dbtargetdir + '/' + meta_timestamp + ',' + targetfile, db_ext), 'w')
        except IOError as e:
            print("\t%s" % e)
            continue
        try:
            # Write META INFO
            # First TITLE
            d.write('TITLE = %s\n' % title.encode('utf-8') or '')
            # Then DESCRIPTION
            d.write('DESCRIPTION = %s\n' % description.encode('utf-8') or '')
            # DATE
            d.write('DATE = %s\n' % date.encode('utf-8') or '')
            # TAGS
            if tags:
                d.write('TAGS = %s\n' % tags.encode('utf-8'))
            else:
                d.write('TAGS = %s\n' % default_tag.encode('utf-8'))
            # TYPE
            d.write('TYPE = %s\n' % default_type or '')
            print("\tdb file: OK")
        except ValueError as e:
            print("\t%s" % e)
            continue
        finally:
            d.close()

    # END
    return 0

if __name__ == '__main__':
    sys.exit(main())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
