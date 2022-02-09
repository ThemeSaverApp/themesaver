from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog ,QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap, QPalette, QMovie
from PyQt5.QtCore import QDir
import os
import subprocess
import sys
import time
import webbrowser
from dotenv import load_dotenv, dotenv_values
import tarfile
from pathlib import Path
import json


AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])

if not 'icon-pack' in AppConfig.keys():
    AppConfig["icon-pack"] = 'OG'
if not 'icon-color' in AppConfig.keys():
    AppConfig["icon-color"] = '#ffffff'

from SaveSlotWindow import SaveSlotWindow
from LoadSlotWindow import LoadSlotWindow
from ImportSlotWindow import ImportSlotWindow



try:

    if AppConfig['icon-pack'] == 'Custom': 
        if not os.path.isdir(f'{FolderPath}/GUI/Icons/Custom'):
            os.mkdir(f'{FolderPath}/GUI/Icons/Custom')
        icon_color = open(f'{FolderPath}/GUI/Icons/Custom/icon-color', 'r').read().strip()
        if icon_color != AppConfig["icon-color"]:
            for image in os.listdir(f'{FolderPath}/GUI/Icons/src'):
                print('hi')
                os.system(f'convert {FolderPath}/GUI/Icons/src/{image} -fill "{AppConfig["icon-color"]}" -colorize 100 {FolderPath}/GUI/Icons/Custom/{image}')
            os.system(f'echo "{AppConfig["icon-color"]}" >  {FolderPath}/GUI/Icons/Custom/icon-color')
except:
    pass


if open(f'{FolderPath}/GUI/Icons/icon-pack', 'r').read().strip() != AppConfig['icon-pack']:
    os.system(f'cp {FolderPath}/GUI/Icons/{AppConfig["icon-pack"]}/ThemeSaver.png ~/.local/share/icons')
    os.system(f'echo "{AppConfig["icon-pack"]}" >  {FolderPath}/GUI/Icons/icon-pack')


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        uic.loadUi(f'{FolderPath}/GUI/Design/MainWindow.ui', self)

        self.setStyleSheet(f"background-color: {AppConfig['background-color']};")

        def SetIcon(widget, iconName):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/{iconName}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            widget.setStyleSheet(f'''
            color: {AppConfig['text-color']};
            background-color: {AppConfig['button-background-color']};
            border-radius: {AppConfig['button-border-radius']};
            font: {AppConfig['text-style']}  {AppConfig['font-size']} {AppConfig['font-name']}
            ''')
            
            widget.setIcon(icon)

        self.setWindowIcon(QtGui.QIcon(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaver.png"))

        self.SaveSlotBtn = self.findChild(QPushButton, 'SaveSlotBtn')
        self.SaveSlotBtn.clicked.connect(self.SaveSlot)
        SetIcon(self.SaveSlotBtn, 'Save')

        self.LoadSlotBtn = self.findChild(QPushButton, 'LoadSlotBtn')
        self.LoadSlotBtn.clicked.connect(self.LoadSlot)
        SetIcon(self.LoadSlotBtn, 'LoadSlot')

        self.ImportSlotBtn = self.findChild(QPushButton, 'ImportSlotBtn')
        self.ImportSlotBtn.clicked.connect(self.ImportSlot)
        SetIcon(self.ImportSlotBtn, 'Import')

        self.ThemeShopBtn = self.findChild(QPushButton, 'ThemeShopBtn')
        self.ThemeShopBtn.clicked.connect(self.ThemeShop)
        SetIcon(self.ThemeShopBtn, 'ShoppingCart')

        self.ThemeSaverLogo = self.findChild(QLabel, 'ThemeSaverLogo')
        self.ThemeSaverLogo.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaverLogo.png"))
        self.ThemeTextLabel = self.findChild(QLabel, 'ThemeTextLabel')
        self.ThemeTextLabel.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeText.png"))
        self.SaverTextLabel = self.findChild(QLabel, 'SaverTextLabel')
        self.SaverTextLabel.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/SaverText.png"))

        self.BorderLabel = self.findChild(QLabel, 'BorderLabel')
        self.BorderLabel.setStyleSheet(f'''
        border: 5px solid {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};
        ''')

        self.show()

    def SaveSlot(self):
        self.SaveSlotWin = SaveSlotWindow(Main)
        self.SaveSlotWin.show()

    def LoadSlot(self):
        if not os.path.isdir(f'{FolderPath}/Slots'):
            os.mkdir(f'{FolderPath}/Slots')

        self.SlotNames = []

        if 'XDG_CURRENT_DESKTOP' in os.environ.keys():
            DE = os.environ['XDG_CURRENT_DESKTOP'].lower().strip()
            if len(DE.split(':')) != 1:
                DE = DE.split(':')[1]
        elif 'DESKTOP_SESSION' in os.environ.keys():
            DE = os.environ['DESKTOP_SESSION'].lower().strip()
        WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()
        if DE.strip() == '':
            DE = WM            

        for slotname in os.listdir(f"{FolderPath}/Slots/"):
            jsonFile = json.load(open(f'{FolderPath}/Slots/{slotname}/info.json'))
            if jsonFile['desktopEnvironment'] == DE and jsonFile['windowManager'] == WM:
                self.SlotNames.append(slotname)

        if len(self.SlotNames) == 0:
            NoSlots = QMessageBox()
            NoSlots.setText("There are no saved slots")
            NoSlots.setIcon(QMessageBox.Critical)
            run = NoSlots.exec_()
            return None

        self.LoadSlotWin = LoadSlotWindow()
        self.LoadSlotWin.show()

    def ImportSlot(self):
        self.win = ImportSlotWindow()
        self.win.show()

    def ThemeShop(self):
        webbrowser.open('https://themesaver.herokuapp.com/shop')


app = QApplication(sys.argv)
Main = MainWin()
app.exec_()
