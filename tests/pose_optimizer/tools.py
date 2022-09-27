import numpy as np
from scipy.spatial.transform import Rotation as scipy_R

from modules.pose_optimizer.optimizer import Optimizer, Keyframe
from tests.pose_optimizer.data_manager import DataManager


def get_random():
    return np.random.rand(1)[0]


def setup(
    feature_points_position,
    cameras_position,
    cameras_rotation,
    feature_points_noise_scale,
    keyframe_position_noise_scale,
    keyframe_rotation_noise_scale,
    keyframe_bundle_noise_scale,
    log_file_name,
):

    data_manager = DataManager(
        feature_points_position, cameras_position, cameras_rotation, log_file_name
    )

    noised_feature_points_position = data_manager.get_noised_feature_points_position(
        feature_points_noise_scale
    )
    noised_cameras_position = data_manager.get_noised_keyframe_position(
        keyframe_position_noise_scale
    )
    noised_cameras_rotation = data_manager.get_noised_keyframe_rotaion(
        keyframe_rotation_noise_scale
    )
    keyframes_bundle = data_manager.get_keyframes_bundle(keyframe_bundle_noise_scale)

    optimizer = Optimizer()
    for point in noised_feature_points_position:
        optimizer.add_feature_point(point)

    for i, bundle in enumerate(keyframes_bundle):

        keyframe = Keyframe(
            noised_cameras_position[i],
            noised_cameras_rotation[i],
            data_manager.cameras_true_position[i],
            data_manager.cameras_true_rotation[i],
            bundle,
        )

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


def get_random_points(xy_scale, z_scale, z_offset, num):
    points = [
        np.array(
            [
                (get_random() - 0.5) * xy_scale,
                (get_random() - 0.5) * xy_scale,
                get_random() * z_scale + z_offset,
            ]
        )
        for i in range(num)
    ]
    return points


def get_random_rotation(offset, scale, num):
    random_vector = [np.random.normal(offset, scale, 3) for p in range(num)]
    return [scipy_R.from_euler("xyz", v).as_matrix() for v in random_vector]


def get_square_position(x, y, z):
    points = [[x, y, z], [x, -y, z], [-x, y, z], [-x, -y, z]]
    return [np.array(p) for p in points]


def get_position(points):
    return [np.array(p) for p in points]


def get_rotation(vectors):
    return [scipy_R.from_euler("xyz", v).as_matrix() for v in vectors]
