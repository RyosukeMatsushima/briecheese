

class DataStore:

    def __init__(self):
        self.featurePointsStore = FeaturePointsStore()
        self.keyframesStore = KeyframesStore()

        # {feature_point_id: [keyframe_id, direction]}
        self.pending_bundles = {}
        # {feature_point_id: [[keyframe_id, direction], ..]}
        self.cueing_bundles = {}

        self.minimum_related_feature_points_count = 8

    def add_new_keyframe(self,
                         keyframe_id,
                         observed_position,
                         observed_rotation,
                         bundles):

        # add bundle to new keyframe bundle if the feature point is already exists.
        new_keyframe_bundles = []
        for i, bundle in enumerate(bunldes):
            feature_point_id = bundle[0]
            direction = bundle[1]

            if feature_point_id in self.featurePointsStore.ids:
                bundles.pop(i)
                feature_piint_index = self.featurePointsStore.ids.index(feature_point_id)
                new_keyframe_bundles += [feature_piint_index, direction]

        # check keyframe is computable
        if len(new_keyframe_bundles) < self.minimum_related_feature_points_count:
            return False

        self.keyframesStore.add(keyframe_id,
                                new_keyframe_bundles,
                                observed_position,
                                observed_rotation)

        # add bundle to cue if the feature point is observed two from keyframes (which means the feature point position is computable).
        for i, bundle in enumerate(bunldes):
            feature_point_id = bundle[0]
            direction = bundle[1]

            if feature_point_id in self.pending_bundles:
                bundles.pop(i)
                keyframe_id, direction = self.pending_bundles.pop(feature_point_id)

                if not feature_point_id in self.cueing_bundles:
                    self.cueing_bundles.update{keyframe_id: []}
                self.cueing_bundles[feature_point_id] += [[keyframe_id, direction]]

        # add bundle to pending_bundles.
        for i, bundle in enumerate(bunldes):
            feature_point_id = bundle[0]
            direction = bundle[1]

            self.pending_bundles.update({feature_point_id: [keyframe_id, direction]})

        return True

