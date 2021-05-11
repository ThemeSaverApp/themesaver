from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget
import os

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        FolderPath = f"{os.environ['HOME']}/ThemeSaver"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(264, 177)
        MainWindow.setMaximumSize(QtCore.QSize(264, 177))
        MainWindow.setStyleSheet("background-color: rgb(247, 137, 20);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/ThemeSaverLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SlotNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.SlotNameInput.setGeometry(QtCore.QRect(20, 60, 221, 51))
        self.SlotNameInput.setStyleSheet("font: 15pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"border-style : dashed;\n"
"border : 4px solid white;\n"
"border-radius: 10px;\n"
"background-color: rgb(255, 255, 255);")
        self.SlotNameInput.setInputMask("")
        self.SlotNameInput.setText("")
        self.SlotNameInput.setObjectName("SlotNameInput")
        self.EnterSlotNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.EnterSlotNameLabel.setGeometry(QtCore.QRect(40, 10, 181, 41))
        self.EnterSlotNameLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"font: Bold 15pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        self.EnterSlotNameLabel.setObjectName("EnterSlotNameLabel")
        self.ConfirmBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: SaveSlot())
        self.ConfirmBtn.setGeometry(QtCore.QRect(70, 120, 121, 41))
        self.ConfirmBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12 10pt \"Source Code Pro\";\n"
"border-radius:10px;\n"
"font: Bold 12pt \"Ubuntu\";\n"
"color: rgb(247, 137, 20);\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{FolderPath}/GUI/Icons/Confirm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ConfirmBtn.setIcon(icon)
        self.ConfirmBtn.setIconSize(QtCore.QSize(21, 21))
        self.ConfirmBtn.setFlat(False)
        self.ConfirmBtn.setObjectName("ConfirmBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def SaveSlot():
                SlotName = self.SlotNameInput.text()
                if SlotName.strip() == "":
                        EmptyName = QMessageBox()
                        EmptyName.setText('Enter Valid Slot Name')
                        run = EmptyName.exec_()
                else:
                        if os.path.isdir(f"{FolderPath}/Slots/{SlotName}"):
                                Overwrite = QMessageBox.question(self, 'Overwrite ?', 'A slot with that name already exists, Do you want to overwrite it ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                if Overwrite == QMessageBox.Yes:  
                                        os.system(f"rm -r ~/ThemeSaver/Slots/'{SlotName}'")
                                        os.system(f"themesaver save '{SlotName}'")     
                                        
                        else:
                                os.system(f"themesaver save '{SlotName}'")
                
                FinishedSaving = QMessageBox()
                FinishedSaving.setText("Finished Saving Theme")
                run = FinishedSaving.exec_()
                exit()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SaveSlot"))
        self.EnterSlotNameLabel.setText(_translate("MainWindow", "  Enter Slot Name:  "))
        self.ConfirmBtn.setText(_translate("MainWindow", " Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
