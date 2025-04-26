from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSlider, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import numpy as np
from io import BytesIO

class MPRViewer:
    def __init__(self, volume, dicom_metadata, label_axial, label_coronal, label_sagittal):
        # super().__init__(parent)
        self.volume = volume
        self.dicom_metadata = dicom_metadata
        self.axial = label_axial
        self.coronal = label_coronal
        self.sagittal = label_sagittal

        self.axial_index = self.volume.shape[0] // 2
        self.coronal_index = self.volume.shape[1] // 2
        self.sagittal_index = volume.shape[2] // 2

        self.im_axial = None
        self.im_coronal = None
        self.im_sagittal = None

        self.draw_views()

    
    def slice_to_pixmap(self, img):
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        ax.imshow(img, cmap='gray')
        ax.axis('off')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        buf.seek(0)
        img_data = buf.read()
        qimg = QImage.fromData(img_data)
        pixmap = QPixmap.fromImage(qimg)
        return pixmap
    
    def apply_windowing(self, img_slice):
        intercept = int(self.dicom_metadata.get(0x00281052).value if self.dicom_metadata.get(0x00281052) else 0)
        slope = int(self.dicom_metadata.get(0x00281053).value if self.dicom_metadata.get(0x00281053) else 1)

        center = int(self.dicom_metadata.get(0x00281050).value)
        width = int(self.dicom_metadata.get(0x00281051).value)

        img = img_slice * slope + intercept
        img = np.clip(img, center - width / 2, center + width / 2)
        img = ((img - (center - width / 2)) / width * 255).astype(np.uint8)
        return img

    def draw_views(self):
        axial_slice = self.apply_windowing(self.volume[self.axial_index, :, :])
        coronal_slice = self.apply_windowing(self.volume[:, self.coronal_index, :])
        sagittal_slice = self.apply_windowing(self.volume[:, :, self.sagittal_index])

        self.axial.setPixmap(self.slice_to_pixmap(axial_slice))
        self.coronal.setPixmap(self.slice_to_pixmap(coronal_slice))
        self.sagittal.setPixmap(self.slice_to_pixmap(sagittal_slice))


    def update_axial(self, val):
        self.axial_index = val
        self.refresh()
    
    def update_coronal(self, val):
        self.coronal_index = val
        self.refresh()
    
    def update_sagittal(self, val):
        self.sagittal_index = val
        self.refresh()

    def refresh(self):
        self.draw_views()