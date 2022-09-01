import unittest
import numpy as np
from scipy.spatial.transform import Rotation as scipy_R
import matplotlib.pyplot as plt

from modules.pose_optimizer.optimizer import *



def get_random():
    return np.random.rand(1)[0]

def translate_points(points, t, R):
    return [ R @ point + t for point in points ]


class OptimizerTest(unittest.TestCase):

    def setUp(self):
        xy_scale = 3
        z_scale = 3
        z_offset = 4
        self.fp_3d = [ np.array([(get_random() - 0.5) * xy_scale,
                                 (get_random() - 0.5) * xy_scale,
                                 get_random() * z_scale + z_offset])
                           for i in range(10) ]

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

        optimizer = Optimizer()

        for point in self.fp_3d:
            optimizer.add_feature_point(point)

        for fp, t, R in zip(self.related_fp_3d, self.cameras_t_mat, self.cameras_R_mat):
            feature_points_bundle = [ [ i, point / np.linalg.norm(point) ] for i, point in enumerate(fp) ]

            keyframe = Keyframe(t, R, t, R, feature_points_bundle)

            optimizer.add_keyframe(keyframe)

        optimizer.optimize()

if __name__ == "__main__":
    unittest.main()
