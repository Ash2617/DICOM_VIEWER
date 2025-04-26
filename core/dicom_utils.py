import numpy as np
import pydicom

def normalize_dicom_image(img, window_center, window_width):
    pixels = img.pixel_array
    rescale_intercept = int(img.get(0x00281052).value)
    rescale_slope = int(img.get(0x00281053).value)

    window_min = window_center - window_width / 2
    window_max = window_center + window_width / 2

    rescaled_img = pixels * rescale_slope + rescale_intercept
    clipped_image = np.clip(rescaled_img, window_min, window_max)
    normalised_image = ((clipped_image - window_min) / (window_max - window_min) * 255).astype(np.uint8)

    return normalised_image
