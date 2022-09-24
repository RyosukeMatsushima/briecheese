#!/usr/bin/env python

from __future__ import print_function
import sys
import numpy as np
from scipy.spatial.transform import Rotation as R
import cv2 as cv
from collections import namedtuple
from database.descriptors_db import DescriptorsDB


class FeaturePointId:
    def __init__(self):
        flann_params = dict(
            algorithm=6, table_number=6, key_size=12, multi_probe_level=1
        )
        self.detector = cv.ORB_create(nfeatures=1000)
        self.matcher = cv.FlannBasedMatcher(flann_params, {})
        self.db = DescriptorsDB()
        db_descriptors = self.db.get_all()
        descriptors = []
        for db_descriptor in db_descriptors:
            descriptors.append(db_descriptor[1])
        self.matcher.add(descriptors)

    def get_with_pixel(self, frame):
        keypoints, descriptors = self.detectAndCompute(frame)
        matches = self.matcher.knnMatch(descriptors, k=2)
        response = []
        unmatch_descriptors = []
        for keypoint, descriptor in keypoints, descriptors:
            unmatch_descriptors.append([keypoint, descriptor])

        for m in matches:
            if m.distance < 1:
                feature_point_id_column = self.db.find_by_descriptor(
                    descriptors[m.trainIdx]
                )
                unmatch_descriptors.pop(m.trainIdx)
                response.append(
                    [[keypoints[m.trainIdx].pt], feature_point_id_column[0]]
                )
        for unmatch_descriptor in unmatch_descriptors:
            feature_point_id = self.db.create(unmatch_descriptor[1])
            response.append([[unmatch_descriptor[0].pt], feature_point_id])

        return response

    def detectAndCompute(self, frame):
        keypoints, descriptors = self.detector.detectAndCompute(frame, None)
        if not descriptors:
            descriptors = []
        return keypoints, descriptors