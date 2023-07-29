from modules.pose_optimizer.optimizer import Optimizer, Keyframe
from tests.tools.data_manager import DataManager


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
