import numpy as np
import cv2 as cv
import sys
import argparse
import pathlib
from samples.common.video_streamer import VideoStreamer
from modules.armarker.pose_estimator import PoseEstimator
from modules.armarker.aruco_dict import aruco_dict

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../../")


class App(VideoStreamer):
    def __init__(
        self, src, aruco_dict_type, matrix_coefficients, distortion_coefficients
    ):
        self.matrix_coefficients = matrix_coefficients
        self.distortion_coefficients = distortion_coefficients

        self.arMakerPoseEstimator = PoseEstimator(
            aruco_dict_type, matrix_coefficients, distortion_coefficients
        )

        super().__init__(src)

    def create_view(self, frame):
        p2k = self.arMakerPoseEstimator.get_pose(frame)
        vis = frame.copy()

        if not p2k:
            return vis

        # Draw a square around the markers
        cv.aruco.drawDetectedMarkers(vis, p2k.markerInfo.corners)

        # Draw Axis
        cv.drawFrameAxes(
            vis,
            self.matrix_coefficients,
            self.distortion_coefficients,
            p2k.markerInfo.rvec,
            p2k.markerInfo.tvec,
            0.1,
        )

        if not p2k.pose:
            return vis

        rot_mat = cv.Rodrigues(p2k.markerInfo.rvec)[0]
        p = rot_mat @ p2k.pose.position
        cv.drawFrameAxes(
            vis,
            self.matrix_coefficients,
            self.distortion_coefficients,
            cv.Rodrigues((p2k.pose.rotMat.T))[0],
            p,
            0.1,
        )

        return vis

    def get_commands(self, key):
        super().get_commands(key)

        if key == ord(" "):
            self.arMakerPoseEstimator.set_keyframe()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--Video_src", default=0, help="Video source selection")
    ap.add_argument(
        "-k",
        "--K_Matrix",
        required=True,
        help="Path to calibration matrix (numpy file)",
    )
    ap.add_argument(
        "-d",
        "--D_Coeff",
        required=True,
        help="Path to distortion coefficients (numpy file)",
    )
    ap.add_argument(
        "-t",
        "--type",
        type=str,
        default="DICT_ARUCO_ORIGINAL",
        help="Type of ArUCo tag to detect",
    )
    args = vars(ap.parse_args())

    if aruco_dict().get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    aruco_dict_type = aruco_dict()[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]

    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    video_src = args["Video_src"]

    App(video_src, aruco_dict_type, k, d).run()
