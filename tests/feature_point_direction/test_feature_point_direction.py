import unittest
from modules.feature_point_direction.feature_point_direction import (
    FeaturePointDirection,
)


class FeaturePointDirection_get(unittest.TestCase):
    fx = fy = 1
    cx = 500
    cy = 200

    def test_origin(self):
        pixel_x = self.cx
        pixel_y = self.cy
        response = FeaturePointDirection().get(
            self.fx, self.fy, self.cx, self.cy, pixel_x, pixel_y
        )
        expected = [0, 0, 1]
        self.assertEqual(expected, response)

    def test_corner(self):
        pixel_x = 0
        pixel_y = 0
        upper_left_response = FeaturePointDirection().get(
            self.fx, self.fy, self.cx, self.cy, pixel_x, pixel_y
        )
        pixel_x = 2 * self.cx
        pixel_y = 2 * self.cy
        lower_right_response = FeaturePointDirection().get(
            self.fx, self.fy, self.cx, self.cy, pixel_x, pixel_y
        )
        expected = [
            -1 * upper_left_response[0],
            -1 * upper_left_response[1],
            upper_left_response[2],
        ]
        self.assertEqual(expected, lower_right_response)
