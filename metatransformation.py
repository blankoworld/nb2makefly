#!/usr/bin/env python
# -*- coding: utf-8 -*

import re

A = "éèàçêîâôï "
B = "eeaceiaoi_"
print list(A), list(B)
C = dict(zip(list(A), list(B)))

def mt(string=False):
    res = ""
    if not string:
        return False
    res = re.escape(string)
    for el in C:
        if el in res:
            res = res.replace(el, C[el])
    return res

print(mt("Pourquoi cet été votre âtre côtier n'avait-il pas accueilli l'évènement de François? Quelle naïveté!"))

print(mt("évidemment"))
print(mt("ça sert?"))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
