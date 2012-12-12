#!/usr/bin/env python

import re

url = 'http://olivier.dossmann.net/joueb/'
new_url = "${BASE_URL}/"

chaine = """Comme vous avez pu le constater, autant par le fait que les billets manquent que par le [dernier billet](http://olivier.dossmann.net/joueb/archives/2008/08/31/index.html#e2008-08-31T19_13_50.txt "Lire le dernier billet"), le BlankoJoueb rencontre des troubles d\'affichage."""
autrechaine = """"""
encore = """quelque chose sans url"""

pattern = """(?P<before>^.*\[.*\]\()(?P<address>.*)(?P<after> ['"]+.*['"]+\).*$)"""

def remplacement(p):
    b = p.group('before')
    u = p.group('address')
    e = p.group('after')
    if u.startswith(url):
        u = u.replace(url, new_url)
    return "%s%s%s" % (b, u, e)


print re.sub(pattern, remplacement, chaine, 1)
print re.sub(pattern, remplacement, autrechaine, 1)
print re.sub(pattern, remplacement, encore, 1)
