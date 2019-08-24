# -*- coding: utf-8 -*-
"""
@created on: 2019-07-01
@author: Markus Scholz
@license: MIT
"""

# xep reader - simple process to continuously read out xep frames
from threading import Thread

class xep_reader():

    def __init__(self, data_function, target_functions):
        serial_thread=Thread(target=self.push_data, args=(data_function,target_functions))
        serial_thread.daemon=True
        serial_thread.start()

    def push_data(self, data_function, target_functions):
        # pushes radar data to target functions
        while True:
            data = data_function()
            if data is not None:
                for f in target_functions:
                    f(data)
