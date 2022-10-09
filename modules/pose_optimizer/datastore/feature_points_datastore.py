
'''
FeatruePointsStore manages ids and array order.
Optimizer care only array order of position data not ids.
'''

class FeaturePointsStore:

    def __init__(self):
        self.ids = []
        self.positions = []

    def get_position(self, feature_point_id):
        return self.positions[self.ids.index(feature_point_id)]
