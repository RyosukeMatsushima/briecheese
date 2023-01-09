import numpy as np
import cv2 as cv
from scipy.spatial.transform import Rotation as R
import yaml

import sys
import pathlib

from frame_stream import FrameStream

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../../")

from samples.common.video_streamer import VideoStreamer
# from modules.main.main import Main
from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict


class BriecheeseInterface(FrameStream):
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

        #self.briecheese = Main()
        self.mode = 'create_map' # mode: 'create_map' or 'get_pose'

    def do_next_frame(self):

        if self.last_frame.size != 0 and self.pause:
            return self.last_frame

        success, frame = self.cap.read()

        if not success:
            raise RuntimeError('Failed read capture')

        frame_view = frame.copy()
        value_view = np.ones(frame.shape, np.uint8) * 205

        p2k = self.arMakerPoseEstimator.get_pose(frame)

        is_marker_detected = p2k is not None

        if is_marker_detected:
            marker_position_from_camera_coordinate = p2k.markerInfo.tvec[0][0]
            marker_rotation_vector_from_camera_coordinate = p2k.markerInfo.rvec[0][0]

            camera_position = p2k.pose.position
            camera_rotation_matrix = p2k.pose.rotMat

            ar_marker_corners = p2k.markerInfo.corners

            frame_view = self.draw_armarker(frame_view, marker_rotation_vector_from_camera_coordinate, marker_position_from_camera_coordinate, ar_marker_corners)

            if self.mode == 'create_map':
                self.create_map(frame, camera_position, camera_rotation_matrix)

            feature_point_positions = np.float32([[0.1, 0.1, 0.],
                                                  [-0.1, 0.1, 0.],
                                                  [-0.1, -0.1, 0.],
                                                  [0.1, -0.1, 0.],
                                                  [0.1, 0.1, 0.1],
                                                  [-0.1, 0.1, 0.1],
                                                  [-0.1, -0.1, 0.1],
                                                  [0.1, -0.1, 0.1]])

            frame_view = self.draw_feature_points(frame_view, feature_point_positions, marker_rotation_vector_from_camera_coordinate, marker_position_from_camera_coordinate)

            value_view = self.draw_text(value_view, 'pose from armarker', (10, 15))
            value_view = self.draw_position_value(value_view, camera_position, (10, 35))
            value_view = self.draw_rotation_value(value_view, camera_rotation_matrix, (10, 55))

        return self.encode(cv.hconcat([frame_view, value_view]))

    def create_map(self, frame, observed_position, observed_rotation):
        return
        #self.briecheese.add_keyframe(frame, observed_rotation, observed_rotation)

    def get_pose(self, frame):
        return
        #self.briecheese.get_pose(frame)

    def draw_armarker(self, view, rvec, tvec, corners):

        # Draw a square around the markers
        cv.aruco.drawDetectedMarkers(view, corners)

        # Draw Axis
        cv.drawFrameAxes(
            view,
            self.camera_matrix,
            self.distortion_coefficients,
            rvec,
            tvec,
            0.1,
        )
        return view

    def draw_feature_points(self, view, points, rvec, tvec):
        imgpts, jac = cv.projectPoints(points, rvec, tvec, self.camera_matrix, self.distortion_coefficients)

        for point in imgpts:
            point = tuple(point[0].astype(int))

            cv.circle(view,point, 6, (0,0,255), -1)

        return view

    def draw_position_value(self, view, position, origin_pixel):
        text = "'position' x: {:3.2f} y: {:3.2f} z: {:3.2f}".format(position[0],
                                                                    position[1],
                                                                    position[2])

        return self.draw_text(view, text, origin_pixel)

    def draw_rotation_value(self, view, rotation_matrix, origin_pixel):
        roll, pitch, yaw = R.from_matrix(rotation_matrix).as_euler('zyx', degrees=True)
        text = "'rotation' roll: {:3.2f} pitch: {:3.2f} yaw: {:3.2f}".format(roll, pitch, yaw)

        return self.draw_text(view, text, origin_pixel)

    def draw_text(self, view, text, origin_pixel):

        cv.putText(view,
                   text=text,
                   org=origin_pixel,
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.5,
                   color=(0, 0, 0),
                   thickness=2,
                   lineType=cv.LINE_4)

        return view
