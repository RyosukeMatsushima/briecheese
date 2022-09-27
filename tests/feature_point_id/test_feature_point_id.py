import unittest
import cv2 as cv
from unittest.mock import patch
from modules.feature_point_id.feature_point_id import FeaturePointId
from database.descriptors_db import DescriptorsDB
from database.db_protocol import DBProtocol


class FeaturePointId_get_with_pixel(unittest.TestCase):
    def setUp(self):
        DBProtocol("test_descriptors", "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))").delete_all()
        
    def tearDown(self):
        DBProtocol("test_descriptors", "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))").delete_all()

    def test_new_feature_point_id(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": "test_descriptors"}):
            frame = cv.imread("tests/feature_point_id/sample.jpg")
            featurePointIdclass = FeaturePointId()
            db = DescriptorsDB()
            response = featurePointIdclass.get_with_pixel(frame)
            expected = len(db.get_all())
            self.assertEqual(expected, len(response))
    
    def test_known_feature_point_id(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": "test_descriptors"}):
            frame = cv.imread("tests/feature_point_id/sample.jpg")
            featurePointIdclass = FeaturePointId()
            db = DescriptorsDB()
            response = featurePointIdclass.get_with_pixel(frame)
            expected = len(db.get_all())
            self.assertEqual(expected, len(response))
            response = featurePointIdclass.get_with_pixel(frame)
            expected = len(db.get_all())
            self.assertEqual(expected, len(response))


if __name__ == "__main__":
    unittest.main()
