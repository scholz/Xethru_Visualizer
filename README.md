# Xethru Visualizer

## About
* example and supporting classes for plotting xethru baseband and radar frames using pyqtgraph
* for plotting run: xep_simple_plot.y -d <device com port> [-b <if you want baseband>]
* tested on on windows 10 and using the xep board

## Requirements
* python3.6
* pyqt5 (pip install PyQt5)
* pyqtgraph > 0.10 (pip install pyqtgraph)
* xethru module connector


## Module Description
* colormap.py .. defines colormaps which can be used with visualizer (see visualizer:86)
* visualizer.py .. open pyqtgraph window and creates all pyqtgraph objects, holds data queue (dequeue) for data vis
* xep_reader.py .. small threaded helper class which distributes received data to visualizer and potentially other consumers of the xep data
* xep_simple_plot.py .. main script (parses CL, configures XEP, start XEP reader, launches visualizer, registers function of visualizer with reader)
* xep.py .. wrapper (based on exampel from xethru) to configure xep


## License
* This project is licensed under the MIT license.