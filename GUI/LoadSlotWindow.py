from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir

class Ui_LoadSlotWindow(QWidget):
    def setupUi(self, LoadSlotWindow):
        global FolderPath
        FolderPath = f"{os.environ['HOME']}/ThemeSaver"
        LoadSlotWindow.setObjectName("LoadSlotWindow")
        LoadSlotWindow.resize(620, 418)
        LoadSlotWindow.setMaximumSize(QtCore.QSize(620, 418))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ThemeSaverLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoadSlotWindow.setWindowIcon(icon)
        LoadSlotWindow.setStyleSheet("background-color: rgb(247, 137, 20);")
        self.centralwidget = QtWidgets.QWidget(LoadSlotWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Screenshot = QtWidgets.QLabel(self.centralwidget)
        self.Screenshot.setGeometry(QtCore.QRect(70, 70, 481, 271))
        self.Screenshot.setStyleSheet("border-radius: 10px;\n"
"border: 5px solid white;")
        self.Screenshot.setText("")
        self.Screenshot.setObjectName("Screenshot")
        self.SlotName = QtWidgets.QLabel(self.centralwidget)
        self.SlotName.setGeometry(QtCore.QRect(110, 10, 401, 51))
        self.SlotName.setAlignment(QtCore.Qt.AlignCenter)
        self.SlotName.setStyleSheet("font: Bold 13pt \"Ubuntu\";\n"
"border-radius:10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(247, 137, 20);")
        self.SlotName.setObjectName("SlotName")
        self.BackButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: BackBtn())
        self.BackButton.setGeometry(QtCore.QRect(10, 180, 50, 50))
        self.BackButton.setStyleSheet(f"border-image : url({FolderPath}/GUI/Icons/BackArrow.png);")
        self.BackButton.setText("")
        self.BackButton.setFlat(True)
        self.BackButton.setObjectName("BackButton")
        self.ForwardButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: ForwardBtn())
        self.ForwardButton.setGeometry(QtCore.QRect(560, 180, 50, 50))
        self.ForwardButton.setStyleSheet(f"border-image : url({FolderPath}/GUI/Icons/ForwardArrow.png);")
        self.ForwardButton.setText("")
        self.ForwardButton.setFlat(True)
        self.ForwardButton.setObjectName("ForwardButton")
        self.LoadSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: LoadBtn())
        self.LoadSlotBtn.setGeometry(QtCore.QRect(260, 360, 121, 41))
        self.LoadSlotBtn.setStyleSheet("font: Bold 13pt \"Ubuntu\";\n"
"border-radius:10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(247, 137, 20);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/LoadSlot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadSlotBtn.setIcon(icon1)
        self.LoadSlotBtn.setIconSize(QtCore.QSize(20, 20))
        self.LoadSlotBtn.setFlat(True)
        self.LoadSlotBtn.setObjectName("LoadSlotBtn")
        self.DeleteSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: DelBtn())
        self.DeleteSlotBtn.setGeometry(QtCore.QRect(410, 360, 131, 41))
        self.DeleteSlotBtn.setStyleSheet("font: Bold 13pt \"Ubuntu\";\n"
"border-radius:10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(247, 137, 20);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/Delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteSlotBtn.setIcon(icon2)
        self.DeleteSlotBtn.setIconSize(QtCore.QSize(20, 20))
        self.DeleteSlotBtn.setFlat(True)
        self.DeleteSlotBtn.setObjectName("DeleteSlotBtn")
        self.ExportSlotBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: ExportBtn())
        self.ExportSlotBtn.setGeometry(QtCore.QRect(100, 360, 131, 41))
        self.ExportSlotBtn.setStyleSheet("font: Bold 13pt \"Ubuntu\";\n"
"border-radius:10px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(247, 137, 20);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/Export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExportSlotBtn.setIcon(icon3)
        self.ExportSlotBtn.setIconSize(QtCore.QSize(20, 20))
        self.ExportSlotBtn.setFlat(True)
        self.ExportSlotBtn.setObjectName("ExportSlotBtn")
        LoadSlotWindow.setCentralWidget(self.centralwidget)

        global SlotNames
        SlotNames = os.listdir(f"{FolderPath}/Slots/")
        global CurrentSlot
        CurrentSlot = 0

        def ForwardBtn():
                global CurrentSlot
                if not CurrentSlot + 1 == len(SlotNames):
                        CurrentSlot += 1
                        self.SlotName.setText(SlotNames[CurrentSlot])
                        self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{SlotNames[CurrentSlot]}/Screenshot.png"))

        def BackBtn():
                global CurrentSlot
                if not CurrentSlot == 0:
                        CurrentSlot -= 1
                        self.SlotName.setText(SlotNames[CurrentSlot])
                        self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{SlotNames[CurrentSlot]}/Screenshot.png"))

        def DelBtn():
                global CurrentSlot
                os.system(f"rm -r {FolderPath}/Slots/'{SlotNames[CurrentSlot]}'")
                FinishedDeleting = QMessageBox()
                FinishedDeleting.setText(f"Finished Deleting The ''{SlotNames[CurrentSlot]}'' Slot")
                run = FinishedDeleting.exec_()
                exit()

        def LoadBtn():
                global CurrentSlot
                os.system(f"themesaver load '{SlotNames[CurrentSlot]}'")
                FinishedLoading = QMessageBox()
                FinishedLoading.setText(f"Finished Loading The '{SlotNames[CurrentSlot]}' Slot")
                run = FinishedLoading.exec_()

        def ExportBtn():
                global CurrentSlot
                DesktopEnvironment = os.environ["DESKTOP_SESSION"]
                if DesktopEnvironment != 'LXDE-pi':
                        ExportPath = QFileDialog.getExistingDirectory(self, 'Open file', f'{FolderPath}')
                        os.system(f"python3 {FolderPath}/GUI/LoadingWindow.py '     Exporting Slot...' &")
                        os.system(f"themesaver export '{SlotNames[CurrentSlot]}' {ExportPath}")
                        os.system("pkill -f LoadingWindow.py")
                        FinishedExporting = QMessageBox()
                        FinishedExporting.setText(f"Finished Exporting Slot To {ExportPath}/'{SlotNames[CurrentSlot]}'.tar.gz")
                        run = FinishedExporting.exec_()
                else:
                        NoLXDE = QMessageBox()
                        NoLXDE.setText("Import Slot is not ready for LXDE yet :(")
                        run = NoLXDE.exec_()

        self.retranslateUi(LoadSlotWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadSlotWindow)

    def retranslateUi(self, LoadSlotWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadSlotWindow.setWindowTitle(_translate("LoadSlotWindow", "LoadSlotWindow"))
        self.SlotName.setText(_translate("LoadSlotWindow", SlotNames[0]))
        self.Screenshot.setPixmap(QtGui.QPixmap(f"{FolderPath}/Slots/{SlotNames[0]}/Screenshot.png"))
        self.LoadSlotBtn.setText(_translate("LoadSlotWindow", " Load Slot"))
        self.DeleteSlotBtn.setText(_translate("LoadSlotWindow", " Delete Slot"))
        self.ExportSlotBtn.setText(_translate("LoadSlotWindow", " Export Slot"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoadSlotWindow = QtWidgets.QMainWindow()
    ui = Ui_LoadSlotWindow()
    ui.setupUi(LoadSlotWindow)
    LoadSlotWindow.show()
    sys.exit(app.exec_())
