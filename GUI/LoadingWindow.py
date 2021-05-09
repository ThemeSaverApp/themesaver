import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        FolderPath = f"{os.environ['HOME']}/ThemeSaver"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(331, 81)
        MainWindow.setMaximumSize(331, 81)
        MainWindow.setStyleSheet("background-color: rgb(247, 137, 20);")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 60, 60))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 20, 241, 41))
        self.label_2.setStyleSheet("color: rgb(247, 137, 20);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"font: Bold 15pt \"Ubuntu\";\n"
"")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.movie = QMovie(f"{FolderPath}/GUI/Icons/Loading.gif")
        self.label.setMovie(self.movie)

        self.startAnimation()
  
    def startAnimation(self):
        self.movie.start()
  

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Loading"))
        self.label_2.setText(_translate("MainWindow", f"{sys.argv[1]}"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
