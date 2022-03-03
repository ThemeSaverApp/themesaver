from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import QDir
import os, sys, time, json
from dotenv import load_dotenv, dotenv_values

     
AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])

class LoadSlotWindow(QDialog):
    def __init__(self):
        super(LoadSlotWindow, self).__init__()

        uic.loadUi(f'{FolderPath}/GUI/Design/LoadSlotWindow.ui', self)     

        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        def SetIcon(widget, iconName):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/{iconName}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            widget.setStyleSheet(f'''
                color: {AppConfig['text-color']};
                background-color: {AppConfig['button-background-color']};
                border-radius: {AppConfig['button-border-radius']};   
                font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};             
            ''')
            
            widget.setIcon(icon)


        self.ForwardBtn = self.findChild(QPushButton, 'ForwardBtn')
        self.ForwardBtn.clicked.connect(self.Forward) 
        SetIcon(self.ForwardBtn, 'ForwardArrow')
        
        self.BackBtn = self.findChild(QPushButton, 'BackBtn') 
        self.BackBtn.clicked.connect(self.Back)
        SetIcon(self.BackBtn, 'BackArrow')

        self.LoadSlotBtn = self.findChild(QPushButton, 'LoadSlotBtn')  
        self.LoadSlotBtn.clicked.connect(self.Load) 
        SetIcon(self.LoadSlotBtn, 'LoadSlot')

        self.ExportSlotBtn = self.findChild(QPushButton, 'ExportSlotBtn')
        self.ExportSlotBtn.clicked.connect(self.Export) 
        SetIcon(self.ExportSlotBtn, 'Export')

        self.DeleteBtn = self.findChild(QPushButton, 'DeleteSlotBtn') 
        self.DeleteBtn.clicked.connect(self.Del)
        SetIcon(self.DeleteBtn, 'Delete')

        self.Screenshot = self.findChild(QLabel, 'Screenshot')
        self.Screenshot.setStyleSheet(f'''
        border-radius: 10px;
        border: 5px solid {AppConfig['button-background-color']};
        ''')

        self.BorderLabel = self.findChild(QLabel, 'BorderLabel')
        self.BorderLabel.setStyleSheet(f'''
        border: 5px solid {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};
        ''')


        self.SlotName = self.findChild(QLabel, 'SlotName')
        self.SlotName.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        
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


        global CurrentSlot
        CurrentSlot = 0

        self.SlotName.setText(self.SlotNames[CurrentSlot])
        self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{self.SlotNames[CurrentSlot]}/Screenshot.png"))

        


    def Forward(self):
            global CurrentSlot
            if not CurrentSlot + 1 == len(self.SlotNames):
                    CurrentSlot += 1
                    self.SlotName.setText(self.SlotNames[CurrentSlot])
                    self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{self.SlotNames[CurrentSlot]}/Screenshot.png"))

    def Back(self):
            global CurrentSlot
            if not CurrentSlot == 0:
                    CurrentSlot -= 1
                    self.SlotName.setText(self.SlotNames[CurrentSlot])
                    self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{self.SlotNames[CurrentSlot]}/Screenshot.png"))

    def Del(self):
            global CurrentSlot
            os.system(f"rm -r {FolderPath}/Slots/'{self.SlotNames[CurrentSlot]}'")
            FinishedDeleting = QMessageBox()
            FinishedDeleting.setText(f"Finished Deleting The ''{self.SlotNames[CurrentSlot]}'' Slot")
            run = FinishedDeleting.exec_()

            # Staring from begginning after deleting 1 slot
            self.SlotNames = []

            for slotname in os.listdir(f"{FolderPath}/Slots/"):
                DE = os.environ['DESKTOP_SESSION'].lower()
                WM = os.popen("wmctrl -m").read().split('\n')[0].replace('Name: ', '').lower()
                jsonFile = json.load(open(f'{FolderPath}/Slots/{slotname}/info.json'))
                if jsonFile['desktopEnvironment'] == DE and jsonFile['windowManager'] == WM:
                    self.SlotNames.append(slotname)



            if len(self.SlotNames) == 0:
                NoSlots = QMessageBox()
                NoSlots.setText("There are no more saved slots")
                NoSlots.setIcon(QMessageBox.Critical)
                run = NoSlots.exec_()
                self.hide()
                return None       

                    
            CurrentSlot = 0
            self.SlotName.setText(self.SlotNames[CurrentSlot])
            self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{self.SlotNames[CurrentSlot]}/Screenshot.png"))

    def Load(self):
            global CurrentSlot
            os.system(f"python3 {FolderPath}/ThemeSaver.py load '{self.SlotNames[CurrentSlot]}'")
            FinishedLoading = QMessageBox()
            FinishedLoading.setText(f"Finished Loading The '{self.SlotNames[CurrentSlot]}' Slot")
            run = FinishedLoading.exec_()

    def Export(self):
            global CurrentSlot
            ExportPath = QFileDialog.getExistingDirectory(self, 'Open file', f'{FolderPath}')
            os.system(f'python3 {FolderPath}/GUI/LoadingWindow.py  "Exporting {self.SlotNames[CurrentSlot]}" Exporting &')
            os.system(f"themesaver export '{self.SlotNames[CurrentSlot]}' {ExportPath}")
            os.system('pkill -f LoadingWindow.py')
            FinishedExporting = QMessageBox()
            FinishedExporting.setText(f"Finished Exporting Slot To {ExportPath}/'{self.SlotNames[CurrentSlot]}'.tar.gz")
            run = FinishedExporting.exec_()
