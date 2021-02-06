import sys
import csv
import os
import serial
import time
import io
from pathlib import Path
import shutil
from datetime import datetime
# datetime object containing current date and time
# now = datetime.now()
# dd/mm/YY H:M:S
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from make_pattern_visual import *
import gui_main_rev02
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import numpy as np
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

# NOT BEING USED!!!!

class CalibratePlate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Plate Coordinate System Calibration')
        self.setGeometry(300,70,750,900)

        self.xy_off = None
        self.phi = None

        self.UI()

        

        self.show()
        self.vidFunc()



    def UI(self):
        self.widgets()
        #self.layouts()
        #self.vidWidgets()
        self.jogWidgets()
        

        self.ptEntryWidgets()
        self.ptEntyLayouts()
        self.jogLayouts()
        self.endLayouts()
        self.jogWidgets()
        #self.widgets()
        #self.layouts()
        

    def widgets(self):
        #self.control_bt = QPushButton()
        #self.control_bt.clicked.connect(self.start_webcam)
        self.vid_lab = QLabel()
        #self.vis_img.setPixmap(QPixmap(self.temp_img_path))
    

    def vidFunc(self):
        cap = cv2.VideoCapture(1)

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    

    def jogWidgets(self):
        ###################### GRBL JOG ###############################
        self.jog_font = QFont('Arial',16)
        
        self.px_btn = QPushButton('+X')
        self.px_btn.clicked.connect(self.pxFunc)
        self.px_btn.setFont(self.jog_font)

        self.mx_btn = QPushButton('-X')
        self.mx_btn.clicked.connect(self.mxFunc)
        self.mx_btn.setFont(self.jog_font)

        self.py_btn = QPushButton('+Y')
        self.py_btn.clicked.connect(self.pyFunc)
        self.py_btn.setFont(self.jog_font)

        self.my_btn = QPushButton('-Y')
        self.my_btn.clicked.connect(self.myFunc)
        self.my_btn.setFont(self.jog_font)

        self.pz_btn = QPushButton('+Z')
        self.pz_btn.clicked.connect(self.pzFunc)
        self.pz_btn.setFont(self.jog_font)

        self.mz_btn = QPushButton('-Z')
        self.mz_btn.clicked.connect(self.mzFunc)
        self.mz_btn.setFont(self.jog_font)

        self.jog_feed_entry = QLineEdit()
        self.jog_feed_label = QLabel('Feed Rate [mm/min]:')

        self.jog_dist_entry = QLineEdit()
        self.jog_dist_label = QLabel('Jog Distance [mm]:')
        
        self.n1 = QLabel('')
        self.n2 = QLabel('')
        self.n3 = QLabel('')
        self.n4 = QLabel('')
        self.n5 = QLabel('')
        self.n6 = QLabel('')
        self.n7 = QLabel('')

    def pxFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21X' +  dist + 'F' + fr + '\n'

            try:
                self.terminal_txt.append(Gcode_str)
                print(self.ser)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def mxFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21X-' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def pyFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21Y' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def myFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21Y-' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def pzFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21Z' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def mzFunc(self):
        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()
        if len(fr) > 0 and fr.isnumeric() and len(dist) > 0 and dist.isnumeric():
            Gcode_str = '$J=G91G21Z-' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def ptEntryWidgets(self):
        self.x1_lb = QLabel('X1')
        self.y1_lb = QLabel('Y1')
        self.x1_entry = QLineEdit()
        self.y1_entry = QLineEdit()
        self.record_pt1_btn = QPushButton('Record Position')
        #self.record_pt1_btn.clicked.connect(self.recordPt1(self))

        self.x2_lb = QLabel('X2')
        self.y2_lb = QLabel('Y2')
        self.x2_entry = QLineEdit()
        self.y2_entry = QLineEdit()
        self.record_pt2_btn = QPushButton('Record Position')
        #self.record_pt2_btn.clicked.connect(self.recordPt2(self))

    def ptEntyLayouts(self):
        self.pt_group1 = QGroupBox()
        self.pt_group2 = QGroupBox()

        self.pt_hbox1 = QHBoxLayout()
        self.pt_hbox2 = QHBoxLayout()
        self.pt_hbox3 = QHBoxLayout()
        self.pt_hbox4 = QHBoxLayout()
        self.pt_hbox5 = QHBoxLayout()
        self.pt_hbox6 = QHBoxLayout()

        self.pt_vbox1 = QVBoxLayout()
        self.pt_vbox2 = QVBoxLayout()
        self.pt_vbox3 = QVBoxLayout()

        self.pt_hbox1.addWidget(self.x1_lb)
        self.pt_hbox1.addWidget(self.x1_entry)
        self.pt_hbox2.addWidget(self.y1_lb)
        self.pt_hbox2.addWidget(self.y1_entry)
        
        self.pt_hbox3.addWidget(self.x2_lb)
        self.pt_hbox3.addWidget(self.x2_entry)
        self.pt_hbox4.addWidget(self.y2_lb)
        self.pt_hbox4.addWidget(self.y2_entry)

        self.pt_vbox1.addLayout(self.pt_hbox1)
        self.pt_vbox1.addLayout(self.pt_hbox2)
        self.pt_vbox1.addWidget(self.record_pt1_btn)
        self.pt_group1.setLayout(self.pt_vbox1)

        self.pt_vbox2.addLayout(self.pt_hbox3)
        self.pt_vbox2.addLayout(self.pt_hbox4)
        self.pt_vbox2.addWidget(self.record_pt2_btn)
        self.pt_group2.setLayout(self.pt_vbox2)

        self.pt_vbox3.addWidget(self.pt_group1)
        self.pt_vbox3.addWidget(self.pt_group2)
    
    
    def jogLayouts(self):
        
        ########################## Grid Layout ################################
        self.jog_grid = QGridLayout()
        self.jog_group = QGroupBox('Jog Machine Controls')
        self.jog_hbox1 = QHBoxLayout()
        self.jog_hbox2 = QHBoxLayout()
        self.jog_hbox3 = QHBoxLayout()
        self.jog_vbox1 = QVBoxLayout()
        self.jog_vbox2 = QVBoxLayout()
        self.jog_vbox3 = QVBoxLayout()
        self.jog_vbox4 = QVBoxLayout()

        self.jog_grid.addWidget(self.n1,0,0)
        self.jog_grid.addWidget(self.py_btn,0,1)
        self.jog_grid.addWidget(self.n2,0,2)
        self.jog_grid.addWidget(self.pz_btn,0,4)
        self.jog_grid.addWidget(self.mx_btn,1,0)
        self.jog_grid.addWidget(self.n3,1,1)
        self.jog_grid.addWidget(self.px_btn,1,2)
        self.jog_grid.addWidget(self.n4,1,3)
        self.jog_grid.addWidget(self.n5,2,0)  
        self.jog_grid.addWidget(self.my_btn,2,1)
        self.jog_grid.addWidget(self.n6,2,2)
        self.jog_grid.addWidget(self.mz_btn,2,4)

        # feed rate and distance
        self.jog_hbox1.addWidget(self.jog_feed_label)
        self.jog_hbox1.addStretch()
        self.jog_hbox1.addWidget(self.jog_feed_entry)

        self.jog_hbox2.addWidget(self.jog_dist_label)
        self.jog_hbox2.addStretch()
        self.jog_hbox2.addWidget(self.jog_dist_entry)

        #self.jog_vbox1.addWidget(self.ctrl_btn_group)
        self.jog_vbox1.addLayout(self.jog_grid)
        self.jog_vbox1.addWidget(self.n7)
        self.jog_vbox1.addLayout(self.jog_hbox1)
        self.jog_vbox1.addLayout(self.jog_hbox2)
        self.jog_vbox1.addStretch()

        self.jog_group.setLayout(self.jog_vbox1)
        self.jog_vbox2.addWidget(self.jog_group)

        #self.jog_hbox3.addLayout(self.jog_vbox2)

        #self.setLayout(self.jog_hbox3)

    def endLayouts(self):
        self.end_vbox1 = QVBoxLayout()

        #self.end_vbox1.addLayout(self.jog_vbox2)
        #self.end_vbox1.addLayout(self.pt_vbox3)
        #self.end_vbox1.addWidget(self.vid_disp)
        self.end_vbox1.addWidget(self.vid_lab)

        self.setLayout(self.end_vbox1)

    def btnClick(self):
        print('HELL YA')


def main():
    App = QApplication(sys.argv)
    window = CalibratePlate()
    #window.show()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()
