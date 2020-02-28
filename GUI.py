from PyQt4 import QtCore, QtGui
#from PyQt4.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
import sys
from PyQt4.QtGui import QPixmap

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setGeometry(10,10,800,480)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Speero")  
           

        login_widget = LoginWidget(self)
        #login_widget.button.clicked.connect(self.login)
        self.central_widget.addWidget(login_widget)

    def login(self):
        logged_in_widget = LoggedWidget(self)
        self.central_widget.addWidget(logged_in_widget)
        self.central_widget.setCurrentWidget(logged_in_widget)
    


class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0);
        layout.setContentsMargins(1, 1, 1, 1);
        
        # Add start demo button
        self.buttonG = QtGui.QPushButton('Start Demo', checkable=False)
        self.buttonG.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                QtGui.QSizePolicy.Expanding)
        self.buttonG.setStyleSheet("QPushButton {background-image: url(/home/harminder/Downloads/start_demo.jpg); border: none}"
                                    "QPushButton:pressed {background-image: url(/home/harminder/Downloads/grey.png); border: none}")
        #self.buttonG.setStyleSheet("QPushButton#DCButton:checked {color: black; background-color: green; border: none; }")
        layout.addWidget(self.buttonG)

        self.buttonD = QtGui.QPushButton('BLACH')
        self.buttonD.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                QtGui.QSizePolicy.Expanding)
        self.buttonD.setStyleSheet("background-image: url(/home/harminder/Downloads/start_demo.jpg);")
        layout.addWidget(self.buttonD)

        # Add logo 
        self.logo = QtGui.QPixmap("/home/harminder/Downloads/logo.png")
        self.logo = self.logo.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label_logo = QtGui.QLabel()
        #self.label_logo.setGeometry(20,20,10,10)
        self.label_logo.setPixmap(self.logo) 
        #self.label_logo.setStyleSheet("background-color: rgb(250,192,191);")
        layout.addWidget(self.label_logo)


        
    
        self.setLayout(layout)

        #self.buttonG.clicked.connect(self.parent().login)
        # you might want to do self.button.click.connect(self.parent().login) here


class LoggedWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoggedWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel('logged in!')
        layout.addWidget(self.label)

        self.button1 = QtGui.QPushButton('Button 1')
        layout.addWidget(self.button1)

        self.button2 = QtGui.QPushButton('Button 2')
        layout.addWidget(self.button2)

        self.setLayout(layout)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()