import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt6.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QVBoxLayout, QFileDialog,QGraphicsProxyWidget
from PyQt6.QtCore import Qt
# from DICOM_VIEWER.gui.main_window import DICOM

class VolumeViewer(QWidget):
    def __init__(self, dicom_path, parent_frame=None):
        super().__init__(parent_frame)

        self.dicom_path = dicom_path
        self.current_iso_value = 400

        print(parent_frame, dicom_path)
        
        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName(self.dicom_path)
        self.reader.Update()

        # self.surface_extractor = vtk.vtkMarchingCubes()
        self.surface_extractor = vtk.vtkFlyingEdges3D()
        self.surface_extractor.SetInputConnection(self.reader.GetOutputPort())
        self.surface_extractor.SetValue(0, self.current_iso_value)
        self.surface_extractor.Update()

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.surface_extractor.GetOutputPort())
        self.mapper.ScalarVisibilityOff()  # Disable scalar visibility to avoid color mapping

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(1.0, 1.0, 1.0)
        self.actor.GetProperty().SetOpacity(0.5)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(0.0, 0.0, 0.0)

        self.render_window = vtk.vtkRenderWindow()
        # self.render_window.AddRenderer(self.renderer)


        self.vtk_widget = QVTKRenderWindowInteractor(self)


        # self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.render_window = self.vtk_widget.GetRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        # self.interactor.SetRenderWindow(self.render_window)

        # # Create an axes actor (you can also use vtkAnnotatedCubeActor)
        # axes = vtk.vtkAxesActor()
        # axes.SetTotalLength(3.5, 3.5, 3.5)
        # axes.SetShaftTypeToCylinder()
        # axes.SetCylinderRadius(0.02)

        # # Orientation Marker Widget
        # self.orientation_widget = vtk.vtkOrientationMarkerWidget()
        # self.orientation_widget.SetOrientationMarker(axes)
        # self.orientation_widget.SetInteractor(self.interactor)
        # self.orientation_widget.SetViewport(0.75, 0.75, 0.95, 0.95)  # bottom-left corner
        # # self.orientation_widget.SetEnabled(1)
        # # self.orientation_widget.InteractiveOff()  # prevents user from rotating the widget itself


        # comment this out and uncomment axis if you want that
        # cube = vtk.vtkAnnotatedCubeActor()
        # cube.SetXPlusFaceText('Right')
        # cube.SetXMinusFaceText('Left')
        # cube.SetYPlusFaceText('Front')
        # cube.SetYMinusFaceText('Back')
        # cube.SetZPlusFaceText('Top')
        # cube.SetZMinusFaceText('Bottom')
        # cube.GetTextEdgesProperty().SetColor(0.0, 0.0, 0.0)
        # cube.GetTextEdgesProperty().SetLineWidth(1)
        # cube.GetCubeProperty().SetColor(0.85, 0.85, 0.85)
        
        # self.orientation_widget = vtk.vtkOrientationMarkerWidget()
        # self.orientation_widget.SetOrientationMarker(cube)
        # self.orientation_widget.SetInteractor(self.interactor)
        # self.orientation_widget.SetViewport(0.0, 0.0, 0.1, 0.1)
        # self.orientation_widget.SetEnabled(1)
        # self.orientation_widget.InteractiveOff()



        # --- Qt Slider and Label
        # self.slider = QSlider(Qt.Orientation.Horizontal)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(1500)
        # self.slider.setValue(self.current_iso_value)
        # self.slider.valueChanged.connect(self.update_iso_value)

        # self.label = QLabel(f"Iso Value: {self.current_iso_value}")

        # self.export_btn = QPushButton("Export to STL")
        # self.export_btn.clicked.connect(self.export_stl)

        # --- Layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.vtk_widget)
        # layout.addWidget(self.label)
        # layout.addWidget(self.slider)
        # layout.addWidget(self.export_btn)
        # self.setLayout(layout)


        # if parent_scene:
        #     proxy = QGraphicsProxyWidget()
        #     proxy.setWidget(self)
        #     parent_scene.addItem(proxy)

        self.renderer.ResetCamera()
        self.render_window.Render()

#       keep for later, was displaying too big at the centre of screen
        # self.camera_widget = vtk.vtkCameraOrientationWidget()
        # self.camera_widget.SetParentRenderer(self.renderer)
        # self.camera_widget.SetInteractor(self.interactor)
        # self.camera_widget.On()

        self.interactor.Initialize()

        # --- Create the box widget
        # self.box_widget = vtk.vtkBoxWidget()
        # self.box_widget.SetInteractor(self.interactor)
        # self.box_widget.SetPlaceFactor(1.0)  # Tight fit
        # self.box_widget.SetInputData(self.surface_extractor.GetOutput())
        # self.box_widget.PlaceWidget()

        # Register the callback using lambda to pass self
        # self.box_widget.AddObserver("InteractionEvent", lambda widget, event: self.clip_callback(widget, event))


        # Enable box outline
        # self.box_widget.GetOutlineProperty().SetColor(1, 0, 0)
        # self.box_widget.GetOutlineProperty().SetLineWidth(2)
        # self.box_widget.On()

        # self.orientation_widget.EnabledOn()
        # self.orientation_widget.InteractiveOff() 

        self.vtk_widget.Initialize()
        # self.vtk_widget.Start()
        self.vtk_widget.GetRenderWindow().Render()

        self.renderer.ResetCamera()
        self.render_window.Render()
        self.vtk_widget.show()
        # self.interactor.Start()

    # --- Callback to update cut geometry
    def clip_callback(self, widget, event):
        box = vtk.vtkPlanes()
        widget.GetPlanes(box)

        # Use this box to clip the surface
        clipper = vtk.vtkExtractPolyDataGeometry()
        clipper.SetInputConnection(self.surface_extractor.GetOutputPort())
        clipper.SetImplicitFunction(box)
        clipper.Update()

        self.mapper.SetInputConnection(clipper.GetOutputPort())
        self.render_window.Render()

        self.clipped_output = clipper.GetOutputPort()



    def update_iso_value(self, value):
        self.current_iso_value = value
        self.label.setText(f"Iso Value: {value}")
        self.surface_extractor.SetValue(0, value)
        self.surface_extractor.Update()

        # Force update box widget to recalculate clip
        if self.box_widget:
            self.box_widget.PlaceWidget()

    
        self.render_window.Render()

    def export_stl(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save STL", "output_model.stl", "STL files (*.stl)")
        if not file_path:
            return

        writer = vtk.vtkSTLWriter()
        writer.SetFileName(file_path)
        if hasattr(self, 'clipped_output'):
            writer.SetInputConnection(self.clipped_output)
        else:
            writer.SetInputConnection(self.surface_extractor.GetOutputPort())

        writer.Write()