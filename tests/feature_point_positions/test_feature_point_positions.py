import unittest
from unittest.mock import patch

import numpy as np
import random

from modules.feature_point_positions.feature_point_positions import (
    FeaturePointPositions,
)
from database.db_protocol import DBProtocol
from database.feature_points_position_db import FeaturePointsPositionDB

from tests.tools.data_manager import DataManager
from tests.tools.generate_data import (
    get_random_points,
    get_random_rotation,
)


class FeaturePointPositionsTest(unittest.TestCase):
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

    def test_feature_point_positions(self):
        with patch.dict(
            "os.environ", {"FEATURE_POINTS_POSITION_DB_TABLE": self.db_table}
        ):
            print("start test_feature_point_positions")
            feature_points_position = get_random_points(3, 4, 2, 10)
            cameras_position = get_random_points(2, 2, 0, 10)
            cameras_rotation = get_random_rotation(0, 1, 10)

            data_manager = DataManager(
                feature_points_position,
                cameras_position,
                cameras_rotation,
                "test_feature_point_positions",
            )

            # create feature points test data.
            id_candidates = list(range(100))
            random.shuffle(id_candidates)
            feature_point_directions = []
            for bundles in data_manager.get_keyframes_bundle(0.0):
                bundles = [
                    [id_candidates[i], bundle[1]] for i, bundle in enumerate(bundles)
                ]
                feature_point_directions.append(bundles)

            featurePointPositions = FeaturePointPositions()

            # create keyframes as test data.
            for i, directions in enumerate(feature_point_directions):
                featurePointPositions.add_keyframe(
                    data_manager.cameras_true_position[i],
                    data_manager.cameras_true_rotation[i],
                    directions,
                )

            # evaluate results.
            feature_point_position_threshold = 0.1
            for i, feature_point_ture_position in enumerate(
                data_manager.feature_points_true_position
            ):
                estimated_position = FeaturePointsPositionDB().find(id_candidates[i])[
                    1:
                ]
                evaluate_value = np.linalg.norm(
                    estimated_position - feature_point_ture_position
                )
                self.assertTrue(evaluate_value < feature_point_position_threshold)

            print("finish test_feature_point_positions")


if __name__ == "__main__":
    unittest.main()
