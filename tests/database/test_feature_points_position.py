import unittest
from database.feature_points_position_db import FeaturePointsPositionDB

class FeaturePointsPositionDBTest(unittest.TestCase):

    def test_create_and_find(self):
        db = FeaturePointsPositionDB()

        data = { 'ID': 12, 'x': 1.2, 'y': 32.3, 'z': 8.4 }

        db.create(data['ID'], data['x'], data['y'], data['z'])
        return_data = db.find(data['ID'])
        ans = (data['ID'], data['x'], data['y'], data['z'])
        self.assertEqual(return_data,
                         ans,
                         'input and output is not samed')

