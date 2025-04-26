import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
RECENT_FILES_PATH = os.path.join(PROJECT_DIR, "resources", "recent.json")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller bundle """
    if getattr(sys, 'frozen', False):  # Running from a PyInstaller bundle
        base_path = sys._MEIPASS  # PyInstaller extracts files here
    else:
        base_path = os.path.abspath(".")
        # print(f"Base path: {base_path}")
        # print(f"Relative path: {relative_path}")
        # print(f"Full path: {os.path.join(base_path, "DICOM_VIEWER", relative_path)}")

    return os.path.join(base_path, "DICOM_VIEWER", relative_path)