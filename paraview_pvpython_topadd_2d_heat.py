#!/usr/bin/pvpython
 
# References
# 1. https://www.paraview.org/Wiki/VTK/Examples/Python/vtkUnstructuredGridReader
# 2. https://cmake.org/pipermail/paraview/2010-November/019265.html

from paraview.simple import *

import vtk
import math

import os
from os.path import exists
dir_path = os.path.dirname(os.path.realpath(__file__))


def main(iterNum):
    # The source file
    iterNumStr = str(iterNum)
    fileName = "{}/output_{}.vtu".format(dir_path, iterNumStr.zfill(5))
    
   
    if (exists(fileName)):
        # Read the source file.
        reader = XMLUnstructuredGridReader(FileName=fileName)
        dp = Show(reader)
        dp.UpdatePipeline()
        
        view = paraview.simple.GetActiveViewOrCreate('RenderView')
        view.Background = [1.0, 1.0, 1.0]
        view.ViewSize = [1920, 1920]
        view.UseLight = 0
        view.OrientationAxesVisibility = 0
        view.ResetCamera()
        
        ColorBy(dp, ('CELLS', 'xPhys'))
        Render()
        
        # reset view to fit data
        view.ResetCamera()
        # reset view to fit data bounds
        view.ResetCamera(0.0, 80.0, 0.0, 80.0, 0.0, 0.0)
        # current camera placement for renderView1
        view.InteractionMode = '2D'
        view.CameraPosition = [40.0, 40.0, 218.5640646055102]
        view.CameraFocalPoint = [40.0, 40.0, 0.0]
        view.CameraParallelScale = 56.568542494923804

        saveFileName = "{}/output_{}_1.png".format(dir_path, iterNumStr.zfill(5))
        SaveScreenshot(saveFileName, ImageResolution=[3840, 2160])
        
        Hide(reader, view)

        
        
        # Threshold 1
        thres1 = Threshold(reader)
        thres1.Scalars = ['CELLS', 'xPassive0']
        thres1.ThresholdRange = [0.1, 1.0]
        
        dp1 = Show(thres1, view)
        dp1.AmbientColor = [1, 1, 1]
        dp1.Representation = 'Surface'
        ColorBy(dp1, ("CELLS", "xPassive0"))
        lut = GetColorTransferFunction('xPassive0')
        lut.ApplyPreset('X Ray', True)
        lut.RGBPoints = [1, 0.92, 0.92, 0.92,
                     1.00024, 1, 1, 1]
        Render()
        # save screenshot
        saveFileName = "{}/output_{}_2.png".format(dir_path, iterNumStr.zfill(5))
        SaveScreenshot(saveFileName, ImageResolution=[3840, 2160])

        Hide(thres1, view)
        
        # Threshold 2
        thres2 = Threshold(thres1)
        thres2.Scalars = 'xPhys'
        thres2.ThresholdRange = [0.5, 1]
        dp2 = Show(thres2)
        dp2.AmbientColor = [1, 1, 1]
        dp2.Representation = 'Surface'
        ColorBy(dp2, ("CELLS", "xPhys"))
        lut = GetColorTransferFunction('xPhys')
        lut.ApplyPreset('X Ray', True)
        lut.RGBPoints = [0, 0, 1, 1,
                         1, 0, 1, 1]
        Render() 
        
#        thres3 = Threshold(reader)
#        thres3.Scalars = 'xPassive1'
#        thres3.ThresholdRange = [0.0, 1]
#        dp3 = Show(thres3)
#        dp3.AmbientColor = [1, 1, 1]
#        dp3.Representation = 'Surface'
#        ColorBy(dp3, ("CELLS", "xPassive1"))
#        lut = GetColorTransferFunction('xPassive1')
#        lut.ApplyPreset('X Ray', True)
#        lut.RGBPoints = [0, 1, 0, 0,
#                         1, 1, 0, 0]
#        Render() 
        
        thres4 = Threshold(reader)
        thres4.Scalars = 'xPassive2'
        thres4.ThresholdRange = [0.1, 3]
        dp4 = Show(thres4)
        dp4.AmbientColor = [1, 1, 1]
        dp4.Representation = 'Surface'
        ColorBy(dp4, ("CELLS", "xPassive2"))
        lut = GetColorTransferFunction('xPassive2')
        lut.ApplyPreset('X Ray', True)
        lut.RGBPoints = [0, 1, 0, 0,
                         1, 1, 0, 0]
        Render() 
        
