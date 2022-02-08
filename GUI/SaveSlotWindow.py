from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
import os
import sys
import time
from dotenv import load_dotenv, dotenv_values

     
AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])


class SaveSlotWindow(QDialog):
    def __init__(self, MainWin):
        super(SaveSlotWindow, self).__init__()


        self.MainWin = MainWin

        uic.loadUi(f'{FolderPath}/GUI/Design/SaveSlotWindow.ui', self)

        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        self.setWindowIcon(QtGui.QIcon(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaver.png"))
        self.SaveSlotBtn = self.findChild(QPushButton, 'SaveSlotBtn')
        self.SaveSlotBtn.clicked.connect(self.SaveSlot)
        self.SaveSlotBtn.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveSlotBtn.setIcon(icon)

        self.SlotNameInput = self.findChild(QTextEdit, 'SlotName')
        self.SlotNameInput.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['font-size']} {AppConfig['font-name']};     
        border : 4px solid {AppConfig['button-background-color']};
        border : 2px solid {AppConfig['button-background-color']};
        border-top: 6px solid {AppConfig['button-background-color']};
        border-style: solid;
        ''')

        self.SlotNameLabel = self.findChild(QLabel, 'SlotNameLabel')
        self.SlotNameLabel.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        self.BorderLabel = self.findChild(QLabel, 'BorderLabel')
        self.BorderLabel.setStyleSheet(f'''
        border: 5px solid {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};
        ''')



    def SaveSlot(self):
        SlotName = self.SlotNameInput.toPlainText()
        if SlotName.strip() == "":
            EmptyName = QMessageBox()
            EmptyName.setText('Enter Valid Slot Name')
            run = EmptyName.exec_()
            return None
        elif os.path.isdir(f"{FolderPath}/Slots/{SlotName}"):
            Overwrite = QMessageBox.question(self, 'Overwrite ?', 'A slot with that name already exists, Do you want to overwrite it ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if Overwrite == QMessageBox.Yes:  
                os.system(f"rm -r {FolderPath}/Slots/'{SlotName}'")
            else:
                return None
        
        self.MainWin.hide()
        self.hide()
        os.system(f'themesaver save {SlotName}')
        self.MainWin.show()
        self.show()

        FinishedSaving = QMessageBox()
        FinishedSaving.setText("Finished Saving Theme")
        run = FinishedSaving.exec_()
        self.hide()
            

  
        
