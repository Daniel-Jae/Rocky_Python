import sys
import time
from Camera.CameraStream import VideoStream

test = VideoStream()

test.start()
test.update()
time.sleep(10)
test.read()

print(sys.version)
print(sys.executable)
