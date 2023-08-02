import numpy as np
import cv2 as cv
import yaml

from modules.feature_point_direction.feature_point_direction import (
    FeaturePointDirection,
)

from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict

from point_calculation import PointCalculation
from frame_info import FrameInfo


class BriecheeseInterface:

    def __init__(self):

        with open("setup.yaml") as file:
            setup_params = yaml.safe_load(file)
            camera_matrix_file = setup_params["camera_matrix"]
            distortion_coefficients_file = setup_params["distortion_coefficients"]

        if aruco_dict().get(setup_params["aruco_type"], None) is None:
            raise RuntimeError("ArUCo tag type '{args['type']}' is not supported")

        self.camera_matrix = np.load(camera_matrix_file)
        self.distortion_coefficients = np.load(distortion_coefficients_file)
        aruco_type = aruco_dict()[setup_params["aruco_type"]]

        self.arMakerPoseEstimator = PoseEstimator(
            aruco_type, self.camera_matrix, self.distortion_coefficients
        )

        fx = self.camera_matrix[0][0]
        fy = self.camera_matrix[1][1]
        cx = self.camera_matrix[0][2]
        cy = self.camera_matrix[1][2]
        self.featurePointDirection = FeaturePointDirection(fx, fy, cx, cy)

        self.pointCalculation = PointCalculation()

        self.data_for_calculation = {}
        self.current_frame_name = None

    def get_camrera_pose_from_maker(self, frame):
        p2k = self.arMakerPoseEstimator.get_pose(frame)

        is_marker_detected = p2k is not None

        if not is_marker_detected:
            raise RuntimeError("no frame positiion data")

        camera_position = p2k.pose.position
        camera_rotation_matrix = p2k.pose.rotMat

        return camera_position, camera_rotation_matrix

    def set_frame(self, img_file_name, frame):
        last_frame_name = self.current_frame_name
        self.current_frame_name = img_file_name
        if last_frame_name:
            if self.data_for_calculation[last_frame_name].is_empty():
                self.data_for_calculation.pop(last_frame_name)

        if img_file_name not in self.data_for_calculation:
            try:
                camera_position, camera_rotation_matrix = self.get_camrera_pose_from_maker(frame)
                self.data_for_calculation.update({img_file_name: FrameInfo(frame, camera_position, camera_rotation_matrix)})
            except RuntimeError as e:
                print(e)
                self.current_frame_name = None
                raise RuntimeError(e)

        return self.data_for_calculation[self.current_frame_name].get_view_img()

    def set_point(self, x, y):
        self.data_for_calculation[self.current_frame_name].point(x, y)
        return self.data_for_calculation[self.current_frame_name].get_view_img()

    def calculation(self):

        for frameInfo in self.data_for_calculation.values():
            if frameInfo.is_empty():
                continue
            print(frameInfo.point_x, frameInfo.point_y)
            feature_point_direction = self.featurePointDirection.get(
                frameInfo.point_x, frameInfo.point_y
            )

            self.pointCalculation.set_frame(frameInfo.camera_position, frameInfo.camera_rotation_matrix, np.array(feature_point_direction))

        print("yhaaaaaaaaaaaaaaaaaaaaaa")
        print(self.pointCalculation.get_position())

    def get_point_position(self):
        return get_position()

    def encode(self, image):
        ret, frame = cv.imencode(".jpg", image)
        self.last_frame = frame
        return frame

    def draw_feature_points(self, view, rvec, tvec):
        for feature_point_position_data in self.feature_point_positions_db.get_all():
            view = self.draw_point(
                view,
                feature_point_position_data[0],
                feature_point_position_data[1:],
                rvec,
                tvec,
            )

        return view

    def draw_point(self, view, feature_point_id, point, rvec, tvec):
        imgpt, jac = cv.projectPoints(
            point, rvec, tvec, self.camera_matrix, self.distortion_coefficients
        )

        imgpt = tuple(imgpt[0][0].astype(int))

        if min(imgpt) < 0:
            return view

        cv.circle(view, imgpt, 6, (0, 0, 255), -1)

        view = self.draw_text(
            view, "id_" + str(feature_point_id), (imgpt[0], imgpt[1] - 10)
        )

        return view

    def draw_armarker(self, view, p2k):

        marker_position_from_camera_coordinate = p2k.markerInfo.tvec[0][0]
        marker_rotation_vector_from_camera_coordinate = p2k.markerInfo.rvec[0][0]
        ar_marker_corners = p2k.markerInfo.corners

        rvec = marker_rotation_vector_from_camera_coordinate,
        tvec = marker_position_from_camera_coordinate,
        corners = ar_marker_corners,

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

    def draw_position_value(self, view, position, origin_pixel):
        text = "'position' x: {:3.2f} y: {:3.2f} z: {:3.2f}".format(
            position[0], position[1], position[2]
        )

        return self.draw_text(view, text, origin_pixel)

    def draw_rotation_value(self, view, rotation_matrix, origin_pixel):
        roll, pitch, yaw = R.from_matrix(rotation_matrix).as_euler("zyx", degrees=True)
        text = "'rotation' roll: {:3.2f} pitch: {:3.2f} yaw: {:3.2f}".format(
            roll, pitch, yaw
        )

        return self.draw_text(view, text, origin_pixel)

    def draw_text(self, view, text, origin_pixel):
        cv.putText(
            view,
            text=text,
            org=origin_pixel,
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 0, 0),
            thickness=2,
            lineType=cv.LINE_4,
        )

        return view
