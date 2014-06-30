'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'


from matplotlib.backends.qt4_compat import QtGui, QtCore
from pyXPD.userapi.Motor_commands import *
import sys


class Motor(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("XPD Motor Controls")
        #Get all the motor names here, essentially load up the motorD

        toplayout=QtGui.QGridLayout()
        number_of_motors_ = len(motorD)
        titles = ['Name', 'Status', 'Position Read Back', 'Position', 'Step', 'Stop']
        fields_per_motor = len(titles)

        i=1
        for n, title in enumerate(titles):
            toplayout.addWidget(QtGui.QLabel(title), 0, n)
        for motor in motorD:

            #set the motor name
            toplayout.addWidget(QtGui.QLabel(motor), i, 0)

            #How do I get this to update automaticly? Also needs if statement with real words
            motor_stat = 'MOTOR STATUS HERE'
            toplayout.addWidget(QtGui.QLabel(motor_stat), i, 1)
            position_read_back='POSITION VALUE HERE'
            toplayout.addWidget(QtGui.QLabel(position_read_back), i, 2)

            #Spin box for setting the position
            user_position=QtGui.QDoubleSpinBox()
            user_position.setMaximum(motorD[motor]['high'])
            user_position.setMinimum(motorD[motor]['low'])
            #this needs to update
            user_position.setValue(caget(motorD[motor]['pv']+'.VAL'))
            user_position.setSuffix(motorD[motor]['EGU'])
            user_position.valueChanged.connect(lambda y=user_position.value, x=motor : self.new_position)

            toplayout.addWidget(user_position)

            #step box
            step = QtGui.QDoubleSpinBox()
            step.setMinimum(motorD[motor]['res'])
            step.setValue(.5)
            step.valueChanged.connect(user_position.setSingleStep)
            toplayout.addWidget(step)

            #stop button
            stop_btn=QtGui.QPushButton("STOP")
            stop_btn.clicked.connect(lambda x=motor: self.gui_stop(x))
            toplayout.addWidget(stop_btn)






            i+=1
        self.setLayout(toplayout)
        self.show()

    @QtCore.Slot(float)
    def sl_update_position(self, position):
        pass

    @QtCore.Slot()
    def gui_stop(self, motorID):
        print motorID
        stop(motorID)

    @QtCore.Slot(float)
    def new_position(self, pos, motor):
        AAA
        print 'start motor move'
        move(motor, pos)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Motor()
    window.show()
    sys.exit(app.exec_())