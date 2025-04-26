import vtk

def render_3d_volume(dicom_files):
    # VTK reader setup
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_files[0])
    reader.Update()

    # Volume mapper
    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())

    # Transfer functions for opacity and color
    color_func = vtk.vtkColorTransferFunction()
    color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
    color_func.AddRGBPoint(500, 1.0, 0.5, 0.3)
    color_func.AddRGBPoint(1000, 1.0, 1.0, 1.0)

    opacity_func = vtk.vtkPiecewiseFunction()
    opacity_func.AddPoint(0, 0.0)
    opacity_func.AddPoint(500, 0.5)
    opacity_func.AddPoint(1000, 1.0)

    volume_prop = vtk.vtkVolumeProperty()
    volume_prop.SetColor(color_func)
    volume_prop.SetScalarOpacity(opacity_func)

    # Volume actor
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_prop)

    # Renderer setup
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.SetBackground(0.1, 0.1, 0.2)

    # Render window setup
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 800)

    # Interactor setup
    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    render_window.Render()
    render_interactor.Start()
