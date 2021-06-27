import cv2
import math
import numpy as np
from Camera.cameraOutput import VideoOutput

from Constants import constants


class PathPrediction:
    def __init__(self, processPuckHSV=0):
        self.process_puck = processPuckHSV
        self.center_old = np.array([0, 0])
        self.center_new = np.array([0, 0])
        self.time_between = 0

    # Return speed as ??? and direction as a vector with length of one
    def calculate_speed_and_direction(self):
        # centers must be np.arrays. example: np.array([420, 69])
        diff = self.center_new - self.center_old

        # length of vector -> np.linalg.norm(diffs)... at least in our 1-D Array
        length = np.linalg.norm(diff)

        if length == 0:
            normalized_vector = np.array([0, 0])
            speed = 0
        else:
            normalized_vector = diff / length
            if self.time_between == 0:
                speed = 0
            else:
                speed = length / self.time_between

        return speed, normalized_vector

    # TODO: Invert x and y when you get position in ProcessPuck
    # self.center_new -> np.array([50, 200])
    # x = 50
    # y = 200
    #               -------
    #               |     |
    # height (y) -> |     |
    #               |     |
    #      (0,0) -> ------- <-- Roboter-side
    #  width (x) -> <     >
    def predictPath(self):
        speed, direction = self.calculate_speed_and_direction()
        field_height = constants.FIELD_HEIGHT_PATH
        field_width = constants.FIELD_WIDTH_PATH

        # Puck doesn't move towards either goal
        if direction[1] == 0:
            remaining_distance = 0
            predicted_x = None
            predicted_y = None
        # Puck moves towards human
        else:
            if direction[1] > 0:
                predicted_y = constants.FIELD_HEIGHT_PATH
            else:
                predicted_y = 0
            remaining_distance = predicted_y - (self.center_new[1])
            multiplicator = abs(remaining_distance / direction[1])
            predicted_position = self.center_new + (multiplicator * direction)
            predicted_x = predicted_position[0]

        return speed, direction, predicted_x, predicted_y

    def draw_predicted_path(self):
        img, cropped_img, amountOfFrames = self.read_position_and_image()
        while amountOfFrames == 0:
            img, cropped_img, amountOfFrames = self.read_position_and_image()
        video_shower = VideoOutput(img).start()

        while True:
            key = cv2.waitKey(1)
            if key == 13 or key == ord("q"):
                break

            img, cropped_img, amountOfFrames = self.read_position_and_image()
            if amountOfFrames == 0:
                cv2.rectangle(
                    img,
                    (constants.PUCK_RADIUS, constants.PUCK_RADIUS),
                    (
                        constants.FIELD_HEIGHT - constants.PUCK_RADIUS,
                        constants.FIELD_WIDTH - constants.PUCK_RADIUS,
                    ),
                    (255, 0, 0),
                    3,
                )
                video_shower.frame = img
                continue

            speed, direction, predicted_x, predicted_y = self.predictPath()
            start_point = self.center_new

            if predicted_x is None:
                cv2.rectangle(
                    img,
                    (constants.PUCK_RADIUS, constants.PUCK_RADIUS),
                    (
                        constants.FIELD_HEIGHT - constants.PUCK_RADIUS,
                        constants.FIELD_WIDTH - constants.PUCK_RADIUS,
                    ),
                    (255, 0, 0),
                    3,
                )
                video_shower.frame = img
                continue
            else:
                bounces = abs(math.floor(predicted_x / constants.FIELD_WIDTH_PATH))

            if bounces == 0:
                remaining_distance = abs(predicted_y - start_point[1])
                multiplicator = abs(remaining_distance / direction[1])
                end_point = start_point + (multiplicator * direction)
                # Draw Line from start_point to end_point
                start_tuple = (int(start_point[1]), int(start_point[0]))
                end_tuple = (int(end_point[1]), int(end_point[0]))
                cv2.line(cropped_img, start_tuple, end_tuple, (0, 0, 255), 5)
            else:
                direction_before_bounce = np.copy(direction)
                direction_after_bounce = np.copy(direction)
                direction_after_bounce[0] = direction_after_bounce[0] * -1
                if predicted_x > 0:
                    for i in range(bounces):
                        if i % 2 == 0:
                            remaining_distance_x = constants.FIELD_WIDTH_PATH - (
                                start_point[0]
                            )
                            multiplicator = abs(remaining_distance_x / direction[0])
                            end_point = start_point + (
                                multiplicator * direction_before_bounce
                            )
                        else:
                            remaining_distance_x = start_point[0]
                            multiplicator = abs(remaining_distance_x / direction[0])
                            end_point = start_point + (
                                multiplicator * direction_after_bounce
                            )
                        # Draw Line from start_point to end_point
                        start_tuple = (int(start_point[1]), int(start_point[0]))
                        end_tuple = (int(end_point[1]), int(end_point[0]))
                        cv2.line(cropped_img, start_tuple, end_tuple, (0, 255, 0), 5)
                        start_point = end_point

                else:
                    for i in range(bounces):
                        if i % 2 == 0:
                            remaining_distance_x = start_point[0]
                            multiplicator = abs(remaining_distance_x / direction[0])
                            end_point = start_point + (
                                multiplicator * direction_before_bounce
                            )
                        else:
                            remaining_distance_x = constants.FIELD_WIDTH_PATH - (
                                start_point[0]
                            )
                            multiplicator = abs(remaining_distance_x / direction[0])
                            end_point = start_point + (
                                multiplicator * direction_after_bounce
                            )
                        # Draw Line from start_point to end_point
                        start_tuple = (int(start_point[1]), int(start_point[0]))
                        end_tuple = (int(end_point[1]), int(end_point[0]))
                        cv2.line(cropped_img, start_tuple, end_tuple, (255, 0, 0), 5)
                        start_point = end_point

                # Draw last line towards goal-line
                remaining_distance_y = abs(predicted_y - start_point[1])
                multiplicator = abs(remaining_distance_y / direction[1])

                if bounces % 2:
                    end_point = start_point + (multiplicator * direction_after_bounce)
                else:
                    end_point = start_point + (multiplicator * direction_before_bounce)
                # Draw Line from start_point to end_point
                start_tuple = (int(start_point[1]), int(start_point[0]))
                end_tuple = (int(end_point[1]), int(end_point[0]))
                cv2.line(cropped_img, start_tuple, end_tuple, (0, 0, 255), 5)

            img[
                constants.PUCK_RADIUS : (constants.FIELD_WIDTH - constants.PUCK_RADIUS),
                constants.PUCK_RADIUS : (
                    constants.FIELD_HEIGHT - constants.PUCK_RADIUS
                ),
            ] = cropped_img
            cv2.rectangle(
                img,
                (constants.PUCK_RADIUS, constants.PUCK_RADIUS),
                (
                    constants.FIELD_HEIGHT - constants.PUCK_RADIUS,
                    constants.FIELD_WIDTH - constants.PUCK_RADIUS,
                ),
                (255, 0, 0),
                3,
            )
            video_shower.frame = img

    def read_position(self):
        pass

    # t
    def read_position_and_image(self):
        img, position, amount_of_frames = self.process_puck.read_position_and_image()
        if amount_of_frames > 0:
            crop_height = constants.FIELD_HEIGHT - constants.PUCK_RADIUS
            crop_width = constants.FIELD_WIDTH - constants.PUCK_RADIUS
            cropped_img = img[
                constants.PUCK_RADIUS : (constants.FIELD_WIDTH - constants.PUCK_RADIUS),
                constants.PUCK_RADIUS : (
                    constants.FIELD_HEIGHT - constants.PUCK_RADIUS
                ),
            ]
            self.center_old = self.center_new
            self.center_new = (
                np.array([position[1], position[0]]) - constants.PUCK_RADIUS
            )
        else:
            cropped_img = img.copy()
        return img, cropped_img, amount_of_frames


if __name__ == "__main__":

    print("EXIT")
    exit
