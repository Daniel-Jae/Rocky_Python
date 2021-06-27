import sys
import os
import time
from Camera.CameraStream import VideoStream
from Camera.CameraCalibration import CameraCalibration
from Processing.ProcessField import ProcessField
from Processing.ProcessPuck_Fiducial import ProcessPuck
from Processing.ProcessPuck_HSV import ProcessPuckHSV
from Prediction.pathPrediction import PathPrediction

import cv2
import numpy as np

# new_cameraCalibration = CameraCalibration(camera=0)

newVideoStream = VideoStream(camera=0)

newVideoStream.start()

newProcessField = ProcessField(newVideoStream)

newProcessField.chooseCorner()

hsv = True

if hsv == True:

    newProcessPuckHSV = ProcessPuckHSV(newProcessField)

    newProcessPuckHSV.setHSV()

    newProcessPuckHSV.show_puck()

else:

    newProcessPuckFiducial = ProcessPuck(newProcessField)

    newProcessPuckFiducial.getPuckPositionAlways()

#new_path_prediction = PathPrediction(newProcessPuckHSV)

#new_path_prediction.draw_predicted_path()

newVideoStream.stop()

cv2.destroyAllWindows()
