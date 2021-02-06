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
from pattern_objs01 import *
#from camera_disp01 import *
import camera_disp01
#import plate_cal_window01
import math
import numpy as np
import cv2
from PIL import Image as im 
import fu

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Alpha.IRUS')
        self.setGeometry(200,50,1500,950)

        self.master_path = 'C:/Users/markp/Documents/Alpha.IRUS/Alpha.IRUS - Operations'

        self.UI()
        self.show()
        
        """ self.master_path = 'C:/Users/markp/OneDrive/Documents/AME 498 - Sr Design/First Draft Code/Alpha_IRUS'
        self.pattern_path = self.master_path + '/Torque Patterns'
        self.doc_path = self.master_path + '/Operation Documentation'
        try:
            Path(self.pattern_path).mkdir()
        except FileExistsError:
            print('The Patter Already Exists 1') 
        
        try:
            Path(self.doc_path).mkdir()
        except FileExistsError:
            print('The Patter Already Exists 2')  """

        self.url = '' 
        self.pattern_dict = {}
        self.check_connect = 0
        
        #self.cap = cv2.VideoCapture(1)
        
    def UI(self):
        self.toolBar()
        # TAB WIDGETS
        self.headTabWidgets()
        self.adminTabWidgets()
        self.PreRunTabWidgets()
        # WIDGETS 
        self.uploadFileWidgets()
        self.patternListWidgets()
        self.modPatternWidgets()
        self.opPatternViewWidgets()
        self.PreRunDocWidgets()
        self.grblMainWidgets()
        self.gcodeTabWidgets()
        self.popPatternList()
        self.ptEntryWidgets()
        
        # LAYOUTS
        self.ptEntyLayouts()
        self.layoutsMain()
        self.uploadFileLayout()
        self.patternListLayout()
        self.OperateTabLayout()
        self.modifyPatternTabLayout()
        self.operatorDocLayout()
        self.termTabLayout()
        self.gcodeTabLayout()
        self.layoutsEnd()
        
        self.setNullPlot()
        #self.layouts()
        
    def toolBar(self):
        self.tb = self.addToolBar('Tool Bar')
        # makes the button name appear under icon
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) 
        ############################# TOOLBAR BUTTONS ##############################
        #--------------------------------------------------------------------------#
        ############################# WIKI's #######################################
          

        self.op_procedure = QAction(QIcon('icons/null.png'),'Operation Procedure',self)
        self.tb.addAction(self.op_procedure)
        self.tb.addSeparator()  

        self.wiki1 = QAction(QIcon('icons/null.png'),'Torque Pattern File Requirements',self) # 
        self.tb.addAction(self.wiki1)
        self.tb.addSeparator()

        self.wiki2 = QAction(QIcon('icons/null.png'),'GRBL Settings',self)
        self.tb.addAction(self.wiki2)
        self.tb.addSeparator()

    def headTabWidgets(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        
        self.tabs.addTab(self.tab1, 'Administrator Mode')
        self.tabs.addTab(self.tab2, 'Operator Mode')

    def adminTabWidgets(self):
        self.mod_view_tabs = QTabWidget()
        self.mod_tab = QWidget()
        self.op_tab = QWidget()
        self.create_tab = QWidget()
        self.mod_view_tabs.addTab(self.op_tab, 'View')
        self.mod_view_tabs.addTab(self.mod_tab, 'Edit')
        self.mod_view_tabs.addTab(self.create_tab, 'Add New')

    def PreRunTabWidgets(self):
        self.op_tabs = QTabWidget()
        self.term_tab = QWidget()
        self.vis_tab = QWidget()
        self.cam_view_tab = QWidget()
        self.gcode_tab = QWidget()
        self.op_tabs.addTab(self.term_tab, 'Terminal')
        self.op_tabs.addTab(self.vis_tab, 'Pattern Visual')
        self.op_tabs.addTab(self.cam_view_tab, 'Camera View')
        self.op_tabs.addTab(self.gcode_tab, 'Nominal GCODE')
        

    def uploadFileWidgets(self):
        self.file_entry_title = QLabel('File:')
        # self.font = QFont('Arial',12)
        # self.file_entry_title.setFont(self.font)
        self.browes_btn = QPushButton('Browse Files')
        self.browes_btn.clicked.connect(self.browesFilesFunc)
        self.add_pat_file_header = QLabel('Add New Torque Pattern')
        self.up_pat_name = QLabel('Enter a Unique Name for the Torque Pattern:')
        self.file_pat_name = QLineEdit()
        self.file_pat_name.setPlaceholderText('Name of Torqe Pattern')
        self.add_file_btn = QPushButton('Add')
        self.add_file_btn.clicked.connect(self.addFilePatternFunc)
        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText('Torque Pattern File Path (*.csv)')

    def patternListWidgets(self):
        self.select_btn = QPushButton('Select')
        self.select_btn.clicked.connect(self.selectPatternFunc)
        self.mod_btn = QPushButton('Modify')
        #self.mod_btn.clicked.connect(self.modPatternFunc)
        self.delete_pat_btn = QPushButton('Delete')
        self.delete_pat_btn.clicked.connect(self.deletePatternFunc)
        self.pattern_list = QListWidget(self)
        self.pattern_list.clicked.connect(self.listClickFunc)

        self.selected_pat_title = QLabel('Pattern Name:')
        self.selected_pat_disp = QLineEdit()
        #self.selected_pat_disp.setReadOnly(True)

    def modPatternWidgets(self):
        self.pat_table1 = QTableWidget()
        self.add_row_btn = QPushButton('Add Row')
        self.add_col_btn = QPushButton('Add Column')
        self.update_pat_rad = QRadioButton('Update Existing Pattern')
        self.save_copy_rad = QRadioButton('Save a Copy')
        self.save_copy_rad.setChecked(True)
        self.new_name_title = QLabel('Name of Modified Torque Pattern:')
        self.update_btn = QPushButton('Update Pattern')
        self.new_name_entry = QLineEdit()
        self.new_name_entry.setPlaceholderText('Name of New Pattern')
        self.save_pattern = QPushButton('Save Copy')
        #self.save_pattern.clicked.connect(self.savePatternFunc)
        self.update_pattern = QPushButton('Update Pattern')
        #self.update_pattern.clicked.connect(self.updatePatternFunc)
        self.update_pat_disp = QLineEdit()
        self.update_pat_disp.setReadOnly(True)
        self.refresh = QPushButton('Refresh')
        self.refresh.clicked.connect(self.refreshFunc)
        self.simulate_btn = QPushButton('Simulate Pattern')
        #self.simulate_btn.clicked.connect(self.simFunc)
        self.visualize_btn = QPushButton('Pattern Visual')
        self.visualize_btn.clicked.connect(self.visualFunc)

    def refreshFunc(self):##################################################################################################################################
        exec(open("fu.py").read())
        
    def opPatternViewWidgets(self):
        self.pat_table2 = QTableWidget()
        self.pat_name_disp_title1 = QLabel('Selected Pattern:')
        self.pat_name_disp1 = QLineEdit()
        self.pat_name_disp1.setReadOnly(True)
        #self.calibrate = QPushButton('Begin Calibration')
        #self.calibrate.clicked.connect(self.plateCalibrateFunc)
        
        #self.simulate_btn2 = QPushButton('Simulate Pattern')
        #self.simulate_btn2.clicked.connect(self.simFunc2)
        #self.visualize_btn2 = QPushButton('Pattern Visual')
        #self.visualize_btn2.clicked.connect(self.visualFunc)

    def PreRunDocWidgets(self):
        self.part_num_title = QLabel('Assembly Part Number:\t')
        self.part_num_entry = QLineEdit()
        self.part_num_entry.setPlaceholderText('(64 charictor maximum)')

        self.serial_num_title = QLabel('Serial Number:\t\t')
        self.serial_num_entry = QLineEdit()
        self.serial_num_entry.setPlaceholderText('(32 charictor maximum)')

        self.out_file_title = QLabel('Output File Name:\t\t')
        self.out_file_entry = QLineEdit()

        self.plate_calibate_btn = QPushButton('Calibrate Plate')
        self.plate_calibate_btn.clicked.connect(self.calibratePlateFunc)
        self.dry_run_btn = QPushButton('Dry Run')
        self.dry_run_btn.clicked.connect(self.dryRunFunc)
        self.run_btn = QPushButton('Run')
        self.run_btn.clicked.connect(self.runFunc)

    #def calBtn(self):
    #self.calibrate = plart_cal_window01.CalibratePlate()
    
    
    def grblMainWidgets(self):
        # VISUALIZE PATTERN - WIDGETS
        self.vis_img = QLabel(self)

        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.connectSerFunc)
        self.disconnect_btn = QPushButton('Disconnect')
        self.disconnect_btn.clicked.connect(self.disconnectSerFunc)

        self.term_pat_title = QLabel('Selected Pattern')
        self.term_pat_disp = QLineEdit()
        self.term_pat_disp.setPlaceholderText('Pattern Not Yet Selected')
        self.term_pat_disp.setReadOnly(True)

        self.terminal_txt = QTextEdit()
        self.terminal_txt.setReadOnly(True)
        
        self.send_cmd_btn = QPushButton('Send')
        self.send_cmd_btn.clicked.connect(self.sendCmdFunc)

        self.cmd_line = QLineEdit()
        self.cmd_line.returnPressed.connect(self.send_cmd_btn.click)
        

        self.alarm_off_btn = QPushButton('Disable Alarm')
        self.alarm_off_btn.clicked.connect(self.alarmOffFunc)

        self.home_btn = QPushButton('Execute Homing')
        self.home_btn.clicked.connect(self.homingFunc)

        ###################### GRBL JOG ###############################
        self.jog_font = QFont('Arial',16)

        self.cont_jog = QRadioButton('Continous Jog')
        self.step_jog = QRadioButton('Step Jog')
        self.step_jog.setChecked(True)

        self.arrow_key_check = QCheckBox('Use Arrow Keys to Jog')

        self.px_btn = QPushButton('+X')
        self.px_btn.clicked.connect(self.pxFunc)
        self.px_btn.pressed.connect(self.pxPressedFunc)
        self.px_btn.released.connect(self.pxReleasedFunc)
        self.px_btn.setFont(self.jog_font)

        self.mx_btn = QPushButton('-X')
        self.mx_btn.pressed.connect(self.mxPressedFunc)
        self.mx_btn.released.connect(self.mxReleasedFunc)
        self.mx_btn.clicked.connect(self.mxFunc)
        self.mx_btn.setFont(self.jog_font)

        self.py_btn = QPushButton('+Y')
        self.py_btn.pressed.connect(self.pyPressedFunc)
        self.py_btn.released.connect(self.pyReleasedFunc)
        self.py_btn.clicked.connect(self.pyFunc)
        self.py_btn.setFont(self.jog_font)

        self.my_btn = QPushButton('-Y')
        self.my_btn.pressed.connect(self.myPressedFunc)
        self.my_btn.released.connect(self.myReleasedFunc)
        self.my_btn.clicked.connect(self.myFunc)
        self.my_btn.setFont(self.jog_font)

        self.pz_btn = QPushButton('+Z')
        self.pz_btn.pressed.connect(self.pzPressedFunc)
        self.pz_btn.released.connect(self.pzReleasedFunc)
        self.pz_btn.clicked.connect(self.pzFunc)
        self.pz_btn.setFont(self.jog_font)

        self.mz_btn = QPushButton('-Z')
        self.mz_btn.pressed.connect(self.mzPressedFunc)
        self.mz_btn.released.connect(self.mzReleasedFunc)
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

    def ptEntryWidgets(self):
        ####################################################################################### CAMERA WIDGETS
        self.open_cam_btn = QPushButton('Open Camera Display')
        self.open_cam_btn.clicked.connect(self.openCamDispFunc)
        self.close_cam_btn = QPushButton('Close Camera Display')
        self.close_cam_btn.clicked.connect(self.closeCamDispFunc)

        self.cam_view1 = QLabel()
        

        self.x1_lb = QLabel('X1')
        self.y1_lb = QLabel('Y1')
        self.x1_entry = QLineEdit()
        self.y1_entry = QLineEdit()
        self.record_pt1_btn = QPushButton('Record Position')
        self.record_pt1_btn.clicked.connect(self.recordPt1)

        self.x2_lb = QLabel('X2')
        self.y2_lb = QLabel('Y2')
        self.x2_entry = QLineEdit()
        self.y2_entry = QLineEdit()
        self.record_pt2_btn = QPushButton('Record Position')
        self.record_pt2_btn.clicked.connect(self.recordPt2)

    def gcodeTabWidgets(self):
        self.gcode_txt = QTextEdit()
        self.gcode_txt.setReadOnly(True)
        


    """ def keyPressEvent(self, e):
        

        key = e.key()


        fr = self.jog_feed_entry.text().strip()
        dist = self.jog_dist_entry.text().strip()

        if e.matches(Qt.Key_Right):
            print('fuck')

        if self.check_connect == 1 and len(fr) > 0 and len(dist) > 0:

            if key == Qt.Key_Left:
                #self.mxFunc()
                pass
            elif key == Qt.Key_Right:
                #self.pxFunc()
                pass
            elif key == Qt.Key_Up:
                self.pyFunc()
            elif key == Qt.Key_Down:
                self.myFunc() """
        
    """ def keyReleaseEvent(self, e):
        key_cmd = e.key()

        if not e.isAutoRepeat():
            print('release AUTO REPEAT')

            if key_cmd == Qt.Key_Up:
                print('POOPup released') """


    def openCamDispFunc(self):
        print('ininini')
        self.cam_off = False
        self.cam_on = True
        self.cap = cv2.VideoCapture(1)
        while(self.cam_on):
            

            on_off = self.turnOff()
            if on_off:
                break

            # Capture frame-by-frame
            ret, frame = self.cap.read()
            height, width, channel = frame.shape
            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            #x = cv2.imshow('frame',frame)
            #frame = gray
            #x = cv2.imshow('frame',frame)
            

            
            bytesPerLine = 3 * width
            #height = height*0.9
            #width = width*0.9
            
            #qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            
            #data = im.fromarray(frame) 
            #img = QImage(frame)
            self.cam_view1.setPixmap(QPixmap(qImg))
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
        
        #camera_disp01.camera_on(self)

    def turnOff(self):
        return self.cam_off
    
    def closeCamDispFunc(self):
        self.cam_off = True
        self.cam_on = False


    def calibratePlateFunc(self):
        #self.calibration_window = plate_cal_window01.CalibratePlate()
        #print(self.calibration_window.phi)

        #try:
        print(self.mpos_x1)
        print(self.xp1)
        in2mm = 25.4
        self.xw1 = (self.mpos_x1 - self.wcx_off)/in2mm
        self.yw1 = (self.mpos_y1 - self.wcy_off)/in2mm
        self.xw2 = (self.mpos_x2 - self.wcx_off)/in2mm
        self.yw2 = (self.mpos_y2 - self.wcy_off)/in2mm
        dxw = self.xw2 - self.xw1
        dyw = self.yw2 - self.yw1
        dxp = self.xp2 - self.xp1
        dyp = self.yp2 - self.yp1

        # plate coord vector to point 1 & 2
        self.rp1 = np.array([[self.xp1, self.yp1]]).T
        self.rp2 = np.array([[self.xp2, self.yp2]]).T

        self.rw1 = np.array([[self.xw1, self.yw1]]).T
        self.rw2 = np.array([[self.xw2, self.yw2]]).T

        gamma = math.atan2(dyw,dxw)
        phi = math.atan2(dyp,dxp)
        self.theta = gamma - phi

        self.A_matrix = np.array([[math.cos(self.theta), -math.sin(self.theta)],
                            [math.sin(self.theta), math.cos(self.theta)]])
        
        self.rQ = self.rw1 - np.matmul(self.A_matrix, self.rp1)
        rQQ = self.rw2 - np.matmul(self.A_matrix, self.rp2)

        print(self.rQ)
        print(self.theta*180/math.pi)
        print(rQQ)

        # defineing the work coordinates
        self.pat_linked_list.set_work_coords(self.A_matrix, self.rQ)
        self.pat_linked_list.disp()
        #self.pat_linked_list.write_gcode()

        #except AttributeError:
            #self.terminal_txt.append('\nThe Necessary Fields Have Not Been Recorded')


    def alarmOffFunc(self):
        cmd = '$X\n'
        try:
            self.terminal_txt.append(cmd)
            #print(self.ser)
            self.ser.write(cmd.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass
    
    def homingFunc(self):
        cmd = '$H\n'
        try:
            self.terminal_txt.append(cmd)
            #print(self.ser)
            self.ser.write(cmd.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass

        
        cmd = 'G0Z60\n'
        try:
            self.terminal_txt.append(cmd)
            #print(self.ser)
            self.ser.write(cmd.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass

    def pxPressedFunc(self):
        if self.step_jog.isChecked():
            return

        fr = self.jog_feed_entry.text().strip()
        dist = '600'
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

    def pxReleasedFunc(self):

        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.ser.write(Gcode_str.encode())
            self.terminal_txt.append(Gcode_str)
            print(self.ser)
            
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_byte = b'0x18'
        Gcode_byte = b'0x85' + '\n'.encode()
        Gcode_str = '(can)\r\n' # suppose to be ctrl-X but idk if it works
        Gcode_str = '~\n'

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


    def pxFunc(self):
        if self.cont_jog.isChecked():
            return

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

    

    def mxPressedFunc(self):
        if self.step_jog.isChecked():
            return

        fr = self.jog_feed_entry.text().strip()
        dist = '-600'
        if len(fr) > 0 and fr.isnumeric():
            Gcode_str = '$J=G91G21X' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def mxReleasedFunc(self):
        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.terminal_txt.append(Gcode_str)
            self.ser.write(Gcode_str.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_str = '~\n'
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

    def mxFunc(self):
        if self.cont_jog.isChecked():
            return

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

    

    def pyPressedFunc(self):
        if self.step_jog.isChecked():
            return

        fr = self.jog_feed_entry.text().strip()
        dist = '600'
        if len(fr) > 0 and fr.isnumeric():
            Gcode_str = '$J=G91G21Y' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def pyReleasedFunc(self):
        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.terminal_txt.append(Gcode_str)
            self.ser.write(Gcode_str.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_str = '~\n'
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

    def pyFunc(self):
        if self.cont_jog.isChecked():
            return

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

    

    def myPressedFunc(self):
        if self.step_jog.isChecked():
            return
        print('major fuch you')
        fr = self.jog_feed_entry.text().strip()
        dist = '-600'
        
        if len(fr) > 0 and fr.isnumeric():
            Gcode_str = '$J=G91G21Y' +  dist + 'F' + fr + '\n'
            print('fuch you')
            try:
                print('sdfaksjdhfkjsdlhafkjhs')
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def myReleasedFunc(self):
        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.terminal_txt.append(Gcode_str)
            self.ser.write(Gcode_str.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_str = '~\n'
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

    def myFunc(self):
        if self.cont_jog.isChecked():
            return

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

    

    def pzPressedFunc(self):
        if self.step_jog.isChecked():
            return

        fr = self.jog_feed_entry.text().strip()
        dist = '80'
        if len(fr) > 0 and fr.isnumeric():
            Gcode_str = '$J=G91G21Z' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def pzReleasedFunc(self):
        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.terminal_txt.append(Gcode_str)
            self.ser.write(Gcode_str.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_str = '~\n'
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

    def pzFunc(self):
        if self.cont_jog.isChecked():
            return

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

    

    def mzPressedFunc(self):
        if self.step_jog.isChecked():
            return

        fr = self.jog_feed_entry.text().strip()
        dist = '-80'
        if len(fr) > 0 and fr.isnumeric():
            Gcode_str = '$J=G91G21Z' +  dist + 'F' + fr + '\n'
            
            try:
                self.terminal_txt.append(Gcode_str)
                self.ser.write(Gcode_str.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

        else:
            pass

    def mzReleasedFunc(self):
        if self.step_jog.isChecked():
            return
        
        Gcode_str = '!\n'

        try:
            self.terminal_txt.append(Gcode_str)
            self.ser.write(Gcode_str.encode())
            msg = self.ser.readlines()
    
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                print(line.decode('ascii'))
        except:
            pass 

        Gcode_str = '~\n'
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

    def mzFunc(self):
        if self.cont_jog.isChecked():
            return

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

    def connectSerFunc(self):
        self.check_connect = 1
        #baudrate = 115200
        #baudrate = 96200
        try:
            self.ser = serial.Serial('COM5', baudrate = 115200, timeout=1)
            self.terminal_txt.append('\nConnected from Serial Port COM5\n')
        except:
            self.terminal_txt.append('\nConnect Exception\n')
    
    def sendCmdFunc(self):
        cmd = self.cmd_line.text().strip()
        self.terminal_txt.append(cmd)
        self.cmd_line.clear()
        if self.check_connect == 1:
            

            cmd = cmd + "\n"
        
            self.ser.write(cmd.encode())
            
            #time.sleep(0.5)
            
            msg = self.ser.readlines()
            
            for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii'))
        else:
            self.cmd_line.clear()
            self.terminal_txt.append(cmd)
            self.terminal_txt.append('\nMust connect to serial port prior to sending commands\n')
    
    def disconnectSerFunc(self):
        try:
            self.ser.close()
            self.terminal_txt.append('\nDisconnected from Serial Port COM5\n')
            self.check_connect = 0

        except AttributeError:
            self.terminal_txt.append('\nNot Connected to Serial Port\n')
            
        
    def visualFunc(self):
        #name_id = 'plate_coords_test01.csv'
        self.temp_img_path = self.master_path + '/temp_visual.png'
        self.temp_gcode_path = self.master_path + '/temp_gcode.txt'
        pat_name = self.pat_name_disp1.text()
        path = self.pattern_path + '/' + pat_name + '/Torque_Pattern.csv'
        MakeVisualMain(path, self.temp_img_path, self.temp_gcode_path)
        self.vis_img.setPixmap(QPixmap(self.temp_img_path))
        gcode_file = open(self.temp_gcode_path)
        gcode = gcode_file.read()
        self.gcode_txt.setText(gcode)
        gcode_file.close()

    def setNullPlot(self):
        self.null_path = self.master_path + '/null.png'
        self.vis_img.setPixmap(QPixmap(self.null_path))

    def dryRunFunc(self):
        fast_node = self.pat_linked_list.head()

        while fast_node != None:
            gcode = fast_node._gcode_w
            try:
                
                self.ser.write(gcode.encode())
                self.terminal_txt.append(gcode)
                msg = self.ser.readline().decode('ascii')
                
                if msg.strip() == 'ok':
                    #time.sleep(1)
                    print('we good')
                elif msg.strip() == 'error':
                    print('NOT good')
                else:
                    print('WTF')
                
                    
                self.terminal_txt.append(msg)
            except:
                self.terminal_txt.append('except:\t'+'self.terminal_txt.append(cmd)')

            fast_node = fast_node._next

    def dryRunFunc_old(self):
        gcode_file = open(self.temp_gcode_path)
        for gline in gcode_file:
            #time.sleep(10)
            self.terminal_txt.append(gline)
            try:
                #self.terminal_txt.append(gline)
                #print(self.ser)
                gline = gline.strip() + '\n'
                self.ser.write(gline.encode())
                msg = self.ser.readline().decode('ascii')
                if msg.strip() == 'ok':
                    #time.sleep(1)
                    print('we good')
                elif msg.strip() == 'error':
                    print('NOT good')
                else:
                    print('WTF')
                
                """ for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line .decode('ascii')) """
                    
                self.terminal_txt.append(msg)
            except:
                self.terminal_txt.append('except:\t'+'self.terminal_txt.append(cmd)')

            """ time.sleep(3)
            cmd = '$J=G91G21Z10F300\n'

            try:
                self.terminal_txt.append(cmd)
                #print(self.ser)
                self.ser.write(cmd.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass

            #time.sleep(3)
            cmd = '$J=G91G21Z-10F300\n'

            try:
                self.terminal_txt.append(cmd)
                #print(self.ser)
                self.ser.write(cmd.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                pass """


    def runFunc(self):
        # NEED TO ADD SOME ERROR PREVENTIONS STATEMENT/CONDITIONS
        out_file_name = self.out_file_entry.text()
        serial_num = self.serial_num_entry.text()
        part_num = self.part_num_entry.text()
        pat_name = self.term_pat_disp.text()
        dnt = datetime.now() # dd/mm/YY H:M:S
        dnt_str = str(dnt) # (yyyy-mm-dd H:M:S)
        dnt_list = dnt_str.split()
        date = dnt_list[0]
        time_list = dnt_list[1].split('.')
        time = time_list[0]
        ms = time_list[1]
        
        #patdir_path = self.pattern_path + '/' + pattern_name_txt + '/Torque_Pattern.csv'

        if len(serial_num) > 32:
            mbox = QMessageBox.information(self,'Error','The serial number cannot exceed 32 characters')
        elif len(part_num) > 64:
            mbox = QMessageBox.information(self,'Error','The assembly part number cannot exceed 32 characters')
        else:
            self.doc_headers = ['Pattern Name', 'Assembly Part Number', 'Serial Number', 'Date', 'Time']
            doc_entries = [pat_name, part_num, serial_num, date, time]

            new_doc_path = self.doc_path + '/' + out_file_name + '.csv'
            with open(new_doc_path, 'w',newline='') as write_csvfile:
                doc_file = csv.writer(write_csvfile)

                for i in range(len(self.doc_headers)):
                    row = [self.doc_headers[i]] +  [doc_entries[i]]
                    print(row)
                    doc_file.writerow(row)
                print('RUN!')

    def listClickFunc(self):
        self.selected_pat_disp.setText(self.pattern_list.currentItem().text())

    def deletePatternFunc(self):

        if self.pattern_list.currentItem() != None:
            pattern_name_txt = self.pattern_list.currentItem().text()
            mess = 'Are you sure you want to delete Torque Pattern: ' + pattern_name_txt
            mbox = QMessageBox.information(self,'Warning',mess,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:
                dir_path = self.pattern_path + '/' + pattern_name_txt
                try:
                    shutil.rmtree(dir_path)
                except OSError as e:
                    print("\n\nError: %s : %s" % (dir_path, e.strerror))
                     
                id = self.pattern_list.currentRow()
                self.pattern_list.takeItem(id) 
                self.selected_pat_disp.setText('')

    def selectPatternFunc(self):
        if self.pattern_list.currentItem() != None:
            pattern_name_txt = self.pattern_list.currentItem().text()

            self.pat_name_disp1.setText(pattern_name_txt)
            self.update_pat_disp.setText(pattern_name_txt)
            self.term_pat_disp.setText(pattern_name_txt)

            patdir_path = self.pattern_path + '/' + pattern_name_txt + '/Torque_Pattern.csv'


            
            # making a plate pattern object
            self.plate_pat_select = PlatePattern(pattern_name_txt, self.master_path)
            self.pat_linked_list = PatternLinkedList()
            self.pat_linked_list.create_plate_pattern_list(self.plate_pat_select)
            self.pat_linked_list.disp()

            with open(patdir_path, 'r') as csvfile:
                csv_content = csv.reader(csvfile, delimiter = ',')
                ni = 0
                nj = 0

                for row in csv_content:
                    nj = len(row)
                    ni = ni + 1  

            self.pat_table1.setRowCount(ni)
            self.pat_table1.setColumnCount(nj)

            self.pat_table1.setHorizontalHeaderItem(0,QTableWidgetItem('Queue'))
            self.pat_table1.setHorizontalHeaderItem(1,QTableWidgetItem('Xn [IN]'))
            self.pat_table1.setHorizontalHeaderItem(2,QTableWidgetItem('Yn [IN]'))
            self.pat_table1.setHorizontalHeaderItem(3,QTableWidgetItem('Torque [IN.LBS]'))

            self.pat_table2.setRowCount(ni)
            self.pat_table2.setColumnCount(nj)  

            self.pat_table2.setHorizontalHeaderItem(0,QTableWidgetItem('Queue'))
            self.pat_table2.setHorizontalHeaderItem(1,QTableWidgetItem('Xn [IN]'))
            self.pat_table2.setHorizontalHeaderItem(2,QTableWidgetItem('Yn [IN]'))
            self.pat_table2.setHorizontalHeaderItem(3,QTableWidgetItem('Torque [IN.LBS]'))

            csvfile.close()

            self.pat_table2.setEditTriggers(QAbstractItemView.NoEditTriggers) # disables table editing

            with open(patdir_path, 'r') as csvfile:
                csv_content = csv.reader(csvfile, delimiter = ',')
                ni = 0

                i = 0
                for row in csv_content:
                    for j in range(len(row)):

                        nj = len(row)

                        self.pat_table1.setItem(i, j, QTableWidgetItem(row[j]))

                        self.pat_table2.setItem(i, j, QTableWidgetItem(row[j]))

                        if (j+1) > 3 and i == 0:
                            col_title_str = 'Iteration ' + str(j+1-3) + ' [%]'
                            self.pat_table1.setHorizontalHeaderItem(j+1,QTableWidgetItem(col_title_str))
                            self.pat_table2.setHorizontalHeaderItem(j+1,QTableWidgetItem(col_title_str))
                    i = i + 1  
            csvfile.close()
            self.visualFunc()

    def popPatternList(self):
        #self.master_path = 'C:/Users/markp/Documents/Alpha.IRUS/Alpha.IRUS - Operations'
        self.pattern_path = self.master_path + '/Torque Patterns'
        self.doc_path = self.master_path + '/Operation Documentation'
        try:
            Path(self.pattern_path).mkdir()
        except FileExistsError:
            for filename in os.listdir(Path(self.pattern_path)):
                self.pattern_list.addItem(filename)
                print(filename) 
        
        try:
            Path(self.doc_path).mkdir()
        except FileExistsError:
            print('The Patter Already Exists 2') 
        
    def browesFilesFunc(self):
        selected_url = QFileDialog.getOpenFileName(self, "alpha.IRUS",'','All Files(*);;*csv')
        print(selected_url)
        self.url = selected_url[0]
        self.file_entry.setText(self.url)    
        
    def addFilePatternFunc(self):

        self.pat_name = self.file_pat_name.text()

        if len(self.pat_name) >= 1 and len(self.url) > 1:
            self.pat_folder = self.pattern_path + '/' + self.pat_name
        
            #Path(pat_folder).mkdir()

            #os.mkdir(Path(pat_folder))

            try:
                Path(self.pat_folder).mkdir()
            except FileExistsError:
                print('The Patter: ' + self.pat_name + ' Already Exists')  
        
            #with open(self.url, 'r') as csvfile:
                #pat_csvr = csv.reader(csvfile, delimiter, ',')
            csvfile = open(self.url, 'r')
            for row in csvfile.readlines():
                row = row.strip()
                row = row.split(',')
                
                if row[1].isdigit():
                    self.pattern_dict[int(row[0])] = row

            new_csv_file = self.pat_folder + '/Torque_Pattern.csv'
            
            with open(new_csv_file, 'w',newline='') as write_csvfile:
                pat_csvw = csv.writer(write_csvfile)

                for i in range(len(self.pattern_dict)):
                    if i+1 in self.pattern_dict:
                        pat_csvw.writerow(self.pattern_dict[i+1])
                    else:
                        print('error with the queue input column')

            pat_log_path = self.pat_folder + '/Pattern_Log.txt'
            pat_log = open(pat_log_path, 'w')
            
            # datetime object containing current date and time
            dnt = datetime.now() # dd/mm/YY H:M:S
            dnt_str = str(dnt) # (yyyy-mm-dd H:M:S)
            dnt_list = dnt_str.split()
            up_date = dnt_list[0]
            time_list = dnt_list[1].split('.')
            up_time = time_list[0]
            #ss = time_list[1]
            #up_time = hhmm + '.' + ss[0:1]
            
            char_addN = 128 - len(self.pat_name)
            if char_addN > 0:
                pat_name_txt = self.pat_name + '_'*char_addN
            else:
                pat_name_txt = self.pat_name
            pat_log.write('---------------------------- PATTERN CREATED ----------------------------\n\n')
            pat_log.write('Pattern Name:\t\t\t' + pat_name_txt + '\n')
            pat_log.write('Date (yyyy-mm-dd H:M:S):\t' + up_date + '\n')
            pat_log.write('Time (hh:mm:ss):\t\t' + up_time + '\n')
            pat_log.write('Input Method:\t\t\tFile Upload\n\n')
            #pat_log.write('Pattern was submitted via file upload.\n\n')
            #pat_log.write('Original File Path:\n' + self.url + '\n\n')


            pat_log.close()
            csvfile.close()
            write_csvfile.close()

            self.pattern_list.addItem(self.pat_name)
            self.file_pat_name.clear()
            self.file_entry.clear()
            self.url = ''


    def recordPt1(self):
        
        if self.check_connect == 1:
            
            xp = self.x1_entry.text().strip()
            yp = self.y1_entry.text().strip()
            self.xp1 = float(xp)
            self.yp1 = float(yp)
            """ if xp.isnumeric() and yp.isnumeric():
                self.xp1 = float(xp)
                self.yp1 = float(yp)
            else:
                self.terminal_txt.append('\nINVALID (X1, Y1) ENTRY\n') """

            
            cmd = '$#'
            cmd = cmd + "\n"
        
            self.ser.write(cmd.encode())
            
            #time.sleep(0.5)
            
            msg = self.ser.readlines()

            for line in msg:
                m = line.decode('ascii')
                
                wc = m.split(':')
                if len(wc) >= 1:
                    if wc[0] == '[G54':
                        wc = m.split(':')
                        wc = wc[1].strip('[\r\n]')
                        wc = wc.split(',')
                        print(wc)
                        self.wcx_off = float(wc[0])
                        self.wcy_off = float(wc[1])
                        self.wcz_off = float(wc[2]) 
                #self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))

            #################################################################   
            cmd = '?'
            cmd = cmd + "\n"
        
            self.ser.write(cmd.encode())
            
            #time.sleep(0.5)
            
            msg = self.ser.readlines()

            for line in msg:
                m = line.decode('ascii')
                check = m.split(':')
                #print(check)
                wc = m.split(':')
                if len(check) >= 1:
                    #print(check[0])
                    if check[0] == '<Idle|MPos':
                        mpos = m.strip('[\r\n]').split('MPos:')[1].split('|')[0].split(',')
                        
                        print(mpos)
                        self.mpos_x1 = float(mpos[0])
                        self.mpos_y1 = float(mpos[1])
                        self.mpos_z1 = float(mpos[2])
                  

                    """ elif check[0] == 'WCO':
                        print('INNNN')
                        self.wco = m.strip('[\r\n]').split(':')[1].strip('<>\r\n[]').split(',')
                        
                        print(wco)
                        self.wco_x = int(float(wco[0]))
                        self.wco_y = int(float(wco[1]))
                        self.wco_z = int(float(wco[2]))
                        print(wco_y) """
            
            
            """ for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii')) """
            self.terminal_txt.append('\n(X1, Y1) have been recorded\n')
        else:
            #self.cmd_line.clear()
            #self.terminal_txt.append(cmd)
            self.terminal_txt.append('\nMust connect to serial port prior to sending commands\n')

    def recordPt2(self):
        
        if self.check_connect == 1:

            xp = self.x2_entry.text().strip()
            yp = self.y2_entry.text().strip()
            self.xp2 = float(xp)
            self.yp2 = float(yp)
            """ if xp.isnumeric() and yp.isnumeric():
                self.xp2 = float(xp)
                self.yp2 = float(yp)
            else:
                self.terminal_txt.append('\nINVALID (X2, Y2) ENTRY\n') """
            
            cmd = '$#'
            cmd = cmd + "\n"
        
            self.ser.write(cmd.encode())
            
            #time.sleep(0.5)
            
            msg = self.ser.readlines()

            for line in msg:
                m = line.decode('ascii')
                
                wc = m.split(':')
                if len(wc) >= 1:
                    if wc[0] == '[G54':
                        wc = m.split(':')
                        wc = wc[1].strip('[\r\n]')
                        wc = wc.split(',')
                        print(wc)
                        self.wcx_off = float(wc[0])
                        self.wcy_off = float(wc[1])
                        self.wcz_off = float(wc[2]) 
                #self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))

            #################################################################   
            cmd = '?'
            cmd = cmd + "\n"
        
            self.ser.write(cmd.encode())
            
            #time.sleep(0.5)
            
            msg = self.ser.readlines()

            for line in msg:
                m = line.decode('ascii')
                check = m.split(':')
                #print(check)
                wc = m.split(':')
                if len(check) >= 1:
                    #print(check[0])
                    if check[0] == '<Idle|MPos':
                        mpos = m.strip('[\r\n]').split('MPos:')[1].split('|')[0].split(',')
                        
                        print(mpos)
                        self.mpos_x2 = float(mpos[0])
                        self.mpos_y2 = float(mpos[1])
                        self.mpos_z2 = float(mpos[2])
                      
                    """ elif check[0] == 'WCO':
                        print('INNNN')
                        self.wco = m.strip('[\r\n]').split(':')[1].strip('<>\r\n[]').split(',')
                        
                        print(wco)
                        self.wco_x = int(float(wco[0]))
                        self.wco_y = int(float(wco[1]))
                        self.wco_z = int(float(wco[2]))
                        print(wco_y) """
            
            
            """ for line in msg:
                self.terminal_txt.append(line.decode('ascii'))
                #self.terminal_txt.insertPlainText(line.decode('ascii'))
                print(line.decode('ascii')) """
            self.terminal_txt.append('\n(X2, Y2) have been recorded\n')
        else:
            #self.cmd_line.clear()
            #self.terminal_txt.append(cmd)
            self.terminal_txt.append('\nMust connect to serial port prior to sending commands\n')

    def ptEntyLayouts(self):
        self.pt_group1 = QGroupBox('Point 1 Plate Coordinates')
        self.pt_group2 = QGroupBox('Point 2 Plate Coordinates')

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
        self.pt_hbox1.addWidget(self.y1_lb)
        self.pt_hbox1.addWidget(self.y1_entry)
        self.pt_hbox1.addWidget(self.record_pt1_btn)
        
        self.pt_hbox3.addWidget(self.x2_lb)
        self.pt_hbox3.addWidget(self.x2_entry)
        self.pt_hbox3.addWidget(self.y2_lb)
        self.pt_hbox3.addWidget(self.y2_entry)
        self.pt_hbox3.addWidget(self.record_pt2_btn)

        self.pt_vbox1.addLayout(self.pt_hbox1)
        #self.pt_vbox1.addLayout(self.pt_hbox2)
        #self.pt_vbox1.addWidget(self.record_pt1_btn)
        self.pt_group1.setLayout(self.pt_vbox1)

        self.pt_vbox2.addLayout(self.pt_hbox3)
        #self.pt_vbox2.addLayout(self.pt_hbox4)
        
        self.pt_group2.setLayout(self.pt_vbox2)

        self.cam_hbox1 = QHBoxLayout()
        self.cam_hbox1.addWidget(self.open_cam_btn)
        self.cam_hbox1.addWidget(self.close_cam_btn)

        self.pt_vbox3.addLayout(self.cam_hbox1)
        self.pt_vbox3.addWidget(self.pt_group1)
        self.pt_vbox3.addWidget(self.pt_group2)

    def layoutsMain(self):
        self.admin_mainH = QHBoxLayout()
        self.admin_col1V = QVBoxLayout()
        self.admin_col2V = QVBoxLayout()
    
    def uploadFileLayout(self):
        self.up_mainV = QVBoxLayout()
        self.up_hbox1 = QHBoxLayout()
        self.up_hbox2 = QHBoxLayout()
        self.up_group = QGroupBox('Upload Torque Pattern File')

        self.up_hbox1.addWidget(self.file_entry_title)
        self.up_hbox1.addWidget(self.file_entry)
        self.up_hbox1.addWidget(self.browes_btn)
        self.up_mainV.addLayout(self.up_hbox1)
        self.up_mainV.addWidget(self.up_pat_name)
        #self.up_hbox2.addWidget(self.up_pat_name)
        self.up_hbox2.addWidget(self.file_pat_name)
        self.up_hbox2.addWidget(self.add_file_btn)
        self.up_mainV.addLayout(self.up_hbox2)

        self.up_group.setLayout(self.up_mainV)    

    def patternListLayout(self):
        self.plist_hbox1 = QHBoxLayout()
        self.plist_hbox2 = QHBoxLayout()
        self.plist_vbox1 = QVBoxLayout()
        self.plist_group = QGroupBox('List of Torque Patterns')

        self.plist_hbox2.addWidget(self.selected_pat_title)
        self.plist_hbox2.addWidget(self.selected_pat_disp)
        self.plist_hbox2.addWidget(self.select_btn)
        self.plist_hbox2.addWidget(self.delete_pat_btn)
        self.plist_vbox1.addLayout(self.plist_hbox2)
        self.plist_vbox1.addWidget(self.pattern_list)
        self.plist_group.setLayout(self.plist_vbox1)
        #self.plist_vbox1.addWidget(self.select_btn)
        #self.plist_vbox1.addWidget(self.mod_btn)
        #self.plist_vbox1.addWidget(self.delete_pat_btn)
        #self.plist_vbox1.addStretch()
        #self.plist_hbox1.addWidget(self.pattern_list)
        #self.plist_hbox1.addLayout(self.plist_vbox1)
        #self.plist_group.setLayout(self.plist_hbox1)
    
    def OperateTabLayout(self):
        self.op_hbox1 = QHBoxLayout()
        self.op_hbox2 = QHBoxLayout()
        self.op_hbox3 = QHBoxLayout()
        self.op_vbox1 = QVBoxLayout()
        self.op_vbox2 = QVBoxLayout()
        self.op_vbox3 = QVBoxLayout()
        self.op_mainV = QVBoxLayout()

        self.op_hbox3.addWidget(self.pat_name_disp_title1)
        self.op_hbox3.addWidget(self.pat_name_disp1)
        self.op_hbox3.addStretch()

        self.op_mainV.addLayout(self.op_hbox3)
        self.op_mainV.addWidget(self.pat_table2)

        """ self.op_hbox1.addStretch()
        self.op_hbox1.addWidget(self.add_row_btn2)
        self.op_hbox1.addWidget(self.add_col_btn2)
        #self.op_hbox1.addWidget(self.visualize_btn2)
        #self.op_hbox1.addWidget(self.simulate_btn2)
        self.op_mainV.addLayout(self.op_hbox1)
        self.op_hbox2.addWidget(self.calibrate)
        self.op_hbox2.addStretch()
        self.op_mainV.addLayout(self.op_hbox2) """
        self.op_tab.setLayout(self.op_mainV)

    def modifyPatternTabLayout(self):
        self.mod_hbox1 = QHBoxLayout()
        self.mod_hbox2 = QHBoxLayout()
        self.mod_hbox3 = QHBoxLayout()
        self.mod_vbox1 = QVBoxLayout()
        self.mod_vbox2 = QVBoxLayout()
        self.mod_vbox3 = QVBoxLayout()
        self.mod_mainV = QVBoxLayout()

        self.mod_group = QGroupBox()

        #self.mod_mainV.addStretch()
        #self.mod_mainV.addWidget(self.refresh)
        self.mod_mainV.addWidget(self.pat_table1)
        self.mod_hbox1.addStretch()
        self.mod_hbox1.addWidget(self.refresh)
        self.mod_hbox1.addWidget(self.add_row_btn)
        self.mod_hbox1.addWidget(self.add_col_btn)
        #self.mod_hbox1.addWidget(self.visualize_btn)
        #self.mod_hbox1.addWidget(self.simulate_btn)
        self.mod_mainV.addLayout(self.mod_hbox1)

        self.mod_hbox3.addWidget(self.update_pat_rad)

        self.mod_hbox3.addWidget(self.update_pat_disp)
        
        self.mod_hbox3.addWidget(self.update_btn)
        self.mod_hbox3.addStretch()
        self.mod_mainV.addLayout(self.mod_hbox3)
        self.mod_hbox2.addWidget(self.save_copy_rad)
        #self.mod_hbox2.addWidget(self.new_name_title)
        self.mod_hbox2.addWidget(self.new_name_entry)
        self.mod_hbox2.addWidget(self.save_pattern)
        self.mod_vbox2.addLayout(self.mod_hbox2)

        self.mod_mainV.addLayout(self.mod_vbox2)
      
        #self.mod_group.setLayout(self.mod_mainV)
        self.mod_tab.setLayout(self.mod_mainV)

        """ self.admin_col1V.addWidget(self.mod_view_tabs)

        self.admin_mainH.addLayout(self.admin_col1V,50)
        self.admin_mainH.addLayout(self.admin_col2V,50)
        self.tab1.setLayout(self.admin_mainH) """

    def operatorDocLayout(self):
        self.opr_hbox1 = QHBoxLayout()
        self.opr_hbox2 = QHBoxLayout()
        self.opr_hbox3 = QHBoxLayout()
        self.opr_hbox4 = QHBoxLayout()

        self.opr_vbox1 = QVBoxLayout()
        self.opr_vbox2 = QVBoxLayout()
        self.opr_vbox3 = QVBoxLayout()
        self.opr_vbox4 = QVBoxLayout()

        self.opr_hbox1.addWidget(self.part_num_title)
        self.opr_hbox1.addWidget(self.part_num_entry)
        #self.opr_hbox1.addStretch()
        self.opr_hbox2.addWidget(self.serial_num_title)
        #self.opr_hbox2.addStretch()
        self.opr_hbox2.addWidget(self.serial_num_entry)
        #self.opr_hbox2.addStretch()

        self.opr_hbox4.addWidget(self.out_file_title)
        self.opr_hbox4.addWidget(self.out_file_entry)
        #self.opr_hbox4.addStretch() 

        """ self.opr_vbox1.addWidget(self.part_num_title)
        self.opr_vbox1.addWidget(self.part_num_entry)
        self.opr_vbox1.addStretch()
        self.opr_vbox1.addWidget(self.serial_num_title)
        #self.opr_hbox2.addStretch()
        self.opr_vbox1.addWidget(self.serial_num_entry)
        self.opr_vbox1.addStretch()

        self.opr_vbox1.addWidget(self.out_file_title)
        self.opr_vbox1.addWidget(self.out_file_entry)
        self.opr_vbox1.addStretch() """

        #self.opr_hbox3.addWidget(self.plate_calibate_btn)################# PLATE CALIBRATION BTN
        self.opr_hbox3.addWidget(self.dry_run_btn) ####################### DRY RUN BTN
        self.opr_hbox3.addWidget(self.run_btn) ############################# RUN BTN
        #self.opr_hbox3.addStretch()

        
        self.opr_vbox1.addLayout(self.opr_hbox1)
        self.opr_vbox1.addLayout(self.opr_hbox2)
        self.opr_vbox1.addLayout(self.opr_hbox4)
        self.opr_vbox1.addLayout(self.opr_hbox3)

        self.run_doc_group = QGroupBox('Run Documentation')
        self.run_doc_group.setLayout(self.opr_vbox1)
        

    def termTabLayout(self):
        self.term_tab_hbox_main = QHBoxLayout()
        self.ctrl_btn_group = QGroupBox('Machine Controls') ###################

        """ self.term_pat_title = QLabel('Selected Pattern')
        self.term_pat_disp = QLineEdit()
        self.term_pat_disp.setPlaceholderText('Pattern Not Yet Selected')
        self.term_pat_disp.setReadOnly(True) """

        self.term_hbox1 = QHBoxLayout()
        self.term_hbox2 = QHBoxLayout()
        self.term_hbox3 = QHBoxLayout()
        self.term_vbox1 = QVBoxLayout()
        self.term_vbox2 = QVBoxLayout()

        self.term_hbox1.addWidget(self.cmd_line)
        self.term_hbox1.addWidget(self.send_cmd_btn)

        self.term_hbox2.addWidget(self.connect_btn)
        self.term_hbox2.addWidget(self.disconnect_btn)
        self.term_hbox2.addWidget(self.home_btn)
        self.term_hbox2.addWidget(self.alarm_off_btn)

        # term_hbox3 is added to right col in the layoutsEnd section
        """ self.term_hbox3.addStretch()
        self.term_hbox3.addWidget(self.term_pat_title)
        self.term_hbox3.addWidget(self.term_pat_disp)
        self.term_hbox3.addStretch() """

        self.ctrl_btn_group.setLayout(self.term_hbox2) ############################## CRONTROL BTN GROUP


        #self.term_vbox1.addLayout(self.term_hbox2)
        
        self.term_vbox1.addWidget(self.terminal_txt)
        self.term_vbox1.addLayout(self.term_hbox1)
        self.null1 = QLabel('')
        self.term_vbox1.addWidget(self.null1)

        

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

        self.jog_hbox5 = QHBoxLayout()
        self.jog_hbox5.addWidget(self.cont_jog)
        self.jog_hbox5.addWidget(self.step_jog)

        #self.jog_vbox1.addWidget(self.ctrl_btn_group)
        self.jog_vbox1.addLayout(self.jog_grid)
        self.jog_vbox1.addLayout(self.jog_hbox5)
        self.jog_vbox1.addWidget(self.n7)
        self.jog_vbox1.addLayout(self.jog_hbox1)
        self.jog_vbox1.addLayout(self.jog_hbox2)
        self.jog_vbox1.addStretch()

        """ self.jog_hbox4 = QHBoxLayout()
        self.jog_hbox4.addStretch()
        self.jog_hbox4.addWidget(self.arrow_key_check)
        self.jog_vbox1.addLayout(self.jog_hbox4)
        self.jog_vbox1.addStretch() """

        

        self.jog_group.setLayout(self.jog_vbox1)
        #self.jog_vbox2.addWidget(self.cam_view1)
        #self.jog_vbox2.addWidget(self.jog_group)

        self.pt_vbox3.addWidget(self.plate_calibate_btn)
        self.cal_group = QGroupBox('Plate Coordinate Calibration')
        self.cal_group.setLayout(self.pt_vbox3)
        #self.jog_vbox2.addWidget(self.cal_group)

        

        #self.jog_hbox3.addLayout(self.jog_vbox2,50)
        #self.jog_vbox4.addLayout(self.term_vbox1)

        

        self.jog_hbox3.addLayout(self.term_vbox1)

        '''-----------TESTING WIDGETS-----------'''
        self.testing_btn = QPushButton('Run Test')
        self.testing_btn.clicked.connect(self.runTestFunc)
        self.jog_hbox3.addWidget(self.testing_btn)
        '''-----------TESTING WIDGETS-----------'''
        
        #self.jog_hbox3.addLayout(self.jog_vbox2,40)
        
        #self.right_col.addLayout(self.jog_hbox3)

        #self.term_tab_hbox_main.addLayout(self.term_vbox1)
        #self.term_tab_hbox_main.addLayout(self.jog_hbox3)

        #self.term_tab.setLayout(self.term_tab_hbox_main)
        self.term_tab.setLayout(self.jog_hbox3)

        #self.tab3_hbox_main.addLayout(self.right_col,50)
        #self.tab3.setLayout(self.tab3_hbox_main)

    def runTestFunc(self):
        direction = 'X'
        incrament = 0.01 # [mm]
        feedrate = 1.15 # [mm/s]
        pos_start = 10 # [mm]
        
        N = 1000 # number of iterations
        pos_end = pos_start + incrament*N # [mm]
        pos_i = pos_start
        for i in range(N):
            pos_i = pos_i + incrament
            gcode = 'G1' + direction + str(pos_i) + 'F' + str(feedrate) + '\n'

            try:
                self.terminal_txt.append(gcode)
                self.ser.write(gcode.encode())
                msg = self.ser.readlines()
        
                for line in msg:
                    self.terminal_txt.append(line.decode('ascii'))
                    #self.terminal_txt.insertPlainText(line.decode('ascii'))
                    print(line.decode('ascii'))
            except:
                print('EXCEPTION ERROR')


    def gcodeTabLayout(self):
        self.gcode_hbox1 = QHBoxLayout()
        self.gcode_hbox2 = QHBoxLayout()
        self.gcode_vbox1 = QVBoxLayout()
        self.gcode_vbox2 = QVBoxLayout()

        self.gcode_vbox1.addWidget(self.gcode_txt)

        self.gcode_tab.setLayout(self.gcode_vbox1)

    """ def newLayouts(self):
        self.new_hbox1 = QHBoxLayout()
        self.new_hbox2 = QHBoxLayout()
        self.new_hbox3 = QHBoxLayout()

        self.new_vbox1 = QVBoxLayout()
        self.new_vbox2 = QVBoxLayout()
        self.new_vbox3 = QVBoxLayout()

        self.new_vbox1.addWidget(self.ctrl_btn_group)
        self.new_vbox1.addWidget(self.jog_group)

        self.new_hbox1.addLayout(self.new_vbox1)
        self.new_hbox1.addWidget(self.cal_group)
        self.new_hbox1.addWidget(self.run_doc_group) """


    def layoutsEnd(self):
        #self.admin_col1V.addWidget(self.mod_view_tabs)

        self.admin_col1V.addWidget(self.up_group)
        self.admin_col1V.addWidget(self.plist_group)

        self.admin_col1V.addWidget(self.mod_view_tabs)

        self.new_hbox1 = QHBoxLayout()
        self.new_hbox2 = QHBoxLayout()
        self.new_hbox3 = QHBoxLayout()

        self.new_vbox1 = QVBoxLayout()
        self.new_vbox2 = QVBoxLayout()
        self.new_vbox3 = QVBoxLayout()

        self.new_vbox1.addWidget(self.ctrl_btn_group)
        self.new_vbox1.addWidget(self.jog_group)

        self.new_vbox2.addWidget(self.cal_group)
        self.new_vbox2.addWidget(self.run_doc_group)

        self.new_hbox1.addLayout(self.new_vbox1)
        self.new_hbox1.addLayout(self.new_vbox2)
        #self.new_hbox1.addWidget(self.cal_group)
        #self.new_hbox1.addWidget(self.run_doc_group)
        
        self.vis_layout = QHBoxLayout()
        self.vis_layout.addStretch()
        self.vis_layout.addWidget(self.vis_img)
        self.vis_layout.addStretch()
        self.vis_tab.setLayout(self.vis_layout)

        self.cam_vbox1 = QHBoxLayout()
        self.cam_vbox1.addStretch()
        self.cam_vbox1.addWidget(self.cam_view1)
        self.cam_vbox1.addStretch()
        self.cam_view_tab.setLayout(self.cam_vbox1)

        self.section_vbox1 = QVBoxLayout() # layout made to define spacing of right col
        #self.section_vbox1.addWidget(self.ctrl_btn_group) # row of btns
        #self.section_vbox1.addLayout(self.term_hbox3) # selected pattern disp
        
        self.hbox_tabs_jog = QHBoxLayout()
        self.hbox_tabs_jog.addWidget(self.op_tabs)#####################################################################
        
        #self.hbox_tabs_jog.addLayout(self.jog_vbox2)##################################################################### then add hbox to section_vbox1
        #self.section_vbox1.addStretch()
        self.section_vbox1.addLayout(self.new_hbox1, 40)
        self.section_vbox1.addLayout(self.hbox_tabs_jog, 60)
        
        
        #self.section_vbox1.addWidget(self.op_tabs) # tabs for grbl and stuff
        #self.section_vbox1.addStretch()
        
        #self.section_vbox2 = QVBoxLayout()
        #self.section_vbox2.addLayout(self.opr_vbox1)

        self.hh1 = QHBoxLayout()
        self.hh2 = QHBoxLayout()
        
        self.hh1.addLayout(self.section_vbox1)
        
        #self.hh2.addLayout(self.opr_vbox1)
        
        #self.hh2.addLayout(self.jog) #####################################################################
        self.admin_col2V.addLayout(self.hh1)
        #self.admin_col2V.addLayout(self.hh2, 60)

        #self.admin_col2V.addLayout(self.section_vbox1,40)
        #self.admin_col2V.addLayout(self.opr_vbox1,60)
        

        self.admin_mainH.addLayout(self.admin_col1V,45)
        self.admin_mainH.addLayout(self.admin_col2V,55)

        self.tab1.setLayout(self.admin_mainH)



def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()