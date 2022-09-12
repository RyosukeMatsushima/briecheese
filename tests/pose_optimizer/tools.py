
import numpy as np
from scipy.spatial.transform import Rotation as scipy_R

from modules.pose_optimizer.optimizer import *
from tests.pose_optimizer.data_manager import DataManager

def get_random():
    return np.random.rand(1)[0]

def setup(feature_points_position,
          cameras_position,
          cameras_rotation,
          feature_points_noise_scale,
          keyframe_position_noise_scale,
          keyframe_rotation_noise_scale,
          keyframe_bundle_noise_scale,
          log_file_name):

    data_manager = DataManager(feature_points_position, cameras_position, cameras_rotation, log_file_name)

    noised_feature_points_position = data_manager.get_noised_feature_points_position(feature_points_noise_scale)
    noised_cameras_position = data_manager.get_noised_keyframe_position(keyframe_position_noise_scale)
    noised_cameras_rotation = data_manager.get_noised_keyframe_rotaion(keyframe_rotation_noise_scale)
    keyframes_bundle = data_manager.get_keyframes_bundle(keyframe_bundle_noise_scale)

    optimizer = Optimizer()
    for point in noised_feature_points_position:
        optimizer.add_feature_point(point)

    for i, bundle in enumerate(keyframes_bundle):

        keyframe = Keyframe(noised_cameras_position[i],
                            noised_cameras_rotation[i],
                            data_manager.cameras_true_position[i],
                            data_manager.cameras_true_rotation[i],
                            bundle)

        optimizer.add_keyframe(keyframe)

    return optimizer, data_manager

def logging_data(optimizer, data_manager): 
    fp_data = []
    for fp_pos in optimizer.feature_points_position:
        fp_data += fp_pos.tolist()

    kf_data = []
    for kf in optimizer.keyframes:
        kf_data += kf.position.tolist()

    data_manager.logging_trajectory(fp_data, kf_data)

def get_dataset():
    xy_scale = 3
    z_scale = 3
    z_offset = 4

    feature_points_position = [ np.array([(get_random() - 0.5) * xy_scale,
                                 (get_random() - 0.5) * xy_scale,
                                 get_random() * z_scale + z_offset])
                        for i in range(37) ]

    position = [ [0.0, 0.0, 0.0],
                 [0.5, 0.0, 0.0],
                 [1.0, 0.0, 0.0] ]

    cameras_position = [ np.array(p) for p in position ]

    rotation = [ [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0] ]

    cameras_rotation = [ scipy_R.from_euler('xyz', r).as_matrix() for r in rotation ]

    return feature_points_position, cameras_position, cameras_rotation

