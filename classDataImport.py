#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is a part of FreeEurocodes

import os
from xml.dom import minidom

class DataImport(object):

    def __init__(self, datas):
        xmldoc = minidom.parse(datas)
        self.reflist = xmldoc.getElementsByTagName('profil')
        self.list = [ligneX.attributes["id"].value for ligneX in self.reflist]

    def get_value(self, idx, d) :
        ligneX = self.reflist[idx - 1]
        valeur_symbole = ligneX.attributes[d]
        valeur_symbole = valeur_symbole.value
        valeur_symbole = valeur_symbole.encode('utf-8')
        return valeur_symbole
