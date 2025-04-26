import pydicom
import os
import numpy as np

def load_dicom_folder(folder_path):
    dicom_files = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(".dcm")
    ]
    return dicom_files


def load_dicom_volume(folder_path):
    dicom_files = [
        pydicom.dcmread(os.path.join(folder_path, f))
        for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(".dcm")
    ]
    dicom_files.sort(key=lambda x: int(x.InstanceNumber))  # Ensure correct order
    slices = [ds.pixel_array for ds in dicom_files]
    volume = np.stack(slices, axis=0)

    # slope = float(dicom_files[0].get("RescaleSlope", 1))
    # intercept = float(dicom_files[0].get("RescaleIntercept", 0))
    # volume = volume * slope + intercept

    return volume, dicom_files[0]
