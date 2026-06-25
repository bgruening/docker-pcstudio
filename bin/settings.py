# from PyQt5 import QtCore
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QPushButton
from studio_classes import QCheckBox_custom
from PyQt5 import QtCore  #, QtGui
from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QMessageBox,
)
from PyQt5.QtGui import QIntValidator
# from vis_tab import MainPlotWindow   # later maybe
try:
    from galaxy_ie_helpers import put, find_matching_history_ids, get
except:
    print("----- cannot import from galaxy_ie_helpers ")
    pass

class StudioSettings(QWidget):
    def __init__(self, gui_w, min_size_flag, vis_tab):   # use dict eventually
        super().__init__()

        self.gui_w = gui_w
        self.min_size = min_size_flag
        self.fixed_plot_flag = True
        self.vis_tab = vis_tab

        self.pat_id = None

        stylesheet = """ 
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; } 

            """

        self.setStyleSheet(stylesheet)
        
        #-------------------------------------------
        self.scroll = QScrollArea()
        self.vbox = QVBoxLayout()
        glayout = QGridLayout()

        #------------
        idx_row = 0
        self.min_size_checkbox = QCheckBox_custom('min size (1100x790)')
        self.min_size_checkbox.setChecked(self.min_size)
        self.min_size_checkbox.clicked.connect(self.toggle_min_size_cb)
        idx_row += 1
        glayout.addWidget(self.min_size_checkbox, idx_row,0,1,2) # w, row, column, rowspan, colspan

        #  future possibility of a floating Plot window
        # self.fixed_plot_checkbox = QCheckBox_custom('Fixed Plot window')
        # self.fixed_plot_checkbox.setChecked(self.fixed_plot_flag)
        # self.fixed_plot_checkbox.clicked.connect(self.toggle_fixed_plot_cb)
        # idx_row += 1
        # glayout.addWidget(self.fixed_plot_checkbox, idx_row,0,1,2) # w, row, column, rowspan, colspan

        idx_row += 1
        self.get_github_PAT_button = QPushButton("get GitHub PAT: History ID=")
        self.get_github_PAT_button.setFixedWidth(200)
        self.get_github_PAT_button.setEnabled(True)
        self.get_github_PAT_button.setStyleSheet("background-color: lightgreen;")
        self.get_github_PAT_button.clicked.connect(self.github_PAT_cb)
        glayout.addWidget(self.get_github_PAT_button, idx_row, 0, 1, 2)

        self.pat_id_w = QLineEdit("0")
        self.pat_id_w.setEnabled(True)
        self.pat_id_w.setFixedWidth(70)
        self.pat_id_w.setValidator(QIntValidator())
        self.pat_id_w.textChanged.connect(self.PAT_id_changed)
        glayout.addWidget(self.pat_id_w, idx_row, 2, 1, 1)

        self.vbox.addLayout(glayout)

        #----------
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: lightgreen;")
        # self.close_button.setFixedWidth(150)
        self.close_button.clicked.connect(self.close_settings_cb)

        self.vbox.addWidget(self.close_button)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.vbox.addWidget(self.close_button)
        # self.layout.setStretch(0,1000)

        self.setLayout(self.vbox)
        self.resize(200, 120)   # try to fix the size

    #----------
    def close_settings_cb(self):
        self.close()

    def toggle_min_size_cb(self):
        if self.min_size_checkbox.isChecked():
            self.gui_w.setMinimumSize(1100, 790)  #width, height of window (avoid hard-coding in future)
        else:
            self.gui_w.setMinimumSize(0, 0)  

    def toggle_fixed_plot_cb(self):
        self.fixed_plot_flag = not self.fixed_plot_flag
        if self.fixed_plot_flag:
            # self.plot_win = MainPlotWindow(self.canvas)
            # self.vis_tab.plot_win.show()
            # self.cells_physiboss_rb.disconnect()
            # self.cells_physiboss_rb.deleteLater()

            # self.scroll_plot.disconnect()
            # self.scroll_plot.deleteLater()
            self.scroll_plot.setWidget(self.canvas) # for an embedded Plot window (not floating)
        else:
            # self.vis_tab.scroll_plot.setWidget(self.vis_tab.canvas) # self.config_params = QWidget()
            if self.vis_tab.plot_win is None:
                self.vis_tab.plot_win = MainPlotWindow(self.vis_tab.canvas)
                self.vis_tab.plot_win.show()
            # self.vis_tab.plot_win.show()

    def github_PAT_cb(self):
        self.pat_id = int(self.pat_id_w.text())
        try:
            msgBox = QMessageBox()
            msgBox.setText(f'Copying the requested data from the Galaxy History')
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            # fid = find_matching_history_ids(self.pat_id)
            # get(fid)
            # if not self.xml_creator.fake_galaxy_flag:
            get(self.pat_id)
            # print("dummy get")
        except:
            print("Unable to get the file from History")
            msgBox = QMessageBox()
            msgBox.setText(f'load_file_cb: Unable to get file with History ID {self.pat_id}. Perhaps you got it previously.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()

    def PAT_id_changed(self, sval):
        try:
            self.pat_id = int(sval)
        except:
            pass
