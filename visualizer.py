# -*- coding: utf-8 -*-
"""
@created on: 2019-07-01
@author: Markus Scholz
@license: MIT
"""

import os
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

from colormap import *
from sys import stdout
from time import clock, time, sleep

import collections
import numpy as np
import copy 
from decimal import Decimal
from collections import deque

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import subprocess
import datetime
from datetime import timedelta
from time import sleep
from struct import unpack_from


class visualizer():


    def __init__(self, app, data_function, frame_start, frame_end, frame_offset, fps):
        
        test_measurement = None
        while test_measurement is None:
            test_measurement = data_function()

        pg.setConfigOption('background', (255,255,255))
        pg.setConfigOption('foreground', (0,0,0))
        self.win=pg.GraphicsWindow(title="Simple Xethru CIR Plotting")
        self.app = app

        waterfall_height = 500

        # define x-axis ticks for distance based on measurement
        x_bin_in_meters = float(frame_end - frame_start) / len(test_measurement)
        x_tick_spacing = int(len(test_measurement) * 0.1)
        x_tick_positions = np.linspace(0,len(test_measurement), len(test_measurement) // x_tick_spacing)
        x_tick_labels = (x_tick_positions * x_bin_in_meters) + frame_start
        x_ticks = [list(zip(x_tick_positions.tolist(), map(str, x_tick_labels)) )]

        # define y-axis ticks for waterfall
        y_time_per_sample = 1. / fps
        y_tick_spacing = int(waterfall_height * 0.1)
        y_tick_positions = np.linspace(0,waterfall_height, waterfall_height // y_tick_spacing)
        y_tick_labels = (y_tick_positions * y_time_per_sample)
        y_tick_labels_str = list(map(lambda x: f"{x:2.1f}", y_tick_labels))
        y_tick_labels_str.reverse()
        y_ticks = [list(zip(y_tick_positions.tolist(), y_tick_labels_str))]


        ## configure single cir plot
        self.p1=self.win.addPlot(title="CIR",col=0,row=0)
        self.p1.setWindowTitle('CIR Plotting')
        self.p1.setRange(QtCore.QRectF(0, 0, len(test_measurement), 10000)) 
        ax=self.p1.getAxis('bottom')
        ax.setTicks(x_ticks)
        self.p1.setLabel('bottom', 'Distance (m)', units='') # had to remove units m as it was doing km for rf frame
        self.p1.setLabel('left', 'Amplitude', units='')
        
        # TODO: probably define this as hard limits
        self.p1.setLimits( yMin = np.min(test_measurement)-2*np.std(test_measurement), yMax = np.max(test_measurement)+2*np.std(test_measurement))
        self.p1.autoLevels = False
        self.c=self.p1.plot(pen='b')

        ## configure waterfall
        self.p2=self.win.addPlot( title="Waterfall",row=1,col=0)
        
        ax=self.p2.getAxis('bottom')
        ax.setTicks(x_ticks)
        ax=self.p2.getAxis('left')
        ax.setTicks(y_ticks)
    
        self.p2.setLabel('bottom', 'Distance (m)', units='')
        self.p2.setLabel('left', 'Time', units='s')
        self.img=np.ones((len(test_measurement),waterfall_height))*0.

        self.img_item=pg.ImageItem(self.img)
        self.p2.addItem(self.img_item)
      
        self.img_item.setLookupTable(colmap_spectrum_2())
            
        self.img_item.setLevels([np.min(test_measurement),np.max(test_measurement)])
        self.img_item.autoLevels=False
        # np array 
        self.measurement_data_queue=[-100]*len(test_measurement)
        self.waterfall=deque([self.measurement_data_queue]*waterfall_height)

        ## configure fps label
        self.fps_label = self.win.addLabel("Sample rate: %f"%fps, row=3, col=0)
        self.last_sample = time()
        self.current_fps_array = deque([1.]*10, maxlen=10)
        self.current_fps = np.mean(np.array(self.current_fps_array))

    def start_plot(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_graphs)
        self.timer.start(5)

    def stop_plot(self):
        self.timer.stop()

    def update_graphs(self):
        self.c.setData(np.array(self.measurement_data_queue) )
        self.waterfall.append(list(self.measurement_data_queue))
        self.waterfall.popleft()
        self.waterfall_arr=np.array(self.waterfall).T
        self.img_item.setImage(self.waterfall_arr, autoLevels=False)
        self.fps_label.setText("Sample rate (Hz): %2.3f "%(self.current_fps))

        self.app.processEvents()  ## force complete redraw for every plot

    def compute_sampling_rate(self):
        new_sample = time()
        current_fps = 1. / float((new_sample - self.last_sample) + 0.000001)
        self.current_fps_array.append(current_fps)
        self.current_fps = np.mean(self.current_fps_array)
        self.last_sample = new_sample

    def push_data(self, data):
        self.measurement_data_queue = data
        self.compute_sampling_rate()



    