import unittest
import numpy as np
from scipy.spatial.transform import Rotation as scipy_R
from tests.pose_optimizer.tools import (
    setup,
    logging_data,
)
from tests.tools.generate_data import (
    get_random_points,
    get_random_rotation,
)


class OptimizerTest(unittest.TestCase):
    def tearDown(self):
        print("finish OptimizerTest")

    def check_result(
        self,
        optimizer,
        data_manager,
        feature_point_threshold,
        keyframe_position_threshold,
        keyframe_rotation_threshold,
    ):

        for i, keyframe in enumerate(optimizer.keyframes):

            # check keyframe position error
            evaluate_value = np.linalg.norm(
                data_manager.cameras_true_position[i] - keyframe.position
            )
            self.assertTrue(evaluate_value < keyframe_position_threshold)

            # check keyframe rotation error
            rotation_error = data_manager.cameras_true_rotation[i] @ np.linalg.inv(
                keyframe.rotation
            )
            evaluate_value = scipy_R.from_matrix(rotation_error).as_euler(
                "zxy", degrees=True
            )
            for val in evaluate_value:
                self.assertTrue(val < keyframe_rotation_threshold)

        # check feature points position
        for i, fp in enumerate(optimizer.feature_points_position):
            evaluate_value = np.linalg.norm(
                data_manager.feature_points_true_position[i] - fp
            )
            self.assertTrue(evaluate_value < feature_point_threshold)

    def test_optimize_with_full_keyframe_position(self):
        print("start test_optimize_with_full_keyframe_position")
        feature_points_position = get_random_points(3, 4, 2, 10)
        cameras_position = get_random_points(2, 2, 0, 3)
        cameras_rotation = get_random_rotation(0, 1, 3)

        optimizer, data_manager = setup(
            feature_points_position,
            cameras_position,
            cameras_rotation,
            1,
            1,
            1,
            0,
            "with_full_keyframe_position",
        )

        optimizer.position_bundle_constant = 0.9
        optimizer.rotation_bundle_constant = 0.9
        optimizer.position_constant = 0.05
        optimizer.rotation_constant = 0.05

        logging_data(optimizer, data_manager)

        def optimizer_callback(trial, evaluate_value):
            logging_data(optimizer, data_manager)

        optimizer.optimize(2000, callback=optimizer_callback)
        data_manager.finish()

        self.check_result(optimizer, data_manager, 0.1, 0.1, 0.1)
        print("finish test_optimize_with_full_keyframe_position")

    def test_optimize_only_keyframe_position(self):
        print("start test_optimize_only_keyframe_position")

        feature_points_position = get_random_points(10, 2, 0, 10)
        cameras_position = get_random_points(2, 2, 0, 3)
        cameras_rotation = get_random_rotation(0, 1, 3)

        optimizer, data_manager = setup(
            feature_points_position,
            cameras_position,
            cameras_rotation,
            0,
            0.1,
            0.1,
            0,
            "only_keyframe_position",
        )

        optimizer.position_bundle_constant = 0.9
        optimizer.rotation_bundle_constant = 0.9
        optimizer.position_constant = 0.5
        optimizer.rotation_constant = 0.5

        def optimizer_callback(trial, evaluate_value):
            logging_data(optimizer, data_manager)

        no_keyframe_bundle_num = [0, 1, 2]
        for i, keyframe in enumerate(optimizer.keyframes):
            if i in no_keyframe_bundle_num:
                keyframe.position_bundle = np.array([])
                keyframe.rotation_bundle = np.array([])

        logging_data(optimizer, data_manager)
        optimizer.optimize(2000, optimize_feature_point=False, callback=None)
        data_manager.finish()

        self.check_result(optimizer, data_manager, 0.1, 0.1, 0.1)
        print("finish test_optimize_only_keyframe_position")


if __name__ == "__main__":
    unittest.main()
