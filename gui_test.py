import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,  QFrame, QVBoxLayout, QLabel, QSlider, QCheckBox, QAction
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.cm
import math
from functools import partial

from pyvistaqt import QtInteractor, MainWindow
from reader import load_dataset_mat, create_mesh
import time

width = 1280; height = 720


class MyMainWindow(MainWindow):

    def __init__(self, parent=None, show=True):
        QMainWindow.__init__(self, parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setWindowTitle("Voltage Map V1.0")
        self.addVoltageMap = False
        self.addEdges = False

        filename = "./data/dataset_2.mat"
        points, indices, fields = load_dataset_mat(filename)
        mesh = create_mesh(points, indices)
        voltage = [0 if math.isnan(x) else x for x in fields.bipolar_voltage]

        self.mesh = mesh
        self.voltage = voltage

        # create the frame
        self.frame = QFrame()
        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        # add the slide to adjust resolution
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TicksLeft)
        self.slider.valueChanged.connect(self.valuechange)
        self.label = QLabel()
        self.cb1 = QCheckBox("Voltage Map")
        self.cb1.setChecked(False)
        self.cb1.stateChanged.connect(self.changeVoltageMap)
        self.cb2 = QCheckBox("Add Edges")
        self.cb2.setChecked(False)
        self.cb2.stateChanged.connect(self.changeEdges)
        
        grid = QVBoxLayout()
        grid.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)
        grid.addWidget(self.slider)
        grid.addWidget(self.cb1)
        grid.addWidget(self.cb2)
        self.frame.setLayout(grid)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_mesh_action = QAction('Add Mesh', self)
        self.add_mesh_action.triggered.connect(partial(self.add_mesh, 0))
        meshMenu.addAction(self.add_mesh_action)

        if show:
            self.show()

    def valuechange(self):
        print("#################", self.add_mesh(self.slider.value()))
        self.add_mesh(self.slider.value())

    def changeVoltageMap(self, state):
        if state == Qt.Checked:
            self.addVoltageMap = True
        else:
            self.addVoltageMap = False
        self.add_mesh(self.slider.value())
    
    def changeEdges(self, state):
        if state == Qt.Checked:
            self.addEdges = True
        else:
            self.addEdges = False
        print("self.addEdges: ", self.addEdges)
        self.add_mesh(self.slider.value())


    def add_mesh(self, target_reduction):
        """ add a sphere to the pyqt frame """
        target_reduction = target_reduction / 100
        if self.addEdges is True:
            edgesBool = True
        else:
            edgesBool = False

        default_scalar_bar_args = dict(
        interactive=False,
        color="#363737", 
        title_font_size=12,
        label_font_size=11,
        n_labels=2,
        below_label=" ",
        above_label=" ",
        vertical=False,
        width=0.3,
        height=0.05,
        position_x=0.025)

        default_add_mesh_kws = {
        "style": "surface",
        "show_edges": edgesBool,
        # "smooth_shading": True,  
        "annotations": False,
        "cmap": matplotlib.cm.jet_r,
        # "cmap": ['green', 'red'],
        "clim": (0, 2),
        "above_color": "magenta",
        "below_color": "brown",
        "nan_color": "gray",
        "name": "mesh",
        "opacity": 1.0}

        default_add_mesh_kws["scalar_bar_args"] = default_scalar_bar_args

        decimated_mesh = self.mesh.decimate_pro(target_reduction)

        if self.addVoltageMap is True:
            mesh_points_list = np.array(self.mesh.points).tolist()
            decimated_mesh_points_list = np.array(decimated_mesh.points).tolist()
            
            time_start = time.time()
            index_list = []
            for item in decimated_mesh_points_list:
                    index_list.append(mesh_points_list.index(item))
        
            bipolar_voltage = self.voltage
            decimated_voltage = []
            for index in index_list:
                decimated_voltage.append(bipolar_voltage[index])
            time_end = time.time()
            print("time diff: ", time_end - time_start)
        
            self.plotter.add_mesh(
                mesh=decimated_mesh,
                scalars=decimated_voltage,
                **default_add_mesh_kws,
            )
        else:
            self.plotter.add_mesh(
                mesh=decimated_mesh,
                **default_add_mesh_kws,
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())




