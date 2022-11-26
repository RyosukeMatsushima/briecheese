import numpy as np
from scipy.spatial.transform import Rotation as scipy_R


def get_random():
    return np.random.rand(1)[0]

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
