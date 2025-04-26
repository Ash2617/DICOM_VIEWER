import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pydicom
from DICOM_VIEWER.core.dicom_utils import normalize_dicom_image

class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent):
        self.figure, self.ax = plt.subplots()
        super().__init__(self.figure)
        self.parent = parent
        self.setMouseTracking(True)
        self.im = None

    def display_plot(self, file_path, cmap):
        img = pydicom.dcmread(file_path)
        window_center = int(img.get(0x00281050).value)
        window_width = int(img.get(0x00281051).value)
        normalised_image = normalize_dicom_image(img, window_center, window_width)

        if self.im is None:
            self.ax.clear()
            self.im = self.ax.imshow(normalised_image, cmap)
            self.ax.axis("off")
        else:
            self.im.set_data(normalised_image)
            self.im.set_cmap(cmap)

        self.draw()
