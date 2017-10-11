#Gregor Lorencak, Bodo Weber
from PyQt5.QtCore import Qt, QRect, QLine, QTimer

from PyQt5.QtGui import QColor, QPainter, QPen ,QImage

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import math
import time
ballPos=(440,400)
ballSpeed=(0,0)

class Punkt:
    def __init__(self,Xachse,Yachse):
        self.x=Xachse
        self.y=Yachse
    def __str__(self):
        s ='('+str(self.x)+', '+str(self.y)+')'
        return s
    def __lt__(self, other):
        return self.x< other.x or self.x==other.x and self.y<other.y
    def abstand(self,other):
        a=abs(self.x-other.x)
        b=abs(self.y-other.y)
        c=a**2+b**2
        return math.sqrt(c)


class MyRenderAreaFledermaus1(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.imageFledermaus1 = QImage('Fledermaus.png').scaled(100,100)
        self.F1x = 100
        self.F1y = 100

        self.imageFledermaus2 = QImage('Fledermaus.png').scaled(100, 100)
        self.F2x = 800
        self.F2y = 200

        self.imageBalloon = QImage('balloon.png').scaled(100, 100)
        self.Bx = 440
        self.By = 400



    def Kollision(self):
        if Punkt(self.Bx, self.By).abstand(Punkt(self.F2x, self.F2y))<100:
            MyRenderAreaFledermaus1.Gravity(self,(self.Bx-self.F2x,self.By-self.F2y))
        if Punkt(self.Bx, self.By).abstand(Punkt(self.F1x, self.F1y))<100:
            MyRenderAreaFledermaus1.Gravity(self, (self.Bx - self.F1x, self.By - self.F1y))

    def Gravity(self,v=(0,0)):
        global ballSpeed
        global ballPos
        ballSpeed = (ballSpeed[0]*0.9 + v[0]/2, ballSpeed[1]*0.7 + v[1]/2)
        ballPos = (ballPos[0] + ballSpeed[0], max(0, (ballPos[1] + ballSpeed[1])))
        if 50 < ballPos[0] < 900:
            ballSpeed = (ballSpeed[0], ballSpeed[1]-1)
        else:
            ballSpeed = (-ballSpeed[0], ballSpeed[1] - 1)
        self.Bx=ballPos[0]
        self.By=ballPos[1]


    def timer_Funktion(self):
        pass
        #self.time_no+=1
        #if self.time_no%10==0:
         #   MyRenderAreaFledermaus1.Gravity(self,self.By)


    def keyPressEvent(self,e):
        if e.key() ==  Qt.Key_Up:
            self.F1y -= 10
            if self.F1y<0:
                self.F1y+=10
        if e.key()  == Qt.Key_Down:
            self.F1y += 10
            if self.F1y>700:
                self.F1y-=10
        if e.key() == Qt.Key_Left:
            self.F1x -= 10
            if self.F1x<0:
                self.F1x+=10
        if e.key() == Qt.Key_Right:
            self.F1x += 10
            if self.F1x>400:
                self.F1x-=10
        if e.key() ==  Qt.Key_W:
            self.F2y -= 10
            if self.F2y<0:
                self.F2y+=10
        if e.key()  == Qt.Key_S:
            self.F2y += 10
            if self.F2y>700:
                self.F2y-=10
        if e.key() == Qt.Key_A:
            self.F2x -= 10
            if self.F2x<500:
                self.F2x+=10
        if e.key() == Qt.Key_D:
            self.F2x += 10
            if self.F2x>900:
                self.F2x-=10
        MyRenderAreaFledermaus1.Kollision(self)
        MyRenderAreaFledermaus1.Gravity(self)
        self.update()


    def paintEvent(self,e):
        painter = QPainter(self)
        painter.setBrush(QColor('yellow'))
        painter.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRect(rect)
        pen = QPen(QColor('black'))
        pen.setWidth(10)
        painter.setPen(pen)
        line = QLine(500,250,500,0)
        painter.drawLine(line)
        painter.drawImage(self.F1x, self.F1y, self.imageFledermaus1)
        painter.drawImage(self.F2x, self.F2y, self.imageFledermaus2)
        painter.drawImage(self.Bx, self.By, self.imageBalloon)


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300,200,1000,800)


        renderareaF1= MyRenderAreaFledermaus1(self)
        self.setCentralWidget(renderareaF1)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction('Exit', self.close)
        viewMenu = menubar.addMenu("&View")


        statusbar = self.statusBar()
        statusbar.showMessage('Willkommen', 5000)

        self.show()

app = QApplication([])
gui = MyMainWindow()
exit(app.exec_())
