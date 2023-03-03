#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import cv2 as cv
import json

from modules.feature_point_id.descriptor_with_id import DescriptorWithID
from database.descriptors_db import DescriptorsDB


class FeaturePointId:
    def __init__(self):
        flann_params = dict(
            algorithm=6, table_number=6, key_size=12, multi_probe_level=1
        )
        self.detector = cv.ORB_create(nfeatures=1000)
        self.matcher = cv.FlannBasedMatcher(flann_params, {})
        self.matcher_wit_latest = None
        self.db = DescriptorsDB()
        self.descriptorWithID = DescriptorWithID()
        self.unmatched_descriptors_in_previous_frame = np.array([])

        db_descriptors = self.db.get_all()
        descriptors = []
        for db_descriptor in db_descriptors:
            list_db_descriptor = json.loads(db_descriptor[1])
            feature_point_id = db_descriptor[0]
            self.descriptorWithID.add_descriptor(list_db_descriptor, feature_point_id)

    def get_with_pixel(self, frame, in_create_map):
        keypoints, descriptors = self.detectAndCompute(frame)

        response_with_known_feature_points, unmatched_keypoints, unmatched_descriptors = self.match_with_known_feature_points(keypoints, descriptors)

        response_with_previous_frame = []
        if in_create_map:
            response_with_previous_frame = self.match_with_previous_frame(unmatched_keypoints, unmatched_descriptors)

        return response_with_known_feature_points + response_with_previous_frame

    def match_with_known_feature_points(self, keypoints, descriptors):
        known_descriptors = self.descriptorWithID.get_descriptors()

        if len(known_descriptors) == 0:
            print("no known descriptors")
            return [], keypoints, descriptors

        matches = self.matcher.knnMatch(descriptors, known_descriptors, k=2)
        matches = [
            m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * 0.5
        ]

        response = []
        match_query_indexes = []

        for m in matches:
            feature_point_id = self.descriptorWithID.get_id(m.trainIdx)
            response.append([keypoints[m.queryIdx].pt, feature_point_id])
            match_query_indexes.append(m.queryIdx)

        unmatched_keypoints = np.delete(keypoints, match_query_indexes, 0)
        unmatched_descriptors = np.delete(descriptors, match_query_indexes, 0)
        
        return response, unmatched_keypoints, unmatched_descriptors

    def match_with_previous_frame(self, unregistered_keypoints, unregistered_descriptors):

        if len(self.unmatched_descriptors_in_previous_frame) == 0:
            self.unmatched_descriptors_in_previous_frame = unregistered_descriptors
            return []

        matches = self.matcher.knnMatch(unregistered_descriptors, self.unmatched_descriptors_in_previous_frame, k=2)
        matches = [
            m[0] for m in matches if len(m) == 2 and m[0].distance < m[1].distance * 0.5
        ]

        response = []
        match_query_indexes = []
        for m in matches:
            matched_descriptor = self.unmatched_descriptors_in_previous_frame[m.trainIdx]
            feature_point_id = self.add_feature_point_to_db(matched_descriptor)

            response.append([unregistered_keypoints[m.queryIdx].pt, feature_point_id])
            match_query_indexes.append(m.queryIdx)

            self.descriptorWithID.add_descriptor(self.unmatched_descriptors_in_previous_frame[m.trainIdx], feature_point_id)

        self.unmatched_descriptors_in_previous_frame = np.delete(unregistered_descriptors, match_query_indexes, 0)

        return response

    def add_feature_point_to_db(self, descriptor):
        feature_point_id = self.db.create(descriptor.tolist())[0]
        return feature_point_id

    def detectAndCompute(self, frame):
        keypoints, descriptors = self.detector.detectAndCompute(frame, None)
        if descriptors is None:
            descriptors = []
        return keypoints, descriptors
