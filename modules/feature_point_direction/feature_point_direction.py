#!/usr/bin/env python

import numpy as np


class FeaturePointDirection:
    def __init__(self, fx, fy, cx, cy):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy

    def get(self, pixel_x, pixel_y):
        x = (pixel_x - self.cx) / self.fx
        y = (pixel_y - self.cy) / self.fy
        z = 1
        direction = np.array([x, y, z])
        direction_size = np.linalg.norm(direction)
        return (direction / direction_size).tolist()
