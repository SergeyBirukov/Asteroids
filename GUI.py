from PyQt5 import QtGui, QtCore, QtWidgets
import random

app = QtWidgets.QApplication([])
class MyWindow(QtWidgets.QWidget):
    def __init__(self, text, text2, text3, text4):
        QtWidgets.QWidget.__init__(self)
        self.text2 = text2
        self.text3 = text3
        self.text4 = text4
        self.textArray = [text, text2, text3, text4]
        self.number = 0
        self.button = QtWidgets.QPushButton(text2, parent=self)
        self.button.show()
        self.button.setText(text)
        self.button2 = QtWidgets.QPushButton(text2, parent=self)
        self.button2.hide()
        self.button2.move(0, 50)
        self.button3 = QtWidgets.QPushButton(text2, parent=self)
        self.button3.move(0, 100)
        self.button3.hide()
        self.button4 = QtWidgets.QPushButton(text2, parent=self)
        self.button4.move(0, 150)
        self.button4.hide()
        self.buttonArray = [self.button, self.button2, self.button3, self.button4]
        for i in range(4):
            self.buttonArray[i].clicked.connect(self.pressed)

    def pressed(self):

        self.number = self.number + 1
        if (self.number == 1):
            self.button.setText(self.text2)
            self.button2.show()
            self.resize(100, 100)
        if (self.number == 2):
            self.button.setText(self.text3)
            self.button2.setText(self.text3)
            self.button3.show()
            self.button3.setText(self.text3)
            self.resize(100, 150)
        if (self.number == 3):
            # self.button.setText(self.text4)
            # self.button2.setText(self.text4)
            # self.button3.setText(self.text4)
            for i in range(3):
                self.buttonArray[i].hide()
            self.button4.show()
            self.button4.setText(self.text4)
            self.button4.resize(1000, 1000)
            self.resize(1000, 1000)
        if (self.number > 3):
            # self.resize(150, 200)
            for i in range(4):
                random1 = random.randrange(0, 700, 1)
                random2 = random.randrange(0, 700, 1)
                self.buttonArray[i].setText(self.textArray[(self.number + i) % 4].upper())
                self.buttonArray[i].setFont(QFont('Times', 20))
                self.buttonArray[i].move(random1, random2)
                random1 = random.randrange(150, 300, 1)
                random2 = random.randrange(10, 300, 1)
                self.buttonArray[i].resize(random1, random2)
                self.buttonArray[i].show()


button = MyWindow("Push me", "And then just touch me", "'Til I can get my", "SATISFACTION")
button.show()
app.exec()