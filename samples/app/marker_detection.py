import numpy as np
import cv2 as cv
import sys
import pathlib
import yaml

from frame_stream import FrameStream

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../../")

from samples.common.video_streamer import VideoStreamer
from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict


class MarkerDetection(FrameStream):
    def __init__(self):

        super().__init__()

        with open('setup.yaml') as file:
            setup_params = yaml.safe_load(file)
            camera_matrix_file = setup_params['camera_matrix']
            distortion_coefficients_file = setup_params['distortion_coefficients']

        if aruco_dict().get(setup_params['aruco_type'], None) is None:
            raise RuntimeError("ArUCo tag type '{args['type']}' is not supported")

        self.camera_matrix = np.load(camera_matrix_file)
        self.distortion_coefficients = np.load(distortion_coefficients_file)
        aruco_type = aruco_dict()[setup_params['aruco_type']]

        self.arMakerPoseEstimator = PoseEstimator(
            aruco_type, self.camera_matrix, self.distortion_coefficients
        )

    def create_view(self):

        if self.last_frame.size != 0 and self.pause:
            return self.last_frame

        success, frame = self.cap.read()

        if not success:
            raise RuntimeError('Failed read capture')

        p2k = self.arMakerPoseEstimator.get_pose(frame)
        vis = frame.copy()

        if not p2k:
            return self.encode(vis)

        # Draw a square around the markers
        cv.aruco.drawDetectedMarkers(vis, p2k.markerInfo.corners)

        # Draw Axis
        cv.drawFrameAxes(
            vis,
            self.camera_matrix,
            self.distortion_coefficients,
            p2k.markerInfo.rvec,
            p2k.markerInfo.tvec,
            0.1,
        )

        if not p2k.pose:
            return self.encode(vis)

        rot_mat = cv.Rodrigues(p2k.markerInfo.rvec)[0]
        p = rot_mat @ p2k.pose.position
        cv.drawFrameAxes(
            vis,
            self.camera_matrix,
            self.distortion_coefficients,
            cv.Rodrigues((p2k.pose.rotMat.T))[0],
            p,
            0.1,
        )

        return self.encode(vis)

