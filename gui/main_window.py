from PyQt6.QtWidgets import QMainWindow, QMenu, QWidget, QPushButton, QVBoxLayout, QSlider, QComboBox, QFileDialog,QApplication,QSizePolicy
from PyQt6.QtGui import QAction
import sys, os, json
from DICOM_VIEWER.core.dicom_reader import load_dicom_folder, load_dicom_volume
from DICOM_VIEWER.gui.matplotlib_widget import MatplotlibWidget
from DICOM_VIEWER.gui.dicom_v1 import Ui_MainWindow
from DICOM_VIEWER.gui.mpr_viewer import MPRViewer
from DICOM_VIEWER.config.paths import RECENT_FILES_PATH
from DICOM_VIEWER.utils.recent_manager import load_recent_files, save_recent_files
from DICOM_VIEWER.threeD_rendering.volume_view import VolumeViewer

MAX_RECENT = 5

class DICOM(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect tool buttons and stacked widget
        # slice
        self.ui.toolButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        # MPR
        self.ui.toolButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.toolButton_2.clicked.connect(self.launch_mpr_viewer)

        # 3D
        self.ui.toolButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.toolButton_3.clicked.connect(self.open_3d_viewer)

        self.plotWidget = MatplotlibWidget(self)
        self.dicom_files = []
        self.current_index = 0
        self.folder_path = None

        layout = QVBoxLayout(self.ui.frame)
        self.ui.frame.setLayout(layout)
        layout.addWidget(self.plotWidget)

        self.ui.actionOpen_folder.triggered.connect(self.load_dicom_folder)

        self.ui.horizontalSlider_6.setMinimum(0)
        self.ui.horizontalSlider_6.setEnabled(False)
        self.ui.horizontalSlider_6.valueChanged.connect(self.update_frame)


        self.recent_menu = QMenu("Recent Files", self)
        self.ui.menuFile.addMenu(self.recent_menu)

        self.recent_files = load_recent_files()
        self.recent_menu.clear()
        self.update_recent_menu()

        # added lambda function because triggered passed a bool, checked : bool, which gets passed to folder_path
        self.ui.actionOpen_folder.triggered.connect(lambda: self.load_dicom_folder())
        self.ui.actionRecent.triggered.connect(self.show_recent_files)


        
        # self.dropdown = QComboBox()
        # self.dropdown.addItems(list(plt.colormaps()))
        # self.dropdown.currentTextChanged.connect(self.dropdown_selection_changed)
        # self.layout.addWidget(self.dropdown)

        # self.setCentralWidget(self.main_widget)
        # self.show()

    def load_dicom_folder(self, folder_path=None):
        if folder_path is None:
            self.folder_path = QFileDialog.getExistingDirectory(self, "Open DICOM folder")
        if folder_path:
            self.folder_path = folder_path
            self.dicom_files = load_dicom_folder(folder_path)
            if self.dicom_files:
                self.ui.horizontalSlider_6.setEnabled(True)
                self.ui.horizontalSlider_6.setMaximum(len(self.dicom_files) - 1)
                self.ui.horizontalSlider_6.setValue(0)
                self.current_index = 0
                self.plotWidget.display_plot(self.dicom_files[self.current_index], 'gray')
                self.ui.label.setText(f"{self.current_index+1}/{len(self.dicom_files)}")
                self.launch_mpr_viewer()
                self.add_to_recent(folder_path)

    def update_frame(self, value):
        if self.current_index != value:
            self.current_index = value
            self.plotWidget.display_plot(self.dicom_files[self.current_index], 'gray')
            self.ui.label.setText(f"{self.current_index+1}/{len(self.dicom_files)}")

    def dropdown_selection_changed(self, text):
        self.plotWidget.display_plot(self.dicom_files[self.current_index], text)

    def launch_mpr_viewer(self):
        if not self.dicom_files:
            return

        folder_path = os.path.dirname(self.dicom_files[0])
        volume, dicom_metadata = load_dicom_volume(folder_path)


        # self.fig, self.axes = plt.subplots(1,3, figsize=(12,4))
        # self.canvas = FigureCanvas(self.fig)
        # self.ui.horizontalLayout_3.addWidget(self.canvas)

        self.ui.axial.setScaledContents(True)
        self.ui.axial.setMinimumSize(226,226)
        self.ui.axial.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.coronal.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.sagittal.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.coronal.setScaledContents(True)
        self.ui.coronal.setMinimumSize(226,226)
        self.ui.sagittal.setScaledContents(True)
        self.ui.sagittal.setMinimumSize(226,226)
        self.mpr = MPRViewer(volume, dicom_metadata, self.ui.axial, self.ui.coronal, self.ui.sagittal)


        # sliders will change the view in MPR window
        self.ui.axial_slider.setMaximum(volume.shape[0]-1)
        self.ui.axial_slider.setValue(self.mpr.axial_index)
        self.ui.axial_slider.valueChanged.connect(self.mpr.update_axial)
        self.ui.coronal_slider.setMaximum(volume.shape[1]-1)
        self.ui.coronal_slider.setValue(self.mpr.coronal_index)
        self.ui.coronal_slider.valueChanged.connect(self.mpr.update_coronal)
        self.ui.sagittal_slider.setMaximum(volume.shape[2]-1)
        self.ui.sagittal_slider.setValue(self.mpr.sagittal_index)
        self.ui.sagittal_slider.valueChanged.connect(self.mpr.update_sagittal)

    
    def show_recent_files(self):
        if os.path.exists(RECENT_FILES_PATH):
            with open(RECENT_FILES_PATH, "r") as f:
                recent_files =  json.load(f)
            
            for path in recent_files:
                action = QAction(path, self)
                action.triggered.connect(lambda checked, p=path: self.load_dicom_folder(p))

        return []
    
    def add_to_recent(self, path):
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:MAX_RECENT]
        save_recent_files(self.recent_files)
        self.update_recent_menu()

    def update_recent_menu(self):
        self.recent_menu.clear()
        for path in self.recent_files:
            action = QAction(os.path.basename(path), self)
            action.setToolTip(path)
            action.triggered.connect(lambda _, p=path: self.load_dicom_folder(p))
            self.recent_menu.addAction(action)

    def open_3d_viewer(self):
        if self.folder_path:
            self.viewer_window = VolumeViewer(self.folder_path, self.ui.GLview)
            layout = QVBoxLayout(self.ui.GLview)  # or QHBoxLayout
            layout.setContentsMargins(0, 0, 0, 0)  # Optional: make it edge-to-edge
            layout.addWidget(self.viewer_window)
            self.viewer_window.show()
        else:
            dicom_dir = QFileDialog.getExistingDirectory(self, "Select DICOM Folder")
            if dicom_dir:
                self.viewer_window = VolumeViewer(dicom_dir, self.ui.GLview)
                self.viewer_window.show()


def run_main_window():
    app = QApplication(sys.argv)
    window = DICOM()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DICOM()
    window.show()
    sys.exit(app.exec())