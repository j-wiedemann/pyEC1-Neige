#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created: 19/05/2010 19:23:28 
#      by: peterp@n
#
# Ceci est la fenêtre qui affiche la carte des zones de neige en France

import os
from PyQt4 import QtCore, QtGui

class Ui_carte_neige(object):
    def setupUi(self, carte_neige):
        carte_neige.setObjectName("carte_neige")
        carte_neige.setWindowModality(QtCore.Qt.WindowModal)
        carte_neige.resize(582, 718)
        self.gridLayout = QtGui.QGridLayout(carte_neige)
        self.gridLayout.setObjectName("gridLayout")
        self.label_carte_zone_neige = QtGui.QLabel(carte_neige)
        self.label_carte_zone_neige.setMaximumSize(QtCore.QSize(1024, 768))
        self.label_carte_zone_neige.setText("")
        self.label_carte_zone_neige.setPixmap(QtGui.QPixmap("media/carte_zones_neige_france.png"))
        self.label_carte_zone_neige.setScaledContents(True)
        self.label_carte_zone_neige.setObjectName("label_carte_zone_neige")
        self.gridLayout.addWidget(self.label_carte_zone_neige, 0, 0, 1, 1)

        self.retranslateUi(carte_neige)
        QtCore.QMetaObject.connectSlotsByName(carte_neige)

    def retranslateUi(self, carte_neige):
        carte_neige.setWindowTitle(QtGui.QApplication.translate("carte_neige", "Carte des zones de neige en France", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    carte_neige = QtGui.QWidget()
    ui = Ui_carte_neige()
    ui.setupUi(carte_neige)
    carte_neige.show()
    sys.exit(app.exec_())

