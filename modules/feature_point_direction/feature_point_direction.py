#!/usr/bin/env python

import numpy as np


class FeaturePointDirection:
    def get(self, fx, fy, cx, cy, pixel_x, pixel_y):
        x = (pixel_x - cx) / fx
        y = (pixel_y - cy) / fy
        z = 1
        direction = np.array([x, y, z])
        direction_size = np.linalg.norm(direction)
        return (direction / direction_size).tolist()
