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


AppConfig = dotenv_values(f"{os.environ['HOME']}/.config/ThemeSaver/config.env")
FolderPath = os.path.expanduser(AppConfig['FolderPath'])

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        uic.loadUi(f'{FolderPath}/GUI/Design/LoadingWindow.ui', self)

        self.setStyleSheet(f"background-color: {AppConfig['background-color']};\n")

        self.movie = QMovie(f"{FolderPath}/GUI/Icons/{AppConfig['icon-pack']}/{sys.argv[2]}.gif")

        self.gif.setStyleSheet(f'''
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']}; 
        border: 2px solid {AppConfig['button-background-color']};
        ''')

        self.Message.setText(sys.argv[1])
        self.Message.setStyleSheet(f'''
        color: {AppConfig['text-color']};
        background-color: {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};   
        font: {AppConfig['text-style']} {AppConfig['font-size']} {AppConfig['font-name']};
        ''')

        self.BorderLabel.setStyleSheet(f'''
        border: 5px solid {AppConfig['button-background-color']};
        border-radius: {AppConfig['button-border-radius']};
        ''')
        self.gif.setMovie(self.movie)

        self.movie.start()

        self.show()
     

app = QApplication(sys.argv)
Main = MainWin()
app.exec_()
