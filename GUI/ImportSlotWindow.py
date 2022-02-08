from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QTextEdit, QFileDialog, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
import os
import sys
import time
from dotenv import load_dotenv, dotenv_values
import tarfile

     
AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])

from ShopWindow import ShopWindow

class ImportSlotWindow(QDialog):
    def __init__(self):
        super(ImportSlotWindow, self).__init__()
        uic.loadUi(f'{FolderPath}/GUI/Design/ImportWindow.ui', self)
        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        self.setWindowIcon(QtGui.QIcon(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaver.png"))
        self.LocalBtn = self.findChild(QPushButton, 'LocalBtn')
        self.LocalBtn.clicked.connect(self.ImportSlot)
        self.LocalBtn.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/LoadSlot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LocalBtn.setIcon(icon)



        self.ShopBtn = self.findChild(QPushButton, 'ShopBtn')
        self.ShopBtn.clicked.connect(self.Shop)
        self.ShopBtn.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ShoppingCart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShopBtn.setIcon(icon)

        self.BorderLabel = self.findChild(QLabel, 'BorderLabel')
        self.BorderLabel.setStyleSheet(f'''
        border: 5px solid {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};
        ''')


    def Shop(self):
        self.shop = ShopWindow()
        self.shop.show()            

        self.show()

    def ImportSlot(self):
        ImportFile=QFileDialog.getOpenFileName(self, 'Open file', f'{os.environ["HOME"]}', 'tar.gz archive (*.tar.gz)')
        if ImportFile[0] == '':
            return None

        tarFile = tarfile.open(ImportFile[0])
        SlotName = tarFile.getnames()[0]   

        if os.path.isdir(f"{FolderPath}/Slots/{SlotName}"):
            Overwrite = QMessageBox.question(self, 'Overwrite ?', 'A slot with that name already exists, Do you want to overwrite it ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if Overwrite == QMessageBox.Yes:  
                os.system(f"rm -r {FolderPath}/Slots/'{SlotName}'")
            else:
                return None     

        os.system(f'python3 {FolderPath}/GUI/LoadingWindow.py  "Importing {SlotName}" Importing &')

        os.system(f'themesaver import {ImportFile[0]}')

        os.system('pkill -f LoadingWindow.py')

        FinishedImporting = QMessageBox()
        FinishedImporting.setText("Finished Importing Slot")
        run = FinishedImporting.exec_()

