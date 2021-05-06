from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
'''
TODO:
-> Create shop
-> Check if There is a slot with that name while importing
-> Add load bar for import and export slot
Idea: Not letting themesaver be installed if desktop environment is not supported reducing my work :)
'''


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        FolderPath = f"{os.environ['HOME']}/ThemeSaver"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(332, 362)
        MainWindow.setMaximumSize(QtCore.QSize(332, 362))
        MainWindow.setStyleSheet("background-color: rgb(247, 137, 20);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ThemeSaverLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SaveSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: SaveSlot())
        self.SaveSlotBtn.setGeometry(QtCore.QRect(20, 230, 141, 51))
        self.SaveSlotBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"

"border-radius:10px;\n"
"font: Bold 12pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveSlotBtn.setIcon(icon)
        self.SaveSlotBtn.setObjectName("SaveSlotBtn")
        self.ImportSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: ImportSlot())
        self.ImportSlotBtn.setGeometry(QtCore.QRect(170, 230, 141, 51))
        self.ImportSlotBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"

"border-radius:10px;\n"
"font: Bold 12pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/Import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ImportSlotBtn.setIcon(icon1)
        self.ImportSlotBtn.setObjectName("ImportSlotBtn")
        self.LoadSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: LoadSlot())
        self.LoadSlotBtn.setGeometry(QtCore.QRect(20, 290, 141, 51))
        self.LoadSlotBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"

"border-radius:10px;\n"
"font: Bold 12pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/LoadSlot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadSlotBtn.setIcon(icon2)
        self.LoadSlotBtn.setObjectName("LoadSlotBtn")
        self.ThemeShopBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: Shop())
        self.ThemeShopBtn.setGeometry(QtCore.QRect(170, 290, 141, 51))
        self.ThemeShopBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"

"border-radius:10px;\n"
"font: Bold 12pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ShoppingCart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ThemeShopBtn.setIcon(icon3)
        self.ThemeShopBtn.setObjectName("ThemeShopBtn")
        self.BorderLabel = QtWidgets.QLabel(self.centralwidget)
        self.BorderLabel.setGeometry(QtCore.QRect(0, 0, 331, 361))
        self.BorderLabel.setStyleSheet("border-style: outset;\n"
"border-width:5px;\n"
"border-radius:10px;\n"
"border-color:rgb(255, 255, 255);\n"
"")
        self.BorderLabel.setText("")
        self.BorderLabel.setObjectName("BorderLabel")
        self.ThemeSaverLogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.ThemeSaverLogoLabel.setGeometry(QtCore.QRect(90, 10, 131, 141))
        self.ThemeSaverLogoLabel.setText("")
        self.ThemeSaverLogoLabel.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ThemeSaverLogo2.png"))
        self.ThemeSaverLogoLabel.setObjectName("ThemeSaverLogoLabel")
        self.ThemeTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.ThemeTextLabel.setGeometry(QtCore.QRect(10, 150, 161, 61))
        self.ThemeTextLabel.setText("")
        self.ThemeTextLabel.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ThemeText.png"))
        self.ThemeTextLabel.setObjectName("ThemeTextLabel")
        self.SaverTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.SaverTextLabel.setGeometry(QtCore.QRect(170, 150, 141, 61))
        self.SaverTextLabel.setText("")
        self.SaverTextLabel.setPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/SaverText.png"))
        self.SaverTextLabel.setObjectName("SaverTextLabel")
        self.BorderLabel.raise_()
        self.SaveSlotBtn.raise_()
        self.ImportSlotBtn.raise_()
        self.LoadSlotBtn.raise_()
        self.ThemeShopBtn.raise_()
        self.ThemeSaverLogoLabel.raise_()
        self.ThemeTextLabel.raise_()
        self.SaverTextLabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def SaveSlot():
                os.system(f"python3 {FolderPath}/GUI/SaveSlotWindow.py &")
        
        def LoadSlot():
                if len(os.listdir(f"{FolderPath}/Slots/")) == 0:
                        NoSlots = QMessageBox() 
                        NoSlots.setText("There Are No Saved Slots :(")
                        run = NoSlots.exec_()
                os.system(f"python3 {FolderPath}/GUI/LoadSlotWindow.py &")

        def ImportSlot():
                DesktopEnvironment = os.environ["DESKTOP_SESSION"]
                if DesktopEnvironment != 'LXDE-pi':
                        ImportFile=QFileDialog.getOpenFileName(self, 'Open file', f'{FolderPath}', 'tar.gz archive (*.tar.gz)')
                        os.system(f"python3 {FolderPath}/GUI/LoadingWindow.py '     Importing Slot...' &")
                        print(ImportFile[0])
                        os.system(f"themesaver import '{ImportFile[0]}'")
                        os.system(f"pkill -f LoadingWindow.py")
                        FinishedImporting = QMessageBox() 
                        FinishedImporting.setText("Finsished Importing Slot")
                        run = FinishedImporting.exec_()
                else:
                        NoLXDE = QMessageBox()
                        NoLXDE.setText("Import Slot is not ready for LXDE yet :(")
                        run = NoLXDE.exec_()

        def Shop():
                NotReady = QMessageBox()
                NotReady.setText("Theme Shop isn't ready yet :(")
                NotReady.exec_()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SaveSlotBtn.setText(_translate("MainWindow", "  Save Slot"))
        self.ImportSlotBtn.setText(_translate("MainWindow", " Import Slot"))
        self.LoadSlotBtn.setText(_translate("MainWindow", " Load Slots"))
        self.ThemeShopBtn.setText(_translate("MainWindow", " Theme Shop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
