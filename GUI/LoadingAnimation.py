from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QMainWindow)
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import QDir
import os
import sys
import time
from dotenv import load_dotenv, dotenv_values

AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])


class LoadingAnimation(QDialog):
    def __init__(self):
        super(LoadingAnimation, self).__init__()

        uic.loadUi(f'{FolderPath}/GUI/Design/LoadingWindow.ui', self)   

        self.setWindowIcon(QtGui.QIcon(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/ThemeSaver.png"))
        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        self.movie = QMovie(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/Exporting.gif")

        self.gif = self.findChild(QLabel, 'gif')  

        self.gif.setStyleSheet(f'''
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']}; 
        border: 2px solid {AppConfig['button-background-color']};
        ''')

        self.Message = self.findChild(QLabel, 'Message')
        self.Message.setText(f'Exporting Slot')
        self.Message.setStyleSheet(f'''
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


        self.gif.setMovie(self.movie)

        self.movie.start()
