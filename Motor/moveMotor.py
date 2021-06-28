import serial
import time
import random
from Constants import constants

#arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
class MoveMotor:
    def __init__(self, processPuckHSV=0):
        self.process_puck = processPuckHSV
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
        self.center = (0,0)

    # Get the correct coordinates
    def getCoordinates(self):
        position = self.process_puck.getImage()
        
        return position
    
    def testMove(self):        
        time.sleep(5)
        self.arduino.write(bytes("calibrate", 'utf-8'))
        time.sleep(5)

        img, amountOfFrames = self.read_position_and_image()
        while amountOfFrames == 0:
            img, amountOfFrames = self.read_position_and_image()

        old_motor_coordinate_width = 0
        old_motor_coordinate_height = 0

        while True:
            img, amountOfFrames = self.read_position_and_image()
            if amountOfFrames == 0:
                continue
            time.sleep(0.5)
            print(self.center[0], self.center[1])
            multiplier_width = constants.MOTOR_WIDTH / constants.FIELD_WIDTH
            motor_coordinate_width = (self.center[1]) * multiplier_width
            motor_coordinate_width = int(motor_coordinate_width)
            multiplier_height = constants.MOTOR_HEIGHT / constants.FIELD_HEIGHT
            motor_coordinate_height = (self.center[0]) * multiplier_height
            motor_coordinate_height = int(motor_coordinate_height)
            if self.center[0] > constants.FIELD_HEIGHT * 0.4:
                motor_coordinate_height = 2000
            motor_coordinate_width = round(motor_coordinate_width, -2)
            motor_coordinate_height = round(motor_coordinate_height, -2)
            #print("Sending: position")
            #self.arduino.write(bytes("position", 'utf-8'))
            #data = self.arduino.readline()
            #print(data)
            #data = str(data)
            #print("Data as String: " + data)
            #whitelist = set('0123456789,')
            #data = ''.join(filter(whitelist.__contains__, data))
            #print("Data number only: " + data)
            #time.sleep(1)
            ready = False
            self.arduino.write(bytes("position", 'utf-8'))
            ready_string = self.arduino.readline()
            print(ready_string)

            if motor_coordinate_width != old_motor_coordinate_width:
                if motor_coordinate_height != old_motor_coordinate_height:
                        #if ready:
                        string = str(motor_coordinate_height) + ',' + str(motor_coordinate_width)
                        #string = "random"
                        print("Sending: " + string)
                        self.arduino.write(bytes(string, 'utf-8'))
                        time.sleep(0.5)
            old_motor_coordinate_width = motor_coordinate_width
            old_motor_coordinate_height = motor_coordinate_height

    def loop(self):
        while True:
            num = input("Enter a string: ") # Taking input from user
            value = self.write(num)
            print(value) # printing the value
    
    def write(self, x):
        self.arduino.write(bytes("calibrate", 'utf-8'))
        time.sleep(0.05)
        data = self.arduino.readline()
        return data

    #def write(x):
     #   arduino.write(bytes(x, 'utf-8'))
      #  time.sleep(0.05)
       # data = arduino.readline()
        #return data
        #while True:
         #   num = input("Enter a string: ") # Taking input from user
          #  value = write(num)
           # print(value) # printing the value
    
    def read_position_and_image(self):
        img, position, amount_of_frames = self.process_puck.read_position_and_image()
        if amount_of_frames == 0:
            return img, amount_of_frames
        else:
            self.center = position
            return img, amount_of_frames


if __name__ == "__main__":
    pass

    test = MoveMotor()
    test.testMove()

    print("EXIT")
    exit