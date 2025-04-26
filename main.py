import sys, os
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if hasattr(sys, '_MEIPASS'):
    # Running from a PyInstaller bundle
    # ROOT_DIR = sys._MEIPASS
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys._MEIPASS)))))
    print("Running from PyInstaller bundle", ROOT_DIR)
else:
    # Running normally (dev environment)
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Running normally (dev environment):", ROOT_DIR)
sys.path.insert(0, ROOT_DIR)


# Ensure root directory is in sys.path      -- Debugging stuff
# print("Absolute Path:", os.path.abspath(__file__))
# print("Directory Name:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print("Root Directory:", ROOT_DIR)
from gui.main_window import run_main_window

if __name__ == "__main__":
    run_main_window()