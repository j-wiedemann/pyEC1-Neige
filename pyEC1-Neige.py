#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created: 19/05/2010 19:23:28 
#      by: peterp@n
#
# Ce script permet de calculer la charge de neige sur une toiture selon les normes de calculs des Eurocodes 1-1-3
# N'est valable qu'en France
#
# Nécessite Python 2.6, PyQt4

import os, os.path, sys
from carte_zone_neige import *
from classDataImport import *
from xml.dom import minidom
from PyQt4 import QtCore, QtGui

HERE = os.path.dirname(sys.argv[0])
#APPDIR = os.path.abspath(HERE)
HERE = os.path.abspath(HERE)
#sys.path.insert(0, APPDIR)
sys.path.insert(0, HERE)
#os.chdir(APPDIR)
os.chdir(HERE)

class Ui_MainWindow(object):
    c_folder = os.getcwdu()
    f_datas = os.path.join(c_folder, "BDD_xml/zone_neige.xml")
    sk = 0
    altitude = 0
    coef_expo = 1
    coef_thermik = 1
    pente_1 = 0.0
    pente_2 = 0.0
    unit_surf = u" kN/m²"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(522, 785)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_1 = QtGui.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.main_title = QtGui.QLabel(self.centralwidget)
        self.main_title.setMaximumSize(QtCore.QSize(580, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.main_title.setFont(font)
        self.main_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.main_title.setObjectName("main_title")
        self.verticalLayout_1.addWidget(self.main_title)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_name_project = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name_project.sizePolicy().hasHeightForWidth())
        self.label_name_project.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_name_project.setFont(font)
        self.label_name_project.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name_project.setObjectName("label_name_project")
        self.gridLayout.addWidget(self.label_name_project, 0, 0, 1, 1)
        self.lineEdit_name_project = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_name_project.sizePolicy().hasHeightForWidth())
        self.lineEdit_name_project.setSizePolicy(sizePolicy)
        self.lineEdit_name_project.setMaximumSize(QtCore.QSize(250, 26))
        self.lineEdit_name_project.setObjectName("lineEdit_name_project")
        self.gridLayout.addWidget(self.lineEdit_name_project, 0, 1, 1, 1)
        self.verticalLayout_1.addLayout(self.gridLayout)
        self.gridLayout_7.addLayout(self.verticalLayout_1, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_geography = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_geography.setFont(font)
        self.title_geography.setObjectName("title_geography")
        self.verticalLayout_2.addWidget(self.title_geography)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_snow_zone = QtGui.QComboBox(self.centralwidget)
        self.comboBox_snow_zone.setObjectName("comboBox_snow_zone")
        self.gridLayout_2.addWidget(self.comboBox_snow_zone, 0, 1, 1, 1)
        self.label_altitude = QtGui.QLabel(self.centralwidget)
        self.label_altitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_altitude.setObjectName("label_altitude")
        self.gridLayout_2.addWidget(self.label_altitude, 1, 0, 1, 1)
        self.spinBox_altitude = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_altitude.setSuffix(" m")
        self.spinBox_altitude.setMaximum(2000)
        self.spinBox_altitude.setSingleStep(100)
        self.spinBox_altitude.setObjectName("spinBox_altitude")
        self.gridLayout_2.addWidget(self.spinBox_altitude, 1, 1, 1, 1)
        self.pushButton_zone_neige = QtGui.QPushButton(self.centralwidget)
        self.pushButton_zone_neige.setObjectName("pushButton_zone_neige")
        self.gridLayout_2.addWidget(self.pushButton_zone_neige, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.title_valeurs_k = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_valeurs_k.setFont(font)
        self.title_valeurs_k.setObjectName("title_valeurs_k")
        self.verticalLayout_2.addWidget(self.title_valeurs_k)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_sk200 = QtGui.QLabel(self.centralwidget)
        self.label_sk200.setText("Sk200 = ")
        self.label_sk200.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_sk200.setObjectName("label_sk200")
        self.gridLayout_3.addWidget(self.label_sk200, 0, 0, 1, 1)
        self.label_sad = QtGui.QLabel(self.centralwidget)
        self.label_sad.setText("SAd = ")
        self.label_sad.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_sad.setObjectName("label_sad")
        self.gridLayout_3.addWidget(self.label_sad, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(164, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_sk = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.pushButton_sk.sizePolicy().hasHeightForWidth())
        self.pushButton_sk.setSizePolicy(sizePolicy)
        self.pushButton_sk.setText("Sk = ")
        self.pushButton_sk.setEnabled(False)
        self.pushButton_sk.setObjectName("pushButton_sk")
        self.horizontalLayout.addWidget(self.pushButton_sk)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.label_rslt_sk200 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sk200.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sk200.setObjectName("label_rslt_sk200")
        self.gridLayout_3.addWidget(self.label_rslt_sk200, 0, 1, 1, 1)
        self.label_rslt_sad = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sad.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sad.setObjectName("label_rslt_sad")
        self.gridLayout_3.addWidget(self.label_rslt_sad, 1, 1, 1, 1)
        self.label_rslt_sk = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sk.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sk.setObjectName("label_rslt_sk")
        self.gridLayout_3.addWidget(self.label_rslt_sk, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.title_coefficient = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_coefficient.setFont(font)
        self.title_coefficient.setObjectName("title_coefficient")
        self.verticalLayout_2.addWidget(self.title_coefficient)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_coef_expo = QtGui.QLabel(self.centralwidget)
        self.label_coef_expo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_coef_expo.setObjectName("label_coef_expo")
        self.gridLayout_4.addWidget(self.label_coef_expo, 0, 0, 1, 1)
        self.doubleSpinBox_coef_expo = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_coef_expo.setMinimum(1.0)
        self.doubleSpinBox_coef_expo.setMaximum(1.25)
        self.doubleSpinBox_coef_expo.setSingleStep(0.25)
        self.doubleSpinBox_coef_expo.setObjectName("doubleSpinBox_coef_expo")
        self.gridLayout_4.addWidget(self.doubleSpinBox_coef_expo, 0, 1, 1, 1)
        self.label_coef_thermik = QtGui.QLabel(self.centralwidget)
        self.label_coef_thermik.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_coef_thermik.setObjectName("label_coef_thermik")
        self.gridLayout_4.addWidget(self.label_coef_thermik, 1, 0, 1, 1)
        self.doubleSpinBox_coef_thermik = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_coef_thermik.setMinimum(1.0)
        self.doubleSpinBox_coef_thermik.setMaximum(3.0)
        self.doubleSpinBox_coef_thermik.setObjectName("doubleSpinBox_coef_thermik")
        self.gridLayout_4.addWidget(self.doubleSpinBox_coef_thermik, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.title_geometry = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_geometry.setFont(font)
        self.title_geometry.setObjectName("title_geometry")
        self.verticalLayout_2.addWidget(self.title_geometry)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.doubleSpinBox_pente_2 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_pente_2.setEnabled(False)
        self.doubleSpinBox_pente_2.setDecimals(1)
        self.doubleSpinBox_pente_2.setMaximum(90.0)
        self.doubleSpinBox_pente_2.setObjectName("doubleSpinBox_pente_2")
        self.gridLayout_5.addWidget(self.doubleSpinBox_pente_2, 2, 2, 1, 1)
        self.doubleSpinBox_pente_1 = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_pente_1.setEnabled(False)
        self.doubleSpinBox_pente_1.setDecimals(1)
        self.doubleSpinBox_pente_1.setMaximum(90.0)
        self.doubleSpinBox_pente_1.setObjectName("doubleSpinBox_pente_1")
        self.gridLayout_5.addWidget(self.doubleSpinBox_pente_1, 2, 1, 1, 1)
        self.label_versant_2 = QtGui.QLabel(self.centralwidget)
        self.label_versant_2.setEnabled(False)
        self.label_versant_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_versant_2.setObjectName("label_versant_2")
        self.gridLayout_5.addWidget(self.label_versant_2, 1, 2, 1, 1)
        self.label_versant = QtGui.QLabel(self.centralwidget)
        self.label_versant.setAlignment(QtCore.Qt.AlignCenter)
        self.label_versant.setObjectName("label_versant")
        self.gridLayout_5.addWidget(self.label_versant, 1, 0, 1, 1)
        self.label_pente = QtGui.QLabel(self.centralwidget)
        self.label_pente.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pente.setObjectName("label_pente")
        self.gridLayout_5.addWidget(self.label_pente, 2, 0, 1, 1)
        self.label_versant_1 = QtGui.QLabel(self.centralwidget)
        self.label_versant_1.setEnabled(False)
        self.label_versant_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_versant_1.setObjectName("label_versant_1")
        self.gridLayout_5.addWidget(self.label_versant_1, 1, 1, 1, 1)
        self.comboBox_type_toiture = QtGui.QComboBox(self.centralwidget)
        self.comboBox_type_toiture.setObjectName("comboBox_type_toiture")
        self.comboBox_type_toiture.addItem("")
        self.comboBox_type_toiture.addItem("")
        self.comboBox_type_toiture.addItem("")
        self.gridLayout_5.addWidget(self.comboBox_type_toiture, 0, 0, 1, 1)
        self.checkBox_2versants = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2versants.setEnabled(False)
        self.checkBox_2versants.setObjectName("checkBox_2versants")
        self.gridLayout_5.addWidget(self.checkBox_2versants, 0, 2, 1, 1)
        self.label_dispositif_retenu = QtGui.QLabel(self.centralwidget)
        self.label_dispositif_retenu.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dispositif_retenu.setObjectName("label_dispositif_retenu")
        self.gridLayout_5.addWidget(self.label_dispositif_retenu, 3, 0, 1, 1)
        self.checkBox_retenu_1 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_retenu_1.setEnabled(False)
        self.checkBox_retenu_1.setObjectName("checkBox_retenu_1")
        self.gridLayout_5.addWidget(self.checkBox_retenu_1, 3, 1, 1, 1)
        self.checkBox_retenu_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_retenu_2.setEnabled(False)
        self.checkBox_retenu_2.setObjectName("checkBox_retenu_2")
        self.gridLayout_5.addWidget(self.checkBox_retenu_2, 3, 2, 1, 1)
        self.label_zone_faible_pente = QtGui.QLabel(self.centralwidget)
        self.label_zone_faible_pente.setEnabled(False)
        self.label_zone_faible_pente.setAlignment(QtCore.Qt.AlignCenter)
        self.label_zone_faible_pente.setObjectName("label_zone_faible_pente")
        self.gridLayout_5.addWidget(self.label_zone_faible_pente, 4, 0, 1, 1)
        self.label_rslt_finaux = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_rslt_finaux.sizePolicy().hasHeightForWidth())
        self.label_rslt_finaux.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_rslt_finaux.setFont(font)
        self.label_rslt_finaux.setObjectName("label_rslt_finaux")
        self.gridLayout_5.addWidget(self.label_rslt_finaux, 5, 0, 1, 3)
        self.label_coef_forme = QtGui.QLabel(self.centralwidget)
        self.label_coef_forme.setObjectName("label_coef_forme")
        self.gridLayout_5.addWidget(self.label_coef_forme, 6, 0, 1, 1)
        self.label_rslt_si = QtGui.QLabel(self.centralwidget)
        self.label_rslt_si.setObjectName("label_rslt_si")
        self.gridLayout_5.addWidget(self.label_rslt_si, 8, 0, 1, 1)
        self.label_rslt_sadi = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sadi.setObjectName("label_rslt_sadi")
        self.gridLayout_5.addWidget(self.label_rslt_sadi, 10, 0, 1, 1)
        self.label_rslt_sw = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sw.setObjectName("label_rslt_sw")
        self.gridLayout_5.addWidget(self.label_rslt_sw, 9, 0, 1, 1)
        self.label_rslt_sacc = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sacc.setEnabled(False)
        self.label_rslt_sacc.setObjectName("label_rslt_sacc")
        self.gridLayout_5.addWidget(self.label_rslt_sacc, 7, 0, 1, 1)
        self.label_mu_1 = QtGui.QLabel(self.centralwidget)
        self.label_mu_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_mu_1.setObjectName("label_mu_1")
        self.gridLayout_5.addWidget(self.label_mu_1, 6, 1, 1, 1)
        self.label_mu_2 = QtGui.QLabel(self.centralwidget)
        self.label_mu_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_mu_2.setObjectName("label_mu_2")
        self.gridLayout_5.addWidget(self.label_mu_2, 6, 2, 1, 1)
        self.label_rslt_sacc_1 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sacc_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sacc_1.setObjectName("label_rslt_sacc_1")
        self.gridLayout_5.addWidget(self.label_rslt_sacc_1, 7, 1, 1, 1)
        self.label_rslt_sacc_2 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sacc_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sacc_2.setObjectName("label_rslt_sacc_2")
        self.gridLayout_5.addWidget(self.label_rslt_sacc_2, 7, 2, 1, 1)
        self.label_rslt_s1 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_s1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_s1.setObjectName("label_rslt_s1")
        self.gridLayout_5.addWidget(self.label_rslt_s1, 8, 1, 1, 1)
        self.label_rslt_s2 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_s2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_s2.setObjectName("label_rslt_s2")
        self.gridLayout_5.addWidget(self.label_rslt_s2, 8, 2, 1, 1)
        self.label_rslt_sw_1 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sw_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sw_1.setObjectName("label_rslt_sw_1")
        self.gridLayout_5.addWidget(self.label_rslt_sw_1, 9, 1, 1, 1)
        self.label_rslt_sw_2 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sw_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sw_2.setObjectName("label_rslt_sw_2")
        self.gridLayout_5.addWidget(self.label_rslt_sw_2, 9, 2, 1, 1)
        self.label_rslt_sad_1 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sad_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sad_1.setObjectName("label_rslt_sad_1")
        self.gridLayout_5.addWidget(self.label_rslt_sad_1, 10, 1, 1, 1)
        self.label_rslt_sad_2 = QtGui.QLabel(self.centralwidget)
        self.label_rslt_sad_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_rslt_sad_2.setObjectName("label_rslt_sad_2")
        self.gridLayout_5.addWidget(self.label_rslt_sad_2, 10, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_5)
        self.gridLayout_7.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_reset = QtGui.QPushButton(self.centralwidget)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_6.addWidget(self.pushButton_reset, 0, 0, 1, 1)
        self.pushButton_exit = QtGui.QPushButton(self.centralwidget)
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.gridLayout_6.addWidget(self.pushButton_exit, 0, 2, 1, 1)
        self.pushButton_calcul = QtGui.QPushButton(self.centralwidget)
        self.pushButton_calcul.setEnabled(False)
        self.pushButton_calcul.setObjectName("pushButton_calcul")
        self.gridLayout_6.addWidget(self.pushButton_calcul, 0, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 522, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.cal=Calcul()
        self.i_dat = DataImport(self.f_datas)
        zone_neige = ["Zone de neige ..."]
        for p in self.i_dat.list:
            zone_neige.append(p)
        self.comboBox_snow_zone.addItems(zone_neige)
      
        QtCore.QObject.connect(self.lineEdit_name_project, QtCore.SIGNAL                                
                                ("editingFinished()"), self.set_nameProject)
        QtCore.QObject.connect(self.pushButton_zone_neige, QtCore.SIGNAL
                                ("clicked()"), self.voir_carte_zone_neige)
        QtCore.QObject.connect(self.comboBox_snow_zone, QtCore.SIGNAL
                                ("currentIndexChanged(int)"), self.set_profil)
        QtCore.QObject.connect(self.spinBox_altitude, QtCore.SIGNAL
                                ("valueChanged(int)"), self.change_val_altitude)
        QtCore.QObject.connect(self.pushButton_sk, QtCore.SIGNAL
                                ("clicked()"), self.sk_value)
        QtCore.QObject.connect(self.doubleSpinBox_coef_expo, QtCore.SIGNAL
                                ("valueChanged(double)"), self.change_val_coef)
        QtCore.QObject.connect(self.doubleSpinBox_coef_thermik, QtCore.SIGNAL
                                ("valueChanged(double)"), self.change_val_coef)
        QtCore.QObject.connect(self.comboBox_type_toiture, QtCore.SIGNAL
                                ("activated(int)"), self.set_versant_1)
        QtCore.QObject.connect(self.checkBox_2versants, QtCore.SIGNAL
                                ("stateChanged(int)"), self.set_versant_2)
        QtCore.QObject.connect(self.doubleSpinBox_pente_1, QtCore.SIGNAL
                                ("valueChanged(double)"), self.change_val_pente_1) 
        QtCore.QObject.connect(self.doubleSpinBox_pente_2, QtCore.SIGNAL
                                ("valueChanged(double)"), self.change_val_pente_2)
        QtCore.QObject.connect(self.pushButton_reset, QtCore.SIGNAL
                                ("clicked()"), self.reset_all)
        QtCore.QObject.connect(self.pushButton_calcul, QtCore.SIGNAL
                                ("clicked()"), self.cal.calcul)
        QtCore.QObject.connect(self.pushButton_exit, QtCore.SIGNAL
                                ("clicked()"), self.quit_application)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Charge de neige EC1-1-3", None, QtGui.QApplication.UnicodeUTF8))
        self.main_title.setText(QtGui.QApplication.translate("MainWindow", "Calcul de charge de neige sur une toiture", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name_project.setText(QtGui.QApplication.translate("MainWindow", "Nom du projet : ", None, QtGui.QApplication.UnicodeUTF8))
        self.title_geography.setText(QtGui.QApplication.translate("MainWindow", "Situation géographique du bâtiment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_altitude.setText(QtGui.QApplication.translate("MainWindow", "Altitude, A : ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zone_neige.setText(QtGui.QApplication.translate("MainWindow", "Afficher la carte des zones de neige", None, QtGui.QApplication.UnicodeUTF8))
        self.title_valeurs_k.setText(QtGui.QApplication.translate("MainWindow", "Valeurs caractéristiques", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sk200.setToolTip(QtGui.QApplication.translate("MainWindow", "Valeur caractéristique de la charge de neige sur le sol à une altitude inférieure à 200 m.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sad.setToolTip(QtGui.QApplication.translate("MainWindow", "Valeur de calcul de la charge de neige exceptionnelle de neige sur le sol.\n"
"SAd est indépendante de l\'altitude.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_sk.setToolTip(QtGui.QApplication.translate("MainWindow", "Sk est la valeur caractéristique de charge de neige à l\'altitude A.", None, QtGui.QApplication.UnicodeUTF8))
        self.title_coefficient.setText(QtGui.QApplication.translate("MainWindow", "Coefficients", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_expo.setToolTip(QtGui.QApplication.translate("MainWindow", "Le coefficient d\'exposition (Ce) permet de prendre en compte les conditions d\'abris de la toiture.\n"
"Si la toiture est protégée du vent par des bâtiments plus élévés ou par la présence de grands arbres à proximité, on prendra Ce=1,25.\n"
"On prendra Ce=1,0 dans tout les autres cas.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_expo.setText(QtGui.QApplication.translate("MainWindow", "Coefficient d\'exposition, Ce : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_thermik.setToolTip(QtGui.QApplication.translate("MainWindow", "Le coefficient thermique (Ct) permet de prendre en compte l\'influence du flux de chaleur\n"
"au travers de la toiture sur la fonte de la neige.\n"
"Les bâtiments normalement chauffés étant systématiquement isolés,\n"
" il convient de prendre Ct=1,0 sauf spécifications particulières dûment justifiées du projet individuel.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_thermik.setText(QtGui.QApplication.translate("MainWindow", "Coefficient thermique, Ct : ", None, QtGui.QApplication.UnicodeUTF8))
        self.title_geometry.setText(QtGui.QApplication.translate("MainWindow", "Géométrie de la toiture", None, QtGui.QApplication.UnicodeUTF8))
        self.doubleSpinBox_pente_2.setSuffix(QtGui.QApplication.translate("MainWindow", " °", None, QtGui.QApplication.UnicodeUTF8))
        self.doubleSpinBox_pente_1.setSuffix(QtGui.QApplication.translate("MainWindow", " °", None, QtGui.QApplication.UnicodeUTF8))
        self.label_versant_2.setText(QtGui.QApplication.translate("MainWindow", "Versant 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_versant.setText(QtGui.QApplication.translate("MainWindow", "Toiture", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pente.setToolTip(QtGui.QApplication.translate("MainWindow", "Pente du versant étudié en degrés.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pente.setText(QtGui.QApplication.translate("MainWindow", "Pente, αi", None, QtGui.QApplication.UnicodeUTF8))
        self.label_versant_1.setText(QtGui.QApplication.translate("MainWindow", "Versant 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_type_toiture.setToolTip(QtGui.QApplication.translate("MainWindow", "Choisissez le type de toiture : \n"
"Toiture simple pour des toiture à 1 ou 2 versants.\n"
"Toiture multique pour des toiture de bâtiments industriels (shelter ...).", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_type_toiture.setItemText(0, QtGui.QApplication.translate("MainWindow", "Type de toiture ...", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_type_toiture.setItemText(1, QtGui.QApplication.translate("MainWindow", "Toiture simple", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_type_toiture.setItemText(2, QtGui.QApplication.translate("MainWindow", "Toiture multiple", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2versants.setText(QtGui.QApplication.translate("MainWindow", "2eme versant ?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_dispositif_retenu.setToolTip(QtGui.QApplication.translate("MainWindow", "Cocher la case si il y a un dispositif de retenu de neige, barre à neige, acrotère, mur ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_dispositif_retenu.setText(QtGui.QApplication.translate("MainWindow", "Dispositif de retenue de neige ?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_retenu_1.setText(QtGui.QApplication.translate("MainWindow", "Présence", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_retenu_2.setText(QtGui.QApplication.translate("MainWindow", "Présence", None, QtGui.QApplication.UnicodeUTF8))
        self.label_zone_faible_pente.setText(QtGui.QApplication.translate("MainWindow", "Zone de faible pente (Noue)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_finaux.setText(QtGui.QApplication.translate("MainWindow", "Résultats", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_forme.setToolTip(QtGui.QApplication.translate("MainWindow", "Le coefficient de forme dépend : \n"
" - du type de toiture selectionné ;\n"
" - de la pente du versant ;\n"
" - et de la présence d\'un dispositif de retenue de neige.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_coef_forme.setText(QtGui.QApplication.translate("MainWindow", "Coefficient de forme : μi(αi)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_si.setToolTip(QtGui.QApplication.translate("MainWindow", "Si est la charge de neige horizontal à appliqué sur une toiture en situation normale.\n"
"Si =  μi(αi) * Ce * Ct * Sk ( + Sacc,i)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_si.setText(QtGui.QApplication.translate("MainWindow", "Charge de neige : Si", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sadi.setToolTip(QtGui.QApplication.translate("MainWindow", "SAd est la charge de neige en situation accidentelle,\n"
"elle est utilisée uniquement avec des combinaisons de situation accidentelle. ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sadi.setText(QtGui.QApplication.translate("MainWindow", "Charge exceptionnelle : SAd,i", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sw.setToolTip(QtGui.QApplication.translate("MainWindow", "Sw est la cahrge de neige compatible avec le vent, elle s\'applique sur le versant face au vent.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sw.setText(QtGui.QApplication.translate("MainWindow", "Charge compatible avec le vent : Sw,i", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sacc.setToolTip(QtGui.QApplication.translate("MainWindow", "Sacc est une charge de neige supplémentaire appliquée sur une zone de faible pente\n"
"et sur 2 mètre de rampant de part et d\'autres de la zone de faible pente.\n"
"Cette charge s\'ajoute à la cahrge Si. ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_rslt_sacc.setText(QtGui.QApplication.translate("MainWindow", "Charge supplémentaire : Sacc,i", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_reset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_exit.setText(QtGui.QApplication.translate("MainWindow", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_calcul.setText(QtGui.QApplication.translate("MainWindow", "Calculer", None, QtGui.QApplication.UnicodeUTF8))

# Modifie le titre de la fenêtre en rajoutant le nom du projet
    def set_nameProject(self):
        name_project = self.lineEdit_name_project.text()
        window_title = "Charge de neige EC1-1-3"
        if name_project:
            MainWindow.setWindowTitle(window_title + " | Projet : " + name_project)
        else :
            MainWindow.setWindowTitle(window_title)

# Affiche la carte des zones de neige dans une autre fenêtre (WindowModal pour pouvoir selectionner la zone en même temps qu'on voit la carte)
# Appelle carte_zone_neige.py
    def voir_carte_zone_neige(self):
        self.carte_neige = QtGui.QWidget()
        self.map = Ui_carte_neige()
        self.map.setupUi(self.carte_neige)
        self.carte_neige.show()

# Lorsqu'une zone de neige est choisie, affiche les valeurs de sk200 et sad et active le bouton sk
# Si "zone de neige" est choisi, désactive le bouton sk et remet à zero sad et sk200
    def set_profil(self, idx):
        if idx:
            self.sk200 = eval(self.i_dat.get_value(idx, "sk200"))
            self.label_rslt_sk200.setText(str(self.sk200) + self.unit_surf)
            self.sad = eval(self.i_dat.get_value(idx, "sad"))
            self.label_rslt_sad.setText(str(self.sad) + self.unit_surf)
            self.zoneneigeIndex=self.comboBox_snow_zone.currentIndex()
            self.pushButton_sk.setEnabled(True)
            self.label_rslt_sk.setText("")
            self.sk = 0
        else:
            self.pushButton_sk.setEnabled(False)
            self.label_rslt_sk200.setText("")
            self.label_rslt_sad.setText("")
            self.label_rslt_sk.setText("")
            self.sk200 = 0
            self.sad = 0
            self.sk = 0
            self.reset_rslt()

# Quand la valeur de l'altitude change, remet sk à zero et efface les éventuels résultats
    def change_val_altitude(self, v):
        self.label_rslt_sk.setText("")
        self.sk = 0
        self.altitude = self.spinBox_altitude.value()
        self.reset_rslt()

# Quand les coef change, attribue les valeurs aux variables associées et efface les éventuels résultats 
    def change_val_coef(self, v):
        self.coef_expo = self.doubleSpinBox_coef_expo.value()
        self.coef_thermik = self.doubleSpinBox_coef_thermik.value()
        self.reset_rslt()

# Quand la pente_1 change, attribue la valeur et efface les éventuels résultats de versant 1
    def change_val_pente_1(self, v):
        self.pente_1 = self.doubleSpinBox_pente_1.value()
        self.reset_rslt_versant1()

# Quand la pente_2 change, attribue la valeur et efface les éventuels résultats de versant 2
    def change_val_pente_2(self, v):
        self.pente_2 = self.doubleSpinBox_pente_2.value()
        self.reset_rslt_versant2()

# Calcul de la valeur de sk
    def sk_value(self):
        if self.altitude > 200 :
            if self.zoneneigeIndex == 8:
                if self.altitude < 500:
                    sk = self.sk200 + 0.15 * ((self.altitude-200) / 100)
                    self.sk = sk
                elif altitude > 1000:
                    sk = self.sk200 + 2.20 + 0.70 * ((self.altitude-1000) / 100)
                    self.sk = sk
                else :
                    sk = self.sk200 + 0.45 + 0.35 * ((self.altitude-500) / 100)
                    self.sk = sk
            else :
                if self.altitude < 500:
                    sk = self.sk200 + 0.10 * ((self.altitude-200) / 100)
                    self.sk = sk
                elif self.altitude > 1000:
                    sk = self.sk200 + 1.05 + 0.35 * ((self.altitude-1000) / 100)
                    self.sk = sk
                else :
                    sk = self.sk200 + 0.1 + 0.15 * ((self.altitude-500) / 100)
                    self.sk = sk
        else :
            self.sk = self.sk200
        self.label_rslt_sk.setText(str(self.sk) + self.unit_surf)

# Active les entrées pour versant1 quand "Toiture simple" et choisi dans comboBox_type_toiture
    def set_versant_1(self):
        self.combobox_toit_Index = self.comboBox_type_toiture.currentIndex()
        if self.combobox_toit_Index == 1:
            self.label_versant_1.setEnabled(True)
            self.doubleSpinBox_pente_1.setEnabled(True)
            self.checkBox_retenu_1.setEnabled(True)
            self.checkBox_2versants.setEnabled(True)
            self.pushButton_calcul.setEnabled(True)
        else:
            self.label_versant_1.setEnabled(False)
            self.doubleSpinBox_pente_1.setEnabled(False)
            self.checkBox_retenu_1.setEnabled(False)
            self.checkBox_2versants.setEnabled(False)
            self.label_versant_2.setEnabled(False)
            self.doubleSpinBox_pente_2.setEnabled(False)
            self.checkBox_retenu_2.setEnabled(False)
            self.pushButton_calcul.setEnabled(False)
            self.reset_rslt()

# Active ou désactive les entrées de versant 2 en fonction de checkBox_2versants
    def set_versant_2(self):
        if self.checkBox_2versants.isChecked():
            self.label_versant_2.setEnabled(True)
            self.doubleSpinBox_pente_2.setEnabled(True)
            self.checkBox_retenu_2.setEnabled(True)            
        else:
            self.label_versant_2.setEnabled(False)
            self.doubleSpinBox_pente_2.setEnabled(False)
            self.checkBox_retenu_2.setEnabled(False)
            self.reset_rslt_versant2()          

# Reset des résultats de versant1
    def reset_rslt_versant1(self):
        self.label_mu_1.setText("")
        self.mu_1 = 0
        self.label_rslt_s1.setText("")
        self.s1 = 0
        self.label_rslt_sw_1.setText("")
        self.sw_1 = 0
        self.label_rslt_sad_1.setText("")
        self.sad_1 = 0

# Reset des résultats de versant
    def reset_rslt_versant2(self):
        self.label_mu_2.setText("")
        self.mu_2 = 0
        self.label_rslt_s2.setText("")
        self.s2 = 0
        self.label_rslt_sw_2.setText("")
        self.sw_2 = 0
        self.label_rslt_sad_2.setText("")
        self.sad_2 = 0

# Reset des résultats des versants
    def reset_rslt(self):
        self.label_mu_1.setText("")
        self.mu_1 = 0
        self.label_mu_2.setText("")
        self.mu_2 = 0
        self.label_rslt_s1.setText("")
        self.s1 = 0
        self.label_rslt_s2.setText("")
        self.s2 = 0
        self.label_rslt_sw_1.setText("")
        self.sw_1 = 0
        self.label_rslt_sw_2.setText("")
        self.sw_2 = 0
        self.label_rslt_sad_1.setText("")
        self.sad_1 = 0
        self.label_rslt_sad_2.setText("")
        self.sad_2 = 0

# Reset de tout (sauf nom du projet)
    def reset_all(self):
        self.comboBox_snow_zone.setCurrentIndex(0)
        self.set_profil(0)
        self.spinBox_altitude.setValue(0)
        self.doubleSpinBox_coef_expo.setValue(1)
        self.doubleSpinBox_coef_thermik.setValue(1)
        self.comboBox_type_toiture.setCurrentIndex(0)
        self.set_versant_1()
        self.doubleSpinBox_pente_1.setValue(0)
        self.doubleSpinBox_pente_2.setValue(0)
        self.checkBox_retenu_1.setCheckState(False)
        self.checkBox_retenu_2.setCheckState(False)
        self.reset_rslt()

# Quitte l'application
    def quit_application(self):
         sys.exit()

"""
class DataImport(object):

    def __init__(self, datas):
        xmldoc = minidom.parse(datas)
        self.reflist = xmldoc.getElementsByTagName('profil')
        self.listneige = [ligneX.attributes["id"].value for ligneX in self.reflist]

    def get_value(self, idx, d) :
        ligneX = self.reflist[idx - 1]
        valeur_symbole = ligneX.attributes[d]
        valeur_symbole = valeur_symbole.value
        valeur_symbole = valeur_symbole.encode('utf-8')
        return valeur_symbole
"""

class Calcul(object):
    def __init__(self):
        pass

    def mui_simple_toit_calcul(self, pente, retenu) : 
        if retenu == "true" or pente <= 30 :
            self.mui = 0.8
            return self.mui
        else :
            if pente >= 60 :
                self.mui = 0
                return self.mui
            else :
                self.mui=(60 - pente) * 0.8 / 30
                return self.mui

    def set_mui(self):
        if ui.checkBox_retenu_1.isChecked():
            retenu_1 = "true"
            pente_1 = ui.pente_1
            self.mu_1 = self.mui_simple_toit_calcul(pente_1, retenu_1)
            ui.label_mu_1.setText(str( "%.2f" % self.mu_1))
        else :
            retenu_1 = "false"
            pente_1 = ui.pente_1
            self.mu_1 = self.mui_simple_toit_calcul(pente_1, retenu_1)
            ui.label_mu_1.setText(str("%.2f" % self.mu_1))
        if ui.checkBox_2versants.isChecked():
            if ui.checkBox_retenu_2.isChecked():
                retenu_2 = "true"
                pente_2 = ui.pente_2
                self.mu_2 = self.mui_simple_toit_calcul(pente_2, retenu_2)
                ui.label_mu_2.setText(str("%.2f" % self.mu_2))
            else :
                retenu_2 = "false"
                pente_2 = ui.pente_2
                self.mu_2 = self.mui_simple_toit_calcul(pente_2, retenu_2)
                ui.label_mu_2.setText(str("%.2f" % self.mu_2))

    def si_calcul(self, mui):
        ce = ui.coef_expo
        ct = ui.coef_thermik
        sk = ui.sk 
        self.si = mui * ce * ct * sk
        return self.si
          
    def set_si(self):
        if ui.sk:
            self.s1 = self.si_calcul(self.mu_1)
            ui.label_rslt_s1.setText(str("%.2f" % self.s1) + ui.unit_surf)
            ui.statusbar.clearMessage()
            if ui.checkBox_2versants.isChecked():
                self.s2 = self.si_calcul(self.mu_2)
                ui.label_rslt_s2.setText(str("%.2f" % self.s2) + ui.unit_surf)
        else :
            ui.statusbar.showMessage(u"Données insufisantes : Zone de neige ou Sk non définis.")
            ui.label_rslt_s1.setText("")
            ui.label_rslt_s2.setText("")

    def swi_calcul(self, mui):
        ce = ui.coef_expo
        ct = ui.coef_thermik
        sk = ui.sk 
        self.swi = (mui * 0.5) * ce * ct * sk
        return self.swi    

    def set_swi(self):
        if ui.sk:
            self.sw_1 = self.swi_calcul(self.mu_1)
            ui.label_rslt_sw_1.setText(str("%.2f" % self.sw_1) + ui.unit_surf)
            ui.statusbar.clearMessage()
            if ui.checkBox_2versants.isChecked():
                self.sw_2 = self.swi_calcul(self.mu_2)
                ui.label_rslt_sw_2.setText(str("%.2f" % self.sw_2) + ui.unit_surf)
        else :
            ui.statusbar.showMessage(u"Données insufisantes : Zone de neige ou Sk non définis.")
            ui.label_rslt_sw_1.setText("")
            ui.label_rslt_sw_2.setText("")

    def sadi_calcul(self, mui):
        ce = ui.coef_expo
        ct = ui.coef_thermik
        sad = ui.sad 
        self.sadi = mui * ce * ct * sad
        return self.sadi    

    def set_sadi(self):
        if ui.sk:
            if ui.sad:
                self.sad_1 = self.sadi_calcul(self.mu_1)
                ui.label_rslt_sad_1.setText(str("%.2f" % self.sad_1) + ui.unit_surf)
                ui.statusbar.clearMessage()
                if ui.checkBox_2versants.isChecked():
                    self.sad_2 = self.sadi_calcul(self.mu_2)
                    ui.label_rslt_sad_2.setText(str("%.2f" % self.sad_2) + ui.unit_surf)
            else :
                ui.statusbar.showMessage(u"Remarque : Cette zone n'est pas en situation de charge de neige exceptionnelle (Sad).")
                ui.label_rslt_sad_1.setText("")
                ui.label_rslt_sad_2.setText("")
        else :
            ui.statusbar.showMessage(u"Données insufisantes : Zone de neige ou Sk non définis.")
            ui.label_rslt_sad_1.setText("")
            ui.label_rslt_sad_2.setText("")

    def calcul(self) :
        if ui.combobox_toit_Index == 1:
            self.set_mui()
            self.set_si()
            self.set_swi()
            self.set_sadi()
        else :
            ui.statusbar.showMessage(u"Données insufisantes : Type de toiture incorrecte.")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
