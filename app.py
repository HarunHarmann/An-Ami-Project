import sys
import PyQt6
from PyQt6 import sip
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowFlag(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint)
        
        #Start Amiy button.
        button = QPushButton("CLICK HERE!",self)
        button.setGeometry(400, 300, 200, 200)
        button.setStyleSheet("border : 0; background: transparent; color: beige;font: bold;font-family: Bauhaus 93;font-size: 25px")                     
        button.pressed.connect(self.start_process)
        button.pressed.connect(lambda: button.hide())
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      
        self.anim = QPropertyAnimation(button, b"pos")
        self.anim.setStartValue(QRect(200, 200, 600, 600))
        self.anim.setEndValue(QPoint(90,177))
        self.anim.setDuration(1500)
        self.anim.start()

        #Exit program.
        exitButton = QPushButton("X",self) 
        exitButton.setStyleSheet("border : 0; background: transparent; color: purple;font: bold;font-family: Bauhaus 93;font-size: 35px")  
        exitButton.move(330,10)
        exitButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        exitButton.pressed.connect(sys.exit)
    

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos )
        self.dragPos = event.globalPosition().toPoint()
        event.accept()

    def initUI(self):
        self.setWindowFlags(PyQt6.QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(QSize(400,600))
        self.round_corners()
        
    def round_corners(self):
        radius = 20
        path = PyQt6.QtGui.QPainterPath()
        path.addRoundedRect(PyQt6.QtCore.QRectF(self.rect()), radius, radius)
        mask = PyQt6.QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def start_process(self):
        self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.p.startDetached("python", ['C:\\Users\\ACER\\Documents\\GitHub\\Ami\\main.py'])

        # self.label = QLabel(self)
        # self.movie = QMovie("animation.gif")
        # self.label.setMovie(self.movie)
        # self.label.setGeometry(PyQt6.QtCore.QRect(25, 25, 200, 200))
        # self.label.setMinimumSize(PyQt6.QtCore.QSize(250, 250))
        # self.label.move(1,420)
          
        # self.movie.start() 
        # self.label.show()

        # self.label2 = QLabel(self)

         
        # self.movie2 = QMovie("animation.gif")
        # self.label2.setMovie(self.movie)
        # self.label2.setGeometry(PyQt6.QtCore.QRect(25, 25, 200, 200))
        # self.label2.setMinimumSize(PyQt6.QtCore.QSize(250, 250))
     
        
        # self.movie2.start()
        # self.label2.move(270,50)
        # self.label2.show()
        # wid = QWidget()
        # layout = QGridLayout() 
        # layout.addWidget("animation.gif")

        
        
        
   
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pic = ''' MainWindow
{
background-image:url(C:/Users/ACER/Documents/GitHub/Ami/background-1copy.jpg);
background-repeat: no repeat;
background-position: center;
}
'''
app = QApplication(sys.argv)
app.setStyleSheet(pic)

window = MainWindow()
window.show()

app.setWindowIcon(QIcon('icon.ico'))
app.exec()
