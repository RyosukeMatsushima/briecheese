

class DataStore:

    def __init__(self):
        self.featurePointsStore = FeaturePointsStore()
        self.keyframesStore = KeyframesStore()

        # {feature_point_id: [keyframe_id, direction], ...}
        # pending bundles while the feature point is observed only one keyframe.
        # feature point needs to be observed atleast 2 keyframes.
        self.pending_bundles = {}

        # {feature_point_id: [[keyframe_id, direction], ...], ...}
        # keyframe pose will be estimated with pose obtained feature points.
        # add cueing_bundles after keyframe pose estimated and optimize again with the new feature points.
        self.cueing_bundles = {}

        self.MINIMUM_RELATED_FEATURE_POINTS_COUNT = 8

    def add_keyframe(self,
                     keyframe_id,
                     observed_position,
                     observed_rotation,
                     bundles):

        # add bundle to new keyframe bundle if the feature point is already exists.
        known_bundles_in_keyframe = []
        for i, bundle in enumerate(bunldes):
            feature_point_id = bundle[0]
            direction = bundle[1]

            if feature_point_id in self.featurePointsStore.ids:
                bundles.pop(i)
                feature_piint_index = self.featurePointsStore.ids.index(feature_point_id)
                known_bundles_in_keyframe += [feature_piint_index, direction]

        # check keyframe is computable
        if len(known_bundles_in_keyframe) < self.MINIMUM_RELATED_FEATURE_POINTS_COUNT:
            return False

        self.keyframesStore.add(keyframe_id,
                                known_bundles_in_keyframe,
                                observed_position,
                                observed_rotation)
        self.add_bundles(keyframe_id, bundles)
        return True

    def add_bundles(self, keyframe_id, bundles):

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

            else:
                self.pending_bundles.update({feature_point_id: [keyframe_id, direction]})

