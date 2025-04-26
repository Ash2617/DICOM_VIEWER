import json
import os
from DICOM_VIEWER.config.paths import RECENT_FILES_PATH

MAX_RECENT = 5

def load_recent_files():
    if os.path.exists(RECENT_FILES_PATH):
        with open(RECENT_FILES_PATH, "r") as f:
            if f:
                return json.load(f)
    return []

def save_recent_files(recent_list):
    with open(RECENT_FILES_PATH, "w") as f:
        json.dump(recent_list[:MAX_RECENT], f)
