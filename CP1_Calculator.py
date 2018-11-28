import math
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLayout, QGridLayout, QSizePolicy, QToolButton
import time


app = QApplication(sys.argv)


class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 25)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QWidget):
    NumDigitButtons = 10
    
    def __init__(self, parent=None):
        
        super(Calculator, self).__init__(parent)
        self.waitingForOperand = True

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        self.digitButtons = []
        
        for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i),
                    self.digitClicked))

        #Creating the buttons
        self.minusButton = self.createButton("SUB", self.subtractOperatorClicked)
        self.plusButton = self.createButton("ADD", self.additiveOperatorClicked)
        self.orButton = self.createButton("OR", self.orOperatorClicked)
        self.complementButton = self.createButton("2s", self.complementOperatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        self.resetButton = self.createButton("RST", self.resetClicked)

        #Creating grid layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        #Digit Buttons
        mainLayout.addWidget(self.display,0,0,1,6)
        mainLayout.addWidget(self.digitButtons[0],5,2)
        mainLayout.addWidget(self.digitButtons[1],2,1)
        mainLayout.addWidget(self.digitButtons[2],2,2)
        mainLayout.addWidget(self.digitButtons[3],2,3)
        mainLayout.addWidget(self.digitButtons[4],3,1)
        mainLayout.addWidget(self.digitButtons[5],3,2)
        mainLayout.addWidget(self.digitButtons[6],3,3)
        mainLayout.addWidget(self.digitButtons[7],4,1)
        mainLayout.addWidget(self.digitButtons[8],4,2)
        mainLayout.addWidget(self.digitButtons[9],4,3)
        
        
        #Adding function buttons
        mainLayout.addWidget(self.complementButton,5,3)
        mainLayout.addWidget(self.minusButton,3,4)
        mainLayout.addWidget(self.plusButton,2,4)
        mainLayout.addWidget(self.orButton,4,4)
        mainLayout.addWidget(self.resetButton,5,4)
        mainLayout.addWidget(self.equalButton,5,1)


        
        self.setLayout(mainLayout)
        self.setWindowTitle("Mini Calculator")

        
        self.equalButton.clicked.connect(self.equalClicked)
        

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())

        if self.display.text() == '0' and digitValue == 0:
            return

        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + str(digitValue))

        
    def subtractOperatorClicked(self):
        self.display.setText(self.display.text()+"-")
    def orOperatorClicked(self):
        self.display.setText(self.display.text()+"|")
    def resetClicked(self):
        self.display.clear()
    def complementOperatorClicked(self):
        self.display.setText(self.display.text()+"'")    
    def additiveOperatorClicked(self):
        self.display.setText(self.display.text()+"+")
    def multiplicativeOperatorClicked(self):
        self.display.setText(self.display.text()+"*")
    def createButton(self, text, member):
        button = Button(text)
        if text!="=":
            button.clicked.connect(member)
        return button

    #Sending inputs pressed to input.txt file by clicking equal button
    def equalClicked(self):
        with open('input.txt', 'w') as f:
            my_text = self.display.text()
            first_val = int(my_text[0])
            first_val = format(first_val, "04b")
            operator = str(my_text[1])
            if operator=="'":
                second_val = "0000"
            else:
                second_val = int(my_text[2])
                second_val = format(second_val, "04b")
            
            
            if operator == "+":
                operator = "00"
            elif operator == "-":
                operator = "01"
            elif operator == "|":
                operator = "10"
            elif operator == "'":
                operator = "11"
            initial_value = "0000"
            
            my_text="{}{}{}{}".format(operator,first_val,second_val,initial_value)
            f.write(my_text)
            
        self.printout()

    #Function to read output.txt file and print it on calculator
    def printout(self):
        time.sleep(20)
        f = open("output.txt", "r")
        contents = f.read()
        value = int(contents,2)
        #If value is greater than 1 digit then reset to 0
        if value > 9:
            value = 0
        self.display.setText(str(value))   


calc = Calculator()
calc.show()
sys.exit(app.exec_())