#        thres5 = Threshold(reflect1)
#        thres5.Scalars = 'xPassive3'
#        thres5.ThresholdRange = [0.0, 1]
#        dp5 = Show(thres5)
#        dp5.AmbientColor = [1, 1, 1]
#        dp5.Representation = 'Surface'
#        ColorBy(dp5, ("CELLS", "xPassive3"))
#        lut = GetColorTransferFunction('xPassive3')
#        lut.ApplyPreset('X Ray', True)
#        lut.RGBPoints = [0, 0, 0, 1,
#                         1, 0, 0, 1]
#        Render() 
        
        Hide(thres1, view)

        #save screenshot
        saveFileName = "{}/output_{}_3.png".format(dir_path, iterNumStr.zfill(5))
        SaveScreenshot(saveFileName, ImageResolution=[3840, 2160])
        
        
        Hide(thres4, view)
        #Hide(thres3, view)
        Hide(thres2, view)
        
        # Output stl file
        view.UseLight = 1
        light1 = AddLight(view=view)        # Create a new 'Light'
        light1.Position = [0.0, 1.0, 1.0]
        light1.Intensity = 1.0
        cleantoGrid1 = CleantoGrid(Input=reader)
        thres1.Input = cleantoGrid1
        SetActiveSource(thres1)
        thres1.Scalars = ['CELLS', 'xPhys']
        thres1.ThresholdRange = [0.5, 1.0]
        extractSurface1 = ExtractSurface(Input=thres1) # extract surface
        extractSurface1Display = Show(extractSurface1, view)
        Hide(thres1, view)
        # Properties modified on transform2.Transform
        #transform1 = Transform(registrationName='Transform', Input=extractSurface1)
        #transform1.Transform = 'Transform'
        #transform1.Transform.Translate = [-50.0, 0.0, 0.0]
        #transform1.Transform.Rotate = [90.0, 0.0, 0.0]
        linearExtrusion1 = LinearExtrusion(Input=extractSurface1)
        # Properties modified on linearExtrusion1
        linearExtrusion1.ScaleFactor = 10.0
        linearExtrusion1Display = Show(linearExtrusion1, view)
        Hide(extractSurface1, view)
        view.InteractionMode = '3D'
        view.ResetCamera(0.01666666753590107, 1.9833333492279053, 0.03333333507180214, 0.9666666388511658, 0.0, 1.0)
        extractSurface2 = ExtractSurface(Input=linearExtrusion1)
        extractSurface2Display = Show(extractSurface2, view)
        Hide(linearExtrusion1, view)
        triangulate1 = Triangulate(Input=extractSurface2)
        triangulate1Display = Show(triangulate1, view)
        #ColorBy(triangulate1Display, None)
        Hide(extractSurface2, view)
        SetActiveSource(triangulate1)
        Show(triangulate1)
        
        # current camera placement for view
        view.CameraPosition = [193, 56, 155]
        view.CameraFocalPoint = [40, 40, 1]
        view.CameraViewUp = [-0.037, 0.997, -0.07]
        view.CameraParallelScale = 1.5
        
        # save screenshot
        saveFileName = "{}/output_{}_4.png".format(dir_path, iterNumStr.zfill(5))
        SaveScreenshot(saveFileName,TransparentBackground=1, ImageResolution=[7680, 4320])
        
        # save stl file
        saveStlName = "{}/TopADD_2D_extruded_3D_model_clean_to_grid_triangulate.stl".format(dir_path)
        SaveData(saveStlName, proxy=triangulate1)


# Make sure main is only called when the file is executed
if __name__ == "__main__":
        iterNum = 0
        if len(sys.argv) > 1:
                iterNum = sys.argv[1]

        main(iterNum)
