import numpy as np
import cv2 as cv
import yaml

from modules.feature_point_direction.feature_point_direction import (
    FeaturePointDirection,
)

from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict
from modules.tools.coordinate_transformer import CoordinateTransformer

from point_calculation import PointCalculation
from frame_info import FrameInfo


class BriecheeseInterface:

    def __init__(self, pose_data_source="exif"):
        self.pose_data_source = pose_data_source

        with open("setup.yaml") as file:
            setup_params = yaml.safe_load(file)
            camera_matrix_file = setup_params["camera_matrix"]
            distortion_coefficients_file = setup_params["distortion_coefficients"]

        self.camera_matrix = np.load(camera_matrix_file)
        self.distortion_coefficients = np.load(distortion_coefficients_file)

        self.current_frame_name = None

        self.coordinateTransformer = None
        self.arMakerPoseEstimator = None

        if pose_data_source == "marker":
            if aruco_dict().get(setup_params["aruco_type"], None) is None:
                raise RuntimeError("ArUCo tag type '{args['type']}' is not supported")

            aruco_type = aruco_dict()[setup_params["aruco_type"]]
            self.arMakerPoseEstimator = PoseEstimator(
                aruco_type, self.camera_matrix, self.distortion_coefficients
            )

        fx = self.camera_matrix[0][0]
        fy = self.camera_matrix[1][1]
        cx = self.camera_matrix[0][2]
        cy = self.camera_matrix[1][2]
        self.featurePointDirection = FeaturePointDirection(fx, fy, cx, cy)

        self.data_for_calculation = {}

    def get_camrera_pose_from_marker(self, frame):
        p2k = self.arMakerPoseEstimator.get_pose(frame)

        is_marker_detected = p2k is not None

        if not is_marker_detected:
            raise RuntimeError("no frame positiion data")

        camera_position = p2k.pose.position
        camera_rotation_matrix = p2k.pose.rotMat

        return camera_position, camera_rotation_matrix

    def get_camera_pose_from_lat_lon(self, latitude, longitude, altutude):
        if self.coordinateTransformer is None:
            self.coordinateTransformer = CoordinateTransformer(
                latitude, longitude
            )

        x, y = self.coordinateTransformer.transform_to_x_y(latitude, longitude)

        camera_rotation_matrix = np.array([[ 1., 0., 0.],
                                           [ 0., -1.,  0.],
                                           [-0., 0., -1.]])

        return np.array([x, y, altutude]), camera_rotation_matrix

    def set_frame(self, img_file_name, frame, latitude=None, longitude=None, altutude=None):
        last_frame_name = self.current_frame_name
        self.current_frame_name = img_file_name
        if last_frame_name:
            if self.data_for_calculation[last_frame_name].is_empty():
                self.data_for_calculation.pop(last_frame_name)

        if img_file_name not in self.data_for_calculation:
            try:
                camera_position = None
                camera_rotation_matrix = None

                if self.pose_data_source == "marker":
                    camera_position, camera_rotation_matrix = self.get_camrera_pose_from_marker(frame)
                elif self.pose_data_source == "exif":
                    camera_position, camera_rotation_matrix = self.get_camera_pose_from_lat_lon(latitude, longitude, altutude)
                else:
                    raise RuntimeError("unknown pose data source")

                self.data_for_calculation.update({img_file_name: FrameInfo(frame, camera_position, camera_rotation_matrix)})

                print("camera_position", camera_position)
                print("camera_rotation: ", camera_rotation_matrix)
            except RuntimeError as e:
                print(e)
                self.current_frame_name = None
                raise RuntimeError(e)

        return self.data_for_calculation[self.current_frame_name].get_view_img()

    def set_point(self, x, y):
        self.data_for_calculation[self.current_frame_name].point(x, y)

        feature_point_direction = self.featurePointDirection.get(
                x, y
            )
        return self.data_for_calculation[self.current_frame_name].get_view_img()

    def calculation(self):
        print("start calculation")

        self.pointCalculation = PointCalculation()

        for frameInfo in self.data_for_calculation.values():
            if frameInfo.is_empty():
                continue
            feature_point_direction = self.featurePointDirection.get(
                frameInfo.point_x, frameInfo.point_y
            )

            self.pointCalculation.set_frame(frameInfo.camera_position, frameInfo.camera_rotation_matrix, np.array(feature_point_direction))

        point_position = self.pointCalculation.get_position()[0]
        latitude, longitude = self.coordinateTransformer.transform_to_lat_lon(point_position[0], point_position[1])

        print("")
        print("result: ", )
        print("latitude: ", latitude)
        print("longitude: ", longitude)
        print("altitude: ", point_position[2])
        print("")

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

