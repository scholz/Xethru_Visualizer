# -*- coding: utf-8 -*-
"""
@created on: 2019-07-01
@author: Markus Scholz
@license: MIT
"""

# main application for plotting
import sys
from optparse import OptionParser
from time import sleep

from visualizer import visualizer
from xep import xep
from xep_reader import xep_reader
        
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

def main():
    parser = OptionParser()

    parser.add_option(
        "-d",
        "--device",
        dest="device_name",
        help="device file to use",
        metavar="FILE")
    parser.add_option(
        "-b",
        "--baseband",
        action="store_true",
        default=False,
        dest="baseband",
        help="Enable baseband, rf data is default")

    (options, args) = parser.parse_args()

    if not options.device_name:
        parser.error("Missing -d. See --help.")
    else:
        
        # default configuration
        fps = 60
        frame_offset = 0.18
        frame_start = .9
        frame_end = 9.

        xep_dev = xep(options.device_name)
        xep_dev.configure(dac_min = 950, dac_max = 1150, 
                            frame_offset = frame_offset, frame_start = frame_start, frame_end = frame_end, 
                            baseband = options.baseband, fps = fps)

        xep_dev.start_streaming()
        print(xep_dev.get_sensor_configuration())
        
        target_functions = []
        
        app = QtGui.QApplication([])
        vs = visualizer(app = app, data_function = xep_dev.read_frame, fps = fps, frame_start = frame_start, frame_end = frame_end, frame_offset = frame_offset)

        # start update timer
        vs.start_plot()
        target_functions.append(vs.push_data)

        # create xep reader
        _ = xep_reader(xep_dev.read_frame, target_functions)

        # qt app exec
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

        xep_dev.stop_streaming()

if __name__ == "__main__":
   main()


