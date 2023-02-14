import numpy as np
import cv2 as cv
from scipy.spatial.transform import Rotation as R
import yaml

from frame_stream import FrameStream

from modules.main.main import Main
from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict
from database.feature_points_position_db import FeaturePointsPositionDB


class BriecheeseInterface(FrameStream):
    def __init__(self):

        super().__init__()

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

        self.frameStream = FrameStream()

        self.briecheese = self.init_briecheese(self.camera_matrix)
        self.feature_point_positions_db = FeaturePointsPositionDB()
        self.mode = "create_map"  # mode: 'create_map' or 'get_pose'
        self.modes = ["create_map", "get_pose"]

    def init_briecheese(self, camera_matrix):

        fx = camera_matrix[0][0]
        fy = camera_matrix[1][1]
        cx = camera_matrix[0][2]
        cy = camera_matrix[1][2]

        return Main(fx, fy, cx, cy)

    # TODO: remove - this function is just for debug.
    def init_db(self):
        self.feature_point_positions_db.delete_all()
        feature_point_positions = np.float32(
            [
                [0.1, 0.1, 0.0],
                [-0.1, 0.1, 0.0],
                [-0.1, -0.1, 0.0],
                [0.1, -0.1, 0.0],
                [0.1, 0.1, 0.1],
                [-0.1, 0.1, 0.1],
                [-0.1, -0.1, 0.1],
                [0.1, -0.1, 0.1],
            ]
        )
        for i, point in enumerate(feature_point_positions):
            self.feature_point_positions_db.create(i, point[0], point[1], point[2])

    def do_next_frame(self):

        if self.last_frame.size != 0 and self.pause:
            return self.last_frame

        frame = self.frameStream.next_frame()

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

            frame_view = self.draw_armarker(
                frame_view,
                marker_rotation_vector_from_camera_coordinate,
                marker_position_from_camera_coordinate,
                ar_marker_corners,
            )

            if self.mode == "create_map":
                self.create_map(frame, camera_position, camera_rotation_matrix)

            frame_view = self.draw_feature_points(
                frame_view,
                marker_rotation_vector_from_camera_coordinate,
                marker_position_from_camera_coordinate,
            )

            value_view = self.draw_text(value_view, "pose from armarker", (10, 15))
            value_view = self.draw_position_value(value_view, camera_position, (10, 35))
            value_view = self.draw_rotation_value(
                value_view, camera_rotation_matrix, (10, 55)
            )

        if self.mode == "get_pose":
            position, rotation = self.get_pose(frame)
            print("get_pose result position: {} rotation: {}".format(position, rotation))
            # TODO: draw outupt to value_view.

        return self.encode(cv.hconcat([frame_view, value_view]))

    def create_map(self, frame, observed_position, observed_rotation):
        self.briecheese.add_frame(frame, observed_position, observed_rotation)

    def get_pose(self, frame):
        return self.briecheese.get_pose(frame)

    def change_mode(self, mode):
        if mode not in self.modes:
            raise ValueError("invalid mode: {}".format(mode))

        self.mode = mode
        self.frameStream = FrameStream()

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

        cv.circle(view, imgpt, 6, (0, 0, 255), -1)
        view = self.draw_text(
            view, "id_" + str(feature_point_id), (imgpt[0], imgpt[1] - 10)
        )

        return view

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
