import unittest
import numpy as np
from scipy.spatial.transform import Rotation as scipy_R

from tests.pose_optimizer.tools import *

class OptimizerTest(unittest.TestCase):

    def tearDown(self):
        print("finish Points2Dto3DTest")


    def check_result(self,
                     optimizer,
                     data_manager,
                     feature_point_threshold,
                     keyframe_position_threshold,
                     keyframe_rotation_threshold):

        for i, keyframe in enumerate(optimizer.keyframes):

            # check keyframe position error
            evaluate_value = np.linalg.norm(data_manager.cameras_true_position[i] - keyframe.position)
            self.assertTrue(evaluate_value < keyframe_position_threshold)

            # check keyframe rotation error
            rotation_error = data_manager.cameras_true_rotation[i] @ np.linalg.inv(keyframe.rotation)
            evaluate_value = scipy_R.from_matrix(rotation_error).as_euler('zxy', degrees=True)
            for val in evaluate_value:
                self.assertTrue(val < keyframe_rotation_threshold)

        # check feature points position
        for i, fp in enumerate(optimizer.feature_points_position):
            evaluate_value = np.linalg.norm(data_manager.feature_points_true_position[i] - fp)
            self.assertTrue(evaluate_value < feature_point_threshold)

    def test_optimize_with_full_keyframe_position(self):
        feature_points_position, cameras_position, cameras_rotation = get_dataset()

        optimizer, data_manager = setup(feature_points_position,
                                        cameras_position,
                                        cameras_rotation,
                                        1, 1, 1, 0,
                                        'with_full_keyframe_position')

        logging_data(optimizer, data_manager)

        def optimizer_callback(trial, evaluate_value):
            logging_data(optimizer, data_manager)
            print('trial times: {}'.format(trial))
            print('evaluate_value: {}'.format(evaluate_value))


        optimizer.optimize(10000, optimizer_callback)
        data_manager.finish()

        self.check_result(optimizer, data_manager, 0.01, 0.01, 0.1)


if __name__ == "__main__":
    unittest.main()
