import numpy as np
import cv2 as cv

from collections import namedtuple

from .armarker import ARMarker


PoseToKeyframe = namedtuple("PoseToKeyframe", "pose, markerInfo")
MarkerInfo = namedtuple("MarkerInfo", "rvec, tvec, corners")
Pose = namedtuple("Pose", "rotMat, position")


class PoseEstimator(ARMarker):
    def __init__(self, aruco_dict_type, matrix_coefficients, distortion_coefficients):

        super().__init__(aruco_dict_type, matrix_coefficients, distortion_coefficients)

        self.current_frame_pose = None  # in armarker coordinate.

    def get_pose_in_marker_coordinate(self, rvec, tvec):
        rot_mat = cv.Rodrigues(rvec)[0]
        rot_mat = np.linalg.inv(rot_mat)
        position = -rot_mat @ tvec[0][0]

        return Pose(rotMat=rot_mat, position=position)

    def get_pose(self, frame):

        try:
            rvec, tvec, corners = self.detect_marker(frame)
        except ValueError as error:
            print(error)
            return

        self.current_frame_pose = self.get_pose_in_marker_coordinate(rvec, tvec)

        markerInfo = MarkerInfo(rvec=rvec, tvec=tvec, corners=corners)

        return PoseToKeyframe(pose=self.current_frame_pose, markerInfo=markerInfo)
