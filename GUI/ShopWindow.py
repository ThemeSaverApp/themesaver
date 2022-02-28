from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
import os
import sys
import time
from dotenv import load_dotenv, dotenv_values
import requests
import tarfile

     
AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])


class ShopWindow(QDialog):
    def __init__(self):
        super(ShopWindow, self).__init__()
        uic.loadUi(f'{FolderPath}/GUI/Design/ShopWindow.ui', self)
        self.show()


        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        self.setWindowIcon(QtGui.QIcon(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaver.png"))
        self.RepoLink = self.findChild(QTextEdit, 'RepoLink')
        self.RepoLink.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['font-size']} {AppConfig['font-name']};     
        border : 4px solid {AppConfig['button-background-color']};
        border : 2px solid {AppConfig['button-background-color']};
        border-top: 6px solid {AppConfig['button-background-color']};
        border-style: solid;
        ''')

        self.RepoLabel = self.findChild(QLabel, 'RepoLabel')
        self.RepoLabel.setStyleSheet(f'''
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

        self.DownloadBtn = self.findChild(QPushButton, 'DownloadBtn')
        self.DownloadBtn.clicked.connect(self.Download)
        self.DownloadBtn.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};     
        ''')

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/LoadSlot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DownloadBtn.setIcon(icon)        


    def Download(self):
        Repo = self.RepoLink.toPlainText().strip()
        if not len(Repo.split(':')) == 2:
            InvalidRepo = QMessageBox()
            InvalidRepo.setText("Invalid Link (No Branch Provided For Repo)")
            InvalidRepo.setIcon(QMessageBox.Critical)
            run = InvalidRepo.exec_()
            return None    

        url = Repo.split(':')
        r = requests.get(f'https://api.github.com/repos/{url[0]}/git/trees/{url[1]}?recursive=1')
        
        if 'message' in r.json().keys():
            if r.json()['message'] == 'Not Found':
                InvalidRepo = QMessageBox()
                InvalidRepo.setText("Invalid Link (No such link)")
                InvalidRepo.setIcon(QMessageBox.Critical)
                run = InvalidRepo.exec_()
                return None                


        # Checking if the repo contains a info.json file and contains the slot archive
        ifTar = False
        ifJson = False
        for i in r.json()['tree']:
            if i['path'] == 'info.json':
                ifJson = True
            elif i['path'].endswith('.tar.gz'):
                ifTar = True

        if not ifJson or not ifTar:
            InvalidRepo = QMessageBox()
            InvalidRepo.setText("Invalid Link (info.json or archive not found)")
            InvalidRepo.setIcon(QMessageBox.Critical)
            run = InvalidRepo.exec_()
            return None            

        os.system(f'python3 {AppConfig["FolderPath"]}/GUI/LoadingWindow.py  "Installing Slot" Importing &')

        for i in r.json()['tree']:
            if i['path'].endswith('.tar.gz'):
                archive = requests.get(f'https://github.com/{url[0]}/blob/{url[1]}/{i["path"]}?raw=true', allow_redirects=True)
                open(f'{FolderPath}/{i["path"]}', 'wb').write(archive.content)
                tarFileLocation = f'{FolderPath}/{i["path"]}'
                tarFile = tarfile.open(tarFileLocation)
                SlotName = tarFile.getnames()[0]
                break

        if os.path.isdir(f"{FolderPath}/Slots/{SlotName}"):
            Overwrite = QMessageBox.question(self, 'Overwrite ?', 'A slot with that name already exists, Do you want to overwrite it ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if Overwrite == QMessageBox.Yes:  
                os.system(f"rm -r {FolderPath}/Slots/'{SlotName}'")
            else:
                return None            


        os.system(f'themesaver import {tarFileLocation}')
        os.system('pkill -f LoadingWindow.py')

        FinishedSaving = QMessageBox()
        FinishedSaving.setText("Finished Installing Slot")
        run = FinishedSaving.exec_()
        self.hide()


