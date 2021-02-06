import matplotlib.pyplot as plt
import time
import GUI_Jan30Rev

import sys
import csv
import os
from pathlib import Path
import shutil
from datetime import datetime
# datetime object containing current date and time
# now = datetime.now()
# dd/mm/YY H:M:S
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import make_pattern_visual


""" class markVisual():
    def __init__(self):
        super().__init__()
        Main() """


def get_coord_dict(coord_file_name):
    coord_file = open(coord_file_name, 'r')
    coord_dict = {}

    ii = 0
    for line in coord_file.readlines():
        if ii == 1:
            ii = 0
            continue
        line = line.split(',')
        coord_dict[int(line[0])] = (line[1], line[2])
    return coord_dict

def write_gcode(coord_dict, gcode_bp_file):
    g_code_file = open(gcode_bp_file, 'w')

    for ii in range(len(coord_dict)):
        in2mm = 25.4
        xc = int(coord_dict[ii+1][0])*in2mm
        yc = int(coord_dict[ii+1][1])*in2mm
        #line = 'G0 ' + 'X' + coord_dict[ii+1][0] + ' Y' + coord_dict[ii+1][1] + '\n'
        line = 'G0 ' + 'X' + str(xc) + ' Y' + str(yc) + '\n'
        #print(line)
        g_code_file.write(line)
    g_code_file.close()

def animate_pattern(coord_dict,fid):
    x = []
    y = []
    q = []
    for ii in range(len(coord_dict)):
        x = x + [int(coord_dict[ii+1][0])]
        y = y + [int(coord_dict[ii+1][1])]
        q = q + [ii+1]
    #print(x[0:len(x)])
    #print(x[0:len(y)])

    plt.cla()
    plt.clf()

    plt.plot(x, y, marker='o')

    for jj, txt in enumerate(q):
        plt.annotate(txt, (x[jj], y[jj]),size=20)
    #plt.show()

    plt.savefig(fid, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)

    


def MakeVisualMain(pat_name, img_path, gcode_path):
    #coord_file_name = 'plate_coords_test01.csv'
    coord_file_name = pat_name
    #gcode_bp_file = 'gcode_bp_test01.txt'
    gcode_bp_file = gcode_path
    #pic_fid = 'pattern_visual.png'
    pic_fid = img_path
    coord_dict = get_coord_dict(coord_file_name)
    write_gcode(coord_dict, gcode_bp_file)
    animate_pattern(coord_dict, pic_fid)
