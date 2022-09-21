import unittest
from database.bundles_db import BundlesDB

class BundlesTest(unittest.TestCase):

    def test_create_and_find(self):
        db = BundlesDB()
        db.delete_all()

        data = { 'fp_id': 12,
                 'kf_id': 12,
                 'x': 1.2, 'y': 32.3, 'z': 8.4 }

        db.create(data['fp_id'],
                  data['kf_id'], 
                  data['x'], data['y'], data['z'] )

        return_data = db.find_by_feature_point_id(data['fp_id'])
        ans = (data['fp_id'],
               data['kf_id'], 
               data['x'], data['y'], data['z'] )

        self.assertEqual(return_data[0],
                         ans,
                         'input and output is not samed')
