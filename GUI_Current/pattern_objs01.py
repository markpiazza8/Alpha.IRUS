import sys
import csv
import os
import serial
import time
import io
from pathlib import Path
import shutil
from datetime import datetime
import math
import numpy as np


class PlatePattern:
    '''An object of this class represents a calibrated pattern info'''
    def __init__(self, pat_name, main_doc_path):
        # main_doc_path is path to the Alpha.IRUS folder
        self._name = pat_name
        self._pat_csv = main_doc_path + '/Torque Patterns/' + pat_name + '/Torque_Pattern.csv'
        #self._pat_fid = None
        #self._run_doc = None
        self._xy_offset = ()
        self._phi = 0
        self._iterN = 0
        self._fastN = 0

        #self._fastN = 0 # need to define number of fasteners
        #self._iterN = 0 # need to define number of iterations


        with open(self._pat_csv, 'r') as csvfile:
            csv_content = csv.reader(csvfile, delimiter = ',')
            fN = 0
            for row in csv_content:

                if row[0].isnumeric():
                    fN = fN+1
                
                
                if (fN > 0 and len(row)-4 != self._iterN and self._iterN != None):
                    print('ERROR: the pattern has rows with different length')

                self._iterN = len(row) - 4

            self._fastN = fN
                    
        csvfile.close()


    def set_offset(self, xy_offset):
        self._xy_offset = xy_offset

    def set_phi(self, phi):
        self._phi = int(phi)

class FastenerNode:

    def __init__(self, que, nom_xyp, targT, final_nomT, fracT):
        self._que = que
        self._nom_xyp = nom_xyp
        self._nom_xyw = ()
        self._targT = targT
        self._final_nomT = final_nomT
        self._fracT = fracT
        self._gcode_w = None
        self._gcode_p = None

        # documentation attributes
        self._act_xy = []
        self._appT = None

        self._next = None

class PatternLinkedList:

    def __init__(self):
        self._A_matrix = None
        self._rQ_vector = None

        self._head = None

    def find_fast_node(self, que):
        '''
        This method will search for a node in LinkedList that has _word
        attribute word and will return that node if found and otherwise None

        Parameters: word is the string that is meant to be compared the _word
        attributes of the LinkedList's Nodes

        Returns: None if a fasterner node with the queue attribute doesn't
        exist or Node if Node._que = word exists

        Precondition: queue is a int

        Post-cond: current is a Node object
        '''
        if self._head == None:
            return(None)
        current = self._head
        while current._next != None:
            if current._que == que:
                return(current)
            current = current._next
        return(None)

    def is_empty(self):
        '''
        returns Boolean indicating if the list contains any nodes

        Parameters: None

        Returns: True is any nodes exists and False otherwise

        Precondition: None

        Post-cond: True or False
        '''
        return(self._head == None)

    def head(self):
        '''
        GETTER: returns a reference to the first node in the ll,
        None if ll is empty
        '''
        if self._head == None:
            return None
        return self._head

    """ def get_next(self, node):
        if node._next == None:
            return None
        
        g_string = node._n ext._gcode"""


    def add2Queue(self, node):
        ''' add fastener node the the back of the LinkedList queue'''
        if self._head == None:
            self._head = node
        else:
            current = self._head

            while current._next != None:
                current = current._next
            current._next = node

    def set_work_coords(self, A, rQ):
        self._A_matrix = A
        self._rQ_vector = rQ

        current = self._head
        in2mm = 25.4
        in2mm = 1 # they are already converted to inches prior to method being called
        while current != None:
            
            xyp_vec = np.array([[current._nom_xyp[0], current._nom_xyp[1]]]).T
            xyw_vec = rQ/in2mm + np.matmul(A, xyp_vec/in2mm) # should be in inches 
            xw = xyw_vec[0]
            xw = xw[0]
            yw = xyw_vec[1]
            yw = yw[0]
            gc = 'G0 X' + str(xw*25.4) + ' Y' + str(yw*25.4) + '\n'
            current._nom_xyw = (float(xw), float(yw))
            current._gcode_w = gc 

            current = current._next

    def create_plate_pattern_list(self, platePat):
        # platePat must be a platePattern object
        
        with open(platePat._pat_csv, 'r') as csvfile:
            csv_content = csv.reader(csvfile, delimiter = ',')
            fN = 0
            
            for iter in range(platePat._iterN):
                j = iter + 4
                csvfile.seek(0)
                for row in csv_content:
                    # getting info from pattern csv file
                    que = int(row[0]) + iter*platePat._fastN
                    
                    T_final = float(row[3])
                    fracT = float(row[j])
                    T_targ = T_final*fracT
                    xyp = (float(row[1]), float(row[2]))

                    gc = 'G0 X' + str(float(row[1])*25.4) + ' Y' + str(float(row[2])*25.4) + '\n'

                    fast_node = FastenerNode(que, xyp, T_targ, T_final, fracT) # create fastener node
                    fast_node._gcode_p = gc
                    self.add2Queue(fast_node) # add fastener node to end of LinkedList (queue)

            

                    
        csvfile.close()

    def disp(self):
        
        current = self._head
        #print(current)

        while current != None:
            line = [current._que, current._nom_xyp, current._nom_xyw, str(math.floor(current._targT)) + '/' + str(math.floor(current._final_nomT))]
            print(line)
            current = current._next



""" def main():

    master_path = 'C:/Users/markp/OneDrive/Documents/AME 498 - Sr Design/First Draft Code/Alpha_IRUS'
    name = 'PatternF'

    plate_pat = PlatePattern(name, master_path)
    pattern = PatternLinkedList()
    pattern.create_plate_pattern_list(plate_pat)
    pattern.disp()

    nn = pattern.head()
    while nn._next != None:
        print(nn._gcode_p)
        nn = nn._next

    
  
main()  """
