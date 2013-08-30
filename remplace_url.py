#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

url = 'http://olivier.dossmann.net/joueb/'
new_url = "${BLOG_URL}/"

chaine = """Comme vous avez pu le constater, autant par le fait que les billets manquent que par le [dernier billet](http://olivier.dossmann.net/joueb/archives/2008/08/31/index.html#e2008-08-31T19_13_50.txt "Lire le dernier billet"), le BlankoJoueb rencontre des troubles d\'affichage."""
autrechaine = """"""
encore = """quelque chose sans url"""
html_chaine = """J'écris une chaîne au hasard avec <a href="http://olivier.dossmann.net/joueb/archives/2008/index.html" title="Un lien">un lien dedans</a>"""

pattern = """(?P<begin>^.*\[.*\]\()(?P<address>.*)(?P<end> ['"]+.*['"]+\).*$)"""
html_pattern = """(?P<begin>^.*\<a href=['"]+)(?P<address>.*)(?P<end>['"]+.*$)"""

def remplacement(p):
    b = p.group('begin')
    u = p.group('address')
    e = p.group('end')
    if u.startswith(url):
        u = u.replace(url, new_url)
    return "%s%s%s" % (b, u, e)


print re.sub(pattern, remplacement, chaine, 1)
print re.sub(pattern, remplacement, autrechaine, 1)
print re.sub(pattern, remplacement, encore, 1)
print re.sub(html_pattern, remplacement, html_chaine, 1)
