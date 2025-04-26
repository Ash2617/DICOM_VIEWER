# 🩻 DICOM Viewer Project

A cross-platform application for viewing and interacting with DICOM medical imaging data. Built with PyQt6, matplotlib, and VTK for 2D/3D visualization and MPR (Multi-Planar Reconstruction).

---

## 📦 Features

- 📁 Load and parse DICOM files
- 🖼️ Display 2D slices using matplotlib
- 🎛️ GUI controls for navigating through image slices
- 🧠 Multi-Planar Reconstruction (MPR) views
- 🧊 3D volume rendering using VTK
- 🎨 Support for custom colormaps

---

<!-- ## 📸 Screenshots -->

<!-- *(Insert screenshots here once the GUI is working)* -->

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DICOM_Viewer_Project.git
cd DICOM_Viewer_Project
```

### 2. Set up virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\\Scripts\\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python gui/main_window.py
```

### 🧰 Project Structure

```bash
DICOM_Viewer_Project/
├── core/                # DICOM processing logic (reading, processing, volume handling)
│   ├── dicom_reader.py  # Reading and parsing DICOM files
│   ├── dicom_volume.py  # Loading 3D volume data
│   └── dicom_utils.py   # Utility functions for DICOM processing
├── gui/                 # PyQt6 interface components
│   ├── main_window.py   # The main window for the application
│   ├── mpr_viewer.py    # Multi-Planar Reconstruction viewer
│   └── controls.py      # UI elements like buttons and sliders
├── 3d_rendering/        # VTK for 3D volume rendering
│   ├── vtk_renderer.py  # VTK rendering logic
│   └── vtk_utils.py     # Utility functions for 3D visualization
├── assets/              # Icons, images, and other assets
├── tests/               # Unit tests for functionality
├── config/              # Configuration files for the app
└── requirements.txt     # List of project dependencies


```

### 🔧 Requirements

- Python 3.6+
- Operating System: Cross-platform (Windows, macOS, Linux)
- Dependencies listed in requirements.txt

#### Feel free to modify the Run the application step according to your actual entry point.
#### If you're unsure of the necessary dependencies or need any clarifications, feel free to ask!