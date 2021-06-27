import serial
import cv2
import time
import random
from Constants import constants


class FollowStrategy:
    def __init__(self, motor=0, processPuckHSV=0):
        self.process_puck = processPuckHSV
        self.move_motor = motor
        self.center = (0, 0)
        self.stop = False

    # Follow Puck in width, while remaining on the 3000 line
    def use_strategy(self):
        while not self.stop:
            self.read_position()
    	    self.move_motor.move_x_y_absolute(self.center[1], 3000)

    def read_position(self):
        position, amount_of_frames = self.process_puck.read_position()
        if amount_of_frames == 0:
            return amount_of_frames
        else:
            self.center = position
            return amount_of_frames

if __name__ == "__main__":
    pass

    test = FollowStrategy()
    test.use_strategy()

    print("EXIT")
    exit
