import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
class MoveMotor:
    def __init__(self, processPuckHSV=0):
        self.getPuck = processPuckHSV
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

    # Get the correct coordinates
    def getCoordinates(self):
        position = self.getPuck.getImage()
        return position
    
    def testMove(self):
        pass

    def write(x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data
    while True:
        num = input("Enter a string: ") # Taking input from user
        value = write(num)
        print(value) # printing the value


if __name__ == "__main__":
    pass

    test = MoveMotor()
    test.write()

    print("EXIT")
    exit