import vtk

current_iso_value = 500

dicom_path = "/Users/akshukla/CT scans/DCM_test"
 # VTK reader
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dicom_path)
reader.Update()
# Volume mapper
volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())
# Transfer functions for opacity and color
a = 50
color_func = vtk.vtkColorTransferFunction()
color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_func.AddRGBPoint(a, 1.0, 0.5, 0.3)
color_func.AddRGBPoint(1000, 1.0, 1.0, 1.0)

opacity_func = vtk.vtkPiecewiseFunction()
opacity_func.AddPoint(0, 0.0)
opacity_func.AddPoint(500, 0.5)
opacity_func.AddPoint(1000, 1.0)

volume_prop = vtk.vtkVolumeProperty()
volume_prop.SetColor(color_func)
volume_prop.SetScalarOpacity(opacity_func)
volume_prop.ShadeOn()
volume_prop.SetInterpolationTypeToLinear()

        # Volume actor
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_prop)

        # Renderer
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(0.1, 0.1, 0.2)

        # Render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)

        # Interactor
render_interactor = vtk.vtkRenderWindowInteractor()
render_interactor.SetRenderWindow(render_window)

# create a slider representation
slider = vtk.vtkSliderRepresentation2D()
slider.SetMaximumValue(0)
slider.SetMaximumValue(100)
slider.SetValue(50)
slider.SetTitleText("Slider X")

# set slider position (normalised coordinates : 0.0 to 1.0)
slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider.GetPoint1Coordinate().SetValue(0.1, 0.1)
slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider.GetPoint2Coordinate().SetValue(0.4, 0.1)

# create a slider widget
slider_widget = vtk.vtkSliderWidget()
slider_widget.SetInteractor(render_interactor)
slider_widget.SetRepresentation(slider)
slider_widget.SetAnimationModeToAnimate()
slider_widget.EnabledOn()

def slider_callback(obj, event):
    value = obj.GetRepresentation().GetValue()
    a = value * 5
    print("a", a)
    print("value", value)
    color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color_func.AddRGBPoint(a, 1.0, 0.9, 0.9)
    color_func.AddRGBPoint(1000, 1.0, 0.5, 0.0)  
    volume_prop.SetColor(color_func)
    render_window.Render()
    # print(a)

slider_widget.AddObserver("InteractionEvent", slider_callback)


        # Start rendering
render_window.Render()
render_interactor.Initialize()
render_interactor.Start()





# import vtk
# from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# from PyQt6.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QVBoxLayout, QApplication
# from PyQt6.QtCore import Qt
# import sys

# app = QApplication(sys.argv)

# dicom_path = "/Users/akshukla/CT scans/DCM_test"
# current_iso_value = 400

        
# reader = vtk.vtkDICOMImageReader()
# reader.SetDirectoryName(dicom_path)
# reader.Update()

#         # self.surface_extractor = vtk.vtkMarchingCubes()
# surface_extractor = vtk.vtkFlyingEdges3D()
# surface_extractor.SetInputConnection(reader.GetOutputPort())
# surface_extractor.SetValue(0,current_iso_value)
# surface_extractor.Update()

# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(surface_extractor.GetOutputPort())

# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# actor.GetProperty().SetColor(0.9, 0.3, 0.3)
# actor.GetProperty().SetOpacity(1.0)

# renderer = vtk.vtkRenderer()
# renderer.AddActor(actor)
# renderer.SetBackground(0.1, 0.1, 0.2)

# render_window = vtk.vtkRenderWindow()
#         # self.render_window.AddRenderer(self.renderer)


# vtk_widget = QVTKRenderWindowInteractor()



#         # self.vtk_widget = QVTKRenderWindowInteractor(self)
# render_window = vtk_widget.GetRenderWindow()
# render_window.AddRenderer(renderer)
        
# interactor = vtk_widget.GetRenderWindow().GetInteractor()
#         # self.interactor.SetRenderWindow(self.render_window)

#         # # Create an axes actor (you can also use vtkAnnotatedCubeActor)
#         # axes = vtk.vtkAxesActor()
#         # axes.SetTotalLength(3.5, 3.5, 3.5)
#         # axes.SetShaftTypeToCylinder()
#         # axes.SetCylinderRadius(0.02)

#         # # Orientation Marker Widget
#         # self.orientation_widget = vtk.vtkOrientationMarkerWidget()
#         # self.orientation_widget.SetOrientationMarker(axes)
#         # self.orientation_widget.SetInteractor(self.interactor)
#         # self.orientation_widget.SetViewport(0.75, 0.75, 0.95, 0.95)  # bottom-left corner
#         # # self.orientation_widget.SetEnabled(1)
#         # # self.orientation_widget.InteractiveOff()  # prevents user from rotating the widget itself


#         # comment this out and uncomment axis if you want that
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
        
# orientation_widget = vtk.vtkOrientationMarkerWidget()
# orientation_widget.SetOrientationMarker(cube)
# orientation_widget.SetInteractor(interactor)
# orientation_widget.SetViewport(0.0, 0.0, 0.2, 0.2)
#         # self.orientation_widget.SetEnabled(1)
#         # self.orientation_widget.InteractiveOff()



# #         # --- Qt Slider and Label
# slider = QSlider(Qt.Orientation.Horizontal)
# slider.setMinimum(0)
# slider.setMaximum(1500)
# slider.setValue(current_iso_value)
# # slider.valueChanged.connect(update_iso_value)

# label = QLabel(f"Iso Value: {current_iso_value}")

# export_btn = QPushButton("Export to STL")
# # export_btn.clicked.connect(export_stl)

#         # --- Layout
# layout = QVBoxLayout()
# layout.addWidget(vtk_widget)
# layout.addWidget(label)
# layout.addWidget(slider)
# layout.addWidget(export_btn)
# # setLayout(layout)


#         # if parent_scene:
#         #     proxy = QGraphicsProxyWidget()
#         #     proxy.setWidget(self)
#         #     parent_scene.addItem(proxy)

# renderer.ResetCamera()
# render_window.Render()

# camera_widget = vtk.vtkCameraOrientationWidget()
# camera_widget.SetParentRenderer(renderer)
# camera_widget.SetInteractor(interactor)
# camera_widget.On()
# interactor.Initialize()
#         # --- Create the box widget
#         # self.box_widget = vtk.vtkBoxWidget()
#         # self.box_widget.SetInteractor(self.interactor)
#         # self.box_widget.SetPlaceFactor(1.0)  # Tight fit
#         # self.box_widget.SetInputData(self.surface_extractor.GetOutput())
#         # self.box_widget.PlaceWidget()

#         # Register the callback using lambda to pass self
#         # self.box_widget.AddObserver("InteractionEvent", lambda widget, event: self.clip_callback(widget, event))


#         # Enable box outline
#         # self.box_widget.GetOutlineProperty().SetColor(1, 0, 0)
#         # self.box_widget.GetOutlineProperty().SetLineWidth(2)
#         # self.box_widget.On()

# orientation_widget.EnabledOn()
# orientation_widget.InteractiveOff() 
# vtk_widget.Initialize()
#         # self.vtk_widget.Start()
# vtk_widget.GetRenderWindow().Render()

# renderer.ResetCamera()
# render_window.Render()
# vtk_widget.show()
# sys.exit(app.exec())