import sys
import os
import time
from Camera.CameraStream import VideoStream
from Processing.ProcessField import ProcessField
from Processing.ProcessPuck_Fiducial import ProcessPuck
from Processing.ProcessPuck_HSV import ProcessPuckHSV


# ROOT_DIR = os.path.dirname(os.path.abspath("start.py"))
# print(ROOT_DIR)


newVideoStream = VideoStream()

newVideoStream.start()

newProcessField = ProcessField(newVideoStream)

newProcessField.chooseCorner()

newProcessPuckHSV = ProcessPuckHSV(newProcessField)

newProcessPuckHSV.getPuckPositionAlways()

# test.start()
# test.update()
# time.sleep(10)
# test.read()

# print(sys.version)
# print(sys.executable)
# for p in sys.path:
#    print(p)
# print(os.environ["PYTHONPATH"])
