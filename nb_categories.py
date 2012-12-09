#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nb_categories.py
#
# Fetch categories from Nanoblogger DB files

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

datadir = 'data'
cat_ext = '.db'

dirList=os.listdir(datadir)
categs = []
for fname in dirList:
    if fname.endswith(cat_ext):
        categs.append(fname)

if not categs:
    print("Warning: no categs found in this directory: %s." % datadir)

categs_data = {
    'categories': {},
    'files': {},
}

for i, categ in enumerate(categs):
    # Create path to reach categorie's file
    path = datadir + '/' + categ
    text = False
    # Open it, read content and close it
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
 
    # Go to next file if no content
    if not text:
        print("No text found in %s file" % path)
        continue
    # Else parse content
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    lines = text.split("\n")
    if not lines[0]:
        print("No name found for category in %s file" % path)
        continue
    if categ != 'master.db':
        # search categ ID
        categ_id = False
        categ_filename = categ.split('.') and categ.split('.')[0] and categ.split('.')[0].split('_')
        if categ_filename and len(categ_filename) > 1:
            categ_id = categ_filename[1]
        if not categ_id:
            print("No category ID found for this file: %s" % path)
            continue
        # Search name
        name = lines[0]
        # write categ info in result
        categs_data['categories'].update({categ_id: name})
    for j, line in enumerate(lines):
        if j == 0:
            continue
        if not line:
            continue
        info = line.split('>')
        if len(info) > 1:
            categ_ids = info[1].split(',')
            if info[0] not in categs_data['files']:
                categs_data['files'].update({info[0]: categ_ids})
            else:
                existing_ids = categs_data['files'][info[0]]
                for c_id in categ_ids:
                    if c_id not in existing_ids:
                        existing_ids.append(c_id)
                categs_data['files'][info[0]] = existing_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
