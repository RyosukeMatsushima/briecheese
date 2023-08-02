import copy
import cv2 as cv

class FrameInfo:
    def __init__(self, raw_img, camera_position, camera_rotation_matrix):

        self.raw_img = copy.deepcopy(raw_img)
        self.camera_position = camera_position
        self.camera_rotation_matrix = camera_rotation_matrix

        self.point_x = None
        self.point_y = None

    def point(self, x, y):
        self.point_x = x
        self.point_y = y

    def get_view_img(self):
        view_img = copy.deepcopy(self.raw_img)

        if self.point_x and self.point_y:
            cv.circle(view_img, (self.point_x, self.point_y), 6, (0, 0, 255), -1)

        return view_img

    def is_empty(self):
        return self.point_x == None or self.point_y == None

    def get_info_to_calculate(self):
        if self.point_x and self.point_y:
            return self.raw_img, self.camera_position, self.camera_rotation_matrix, self.point_x, self.point_y

        return None

