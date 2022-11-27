import unittest
from unittest.mock import patch

import numpy as np
from scipy.spatial.transform import Rotation as scipy_R
import random

from modules.keyframe_pose.keyframe_pose import KeyframePose
from database.db_protocol import DBProtocol
from database.feature_points_position_db import FeaturePointsPositionDB

from tests.tools.data_manager import DataManager
from tests.tools.generate_data import (
    get_random_points,
    get_random_rotation,
)


class KeyframePoseTest(unittest.TestCase):
    db_table = "test_feature_point_positions_db"
    db_format = "(id INT, x FLOAT, y FLOAT, z FLOAT)"

    def setUp(self):
        DBProtocol(
            self.db_table,
            self.db_format,
        ).delete_all()

    def tearDownAfterClass(self):
        DBProtocol(
            self.db_table,
            self.db_format,
        ).delete_all()

    def test_keyframe_pose(self):
        with patch.dict(
            "os.environ", {"FEATURE_POINTS_POSITION_DB_TABLE": self.db_table}
        ):
            print("start test_keyframe_pose")
            feature_points_position = get_random_points(10, 2, 0, 15)
            cameras_position = get_random_points(2, 2, 0, 1)
            cameras_rotation = get_random_rotation(0, 1, 1)

            data_manager = DataManager(
                feature_points_position,
                cameras_position,
                cameras_rotation,
                "test_keyframe_pose",
            )

            # create feature point positions db for test.
            id_candidates = list(range(100))
            random.shuffle(id_candidates)

            for i, feature_point_position in enumerate(
                data_manager.feature_points_true_position
            ):
                FeaturePointsPositionDB().create(
                    id_candidates[i],
                    feature_point_position[0],
                    feature_point_position[1],
                    feature_point_position[2],
                )

            feature_point_directions = []
            for i, direction in enumerate(data_manager.get_keyframes_bundle(0.0)[0]):
                feature_point_directions.append([id_candidates[i], direction[1]])

            position, rotation = KeyframePose().get_pose(feature_point_directions)

            data_manager.finish()

            # check keyframe position error
            keyframe_position_threshold = 0.1
            evaluate_value = np.linalg.norm(
                data_manager.cameras_true_position[0] - position
            )
            self.assertTrue(evaluate_value < keyframe_position_threshold)

            # check keyframe rotation error
            keyframe_rotation_threshold = 0.1
            rotation_error = data_manager.cameras_true_rotation[0] @ np.linalg.inv(
                rotation
            )
            evaluate_value = scipy_R.from_matrix(rotation_error).as_euler(
                "zxy", degrees=True
            )
            for val in evaluate_value:
                self.assertTrue(val < keyframe_rotation_threshold)
            print("finish test_keyframe_pose")


if __name__ == "__main__":
    unittest.main()
