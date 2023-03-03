#!/usr/bin/env python

import numpy as np

class DescriptorWithID:

    def __init__(self):
        self.descriptors = []
        self.ids = []

    def add_descriptor(self, descriptor, feature_point_id):
        #TODO: check descriptor size.
        self.descriptors.append(descriptor)
        self.ids.append(feature_point_id)

    def get_descriptors(self):
        return np.array(self.descriptors, dtype='u1')

    def get_id(self, index):
        return self.ids[index]
