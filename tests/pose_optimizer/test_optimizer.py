import unittest
import numpy as np
from scipy.spatial.transform import Rotation as scipy_R
import matplotlib.pyplot as plt

import pathlib
import os

from modules.pose_optimizer.optimizer import *
from tests.tools.state_logger import StateLogger

current_dir = pathlib.Path(__file__).resolve().parent
log_dir = str(current_dir) + '/log/'
os.makedirs(log_dir, exist_ok=True)


def get_random():
    return np.random.rand(1)[0]

def translate_points(points, t, R):
    return [ np.linalg.inv(R) @ (point - t) for point in points ]


class OptimizerTest(unittest.TestCase):

    def setUp(self):
        xy_scale = 3
        z_scale = 3
        z_offset = 4
        self.fp_3d = [ np.array([(get_random() - 0.5) * xy_scale,
                                 (get_random() - 0.5) * xy_scale,
                                 get_random() * z_scale + z_offset])
                           for i in range(5) ]

        cameras_position = [ [0.0, 0.0, 0.0],
                             [0.5, 0.0, 0.0],
                             [1.0, 0.0, 0.0] ]

        cameras_rotation = [ [0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0] ]


        self.cameras_t_mat = [ np.array(position) for position in cameras_position ]
        self.cameras_R_mat = [ scipy_R.from_euler('xyz', rotation).as_matrix() for rotation in cameras_rotation ]

        self.related_fp_3d = [ translate_points(self.fp_3d, t, R) for t, R in zip(self.cameras_t_mat, self.cameras_R_mat) ]



    def tearDown(self):
        print("finish Points2Dto3DTest")

    def test_optimize(self):

        def optimizer_callback(trial, evaluate_value):
            data = []
            for fp_pos in optimizer.feature_points_position:
                data += fp_pos.tolist()
            fp_position_trajectory_log.add_data(data)

            print('trial times: {}'.format(trial))
            print('evaluate_value: {}'.format(evaluate_value))

        # setup logger
        labels = []
        for i, fp in enumerate(self.fp_3d):
            labels += ['fp_' + str(i) + axis for axis in 'XYZ']

        fp_position_trajectory_log = StateLogger(log_dir + 'fp_position_trajectory.csv',
                                      tuple(labels))
        fp_position_log = StateLogger(log_dir + 'fp_true_position.csv',
                                      tuple(labels))
        data = []
        for fp in self.fp_3d:
            data += fp.tolist()
        fp_position_log.add_data(data)
        fp_position_log.finish()

        # setup optimizer
        optimizer = Optimizer()

        for point in self.fp_3d:
            noise = np.random.normal(0, 2, 3)
            optimizer.add_feature_point(point + noise)

        for fp, t, R in zip(self.related_fp_3d, self.cameras_t_mat, self.cameras_R_mat):
            feature_points_bundle = [ [ i, point / np.linalg.norm(point) ] for i, point in enumerate(fp) ]

            position_noise = np.random.normal(0, 2, 3)
            rotation_noise = scipy_R.from_euler('xyz', np.random.normal(0, 2, 3)).as_matrix()
            keyframe = Keyframe(t + position_noise, rotation_noise @ R, t, R, feature_points_bundle)

            optimizer.add_keyframe(keyframe)

        # run optimizer
        optimizer.optimize(3000, optimizer_callback)

        fp_position_trajectory_log.finish()

        for i, keyframe in enumerate(optimizer.keyframes):

            # check keyframe position error
            evaluate_value = np.linalg.norm(self.cameras_t_mat[i] - keyframe.position)
            self.assertTrue(evaluate_value < 0.01)

            # check keyframe rotation error
            rotation_error = self.cameras_R_mat[i] @ np.linalg.inv(keyframe.rotation)
            evaluate_value = scipy_R.from_matrix(rotation_error).as_euler('zxy', degrees=True)
            for val in evaluate_value:
                self.assertTrue(val < 0.1)

        # check feature points position
        for i, fp in enumerate(optimizer.feature_points_position):
            evaluate_value = np.linalg.norm(self.fp_3d[i] - fp)
            self.assertTrue(evaluate_value < 0.01)



if __name__ == "__main__":
    unittest.main()
