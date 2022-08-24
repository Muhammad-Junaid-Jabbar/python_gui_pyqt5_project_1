# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from fileinput import filename
from fnmatch import fnmatchcase
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
def calculator_function(ux,trigger_ = 0.002,sensibility_down = 20,sensibility_up=30):
    if abs(ux) < trigger_:
        return 0 
    else:
        if ux <= 0:
            log1= ((np.log(-ux)) / sensibility_down) 
            return log1
        else:
            log2 = (-np.log(ux)) / sensibility_up
            return log2

class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("gui.ui",self)

        self.setWindowTitle("PyQt5 & Matplotlib GUI")

        #file open button
        self.pushButton_file_open.clicked.connect(self.clicker)
        
        #submit button
        self.pushButton_submit.clicked.connect(self.update_graph)

        #graph canvas
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def clicker(self):
        global filename 
        fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*)")  
        filename = str(fname[0])
        print(filename)

    def update_graph(self):
        try:
            trigger_1 = float(self.lineEdit_trigger.text())
            # print(trigger_)
        except:
            self.lineEdit_trigger.setText('0')
            trigger_1 = float(self.lineEdit_trigger.text())
            # print("error")
        
        try:
            sensibility_up_1 = float(self.lineEdit_sensibility_up.text())
            # print(trigger_)
        except:
            self.lineEdit_sensibility_up.setText('0')
            sensibility_up_1 = float(self.lineEdit_sensibility_up.text())
            # print("error")
        
        try:
            sensibility_down_1 = float(self.lineEdit_sensibility_down.text())
            # print(trigger_)
        except:
            self.lineEdit_sensibility_down.setText('0')
            sensibility_down_1 = float(self.lineEdit_sensibility_down.text())
            # print("error")
        
        df = pd.read_excel(str(filename))
        df2 =df.copy()
        df2 = df2[['date','X']]
        df2['BDT'] = df2['X'].apply(lambda x: calculator_function(x,trigger_ = trigger_1,sensibility_down = sensibility_down_1,sensibility_up=sensibility_up_1))
        t = df2['date']
        signal_1 = df2['X']
        signal_2 = df2['BDT']

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, signal_1)
        self.MplWidget.canvas.axes.plot(t, signal_2)
        self.MplWidget.canvas.axes.legend(('X', 'BDT'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('X - BDT Signal')
        self.MplWidget.canvas.axes.set_xlabel('date')
        self.MplWidget.canvas.draw()
        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()