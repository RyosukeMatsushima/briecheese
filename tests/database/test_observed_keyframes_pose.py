import unittest
from database.observed_keyframes_pose_db import ObservedKeyframesPoseDB

class ObservedKeyframesPoseDBTest(unittest.TestCase):

    def test_create_and_find(self):
        db = ObservedKeyframesPoseDB()
        db.delete_all()

        data = { 'ID': 12,
                 'x': 1.2, 'y': 32.3, 'z': 8.4,
                 'rot_x': 3.2, 'rot_y': 293.2, 'rot_z': 0.325 }

        db.create(data['ID'],
                  data['x'], data['y'], data['z'],
                  data['rot_x'], data['rot_y'], data['rot_z'])
        return_data = db.find(data['ID'])
        ans = (data['ID'],
               data['x'], data['y'], data['z'],
               data['rot_x'], data['rot_y'], data['rot_z'])
        self.assertEqual(return_data,
                         ans,
                         'input and output is not samed')
