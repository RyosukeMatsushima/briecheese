import unittest
import cv2 as cv
from unittest.mock import patch
from modules.feature_point_id.feature_point_id import FeaturePointId
from database.descriptors_db import DescriptorsDB
from database.db_protocol import DBProtocol


class FeaturePointId_get_with_pixel(unittest.TestCase):
    db_table = "test_descriptors"

    def setUp(self):
        DBProtocol(
            self.db_table,
            "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))",
        ).delete_all()

    def tearDownAfterClass(self):
        DBProtocol(
            self.db_table,
            "(id INT AUTO_INCREMENT, descriptor JSON, PRIMARY KEY (id))",
        ).delete_all()

    def test_new_feature_point_id(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": self.db_table}):
            frame = cv.imread("tests/feature_point_id/sample1.jpg")
            featurePointIdclass = FeaturePointId()
            db = DescriptorsDB()
            response = featurePointIdclass.get_with_pixel(frame)
            expected = len(db.get_all())
            self.assertEqual(expected, len(response))

    def test_known_feature_point_id(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": self.db_table}):
            frame = cv.imread("tests/feature_point_id/sample1.jpg")
            featurePointIdclass = FeaturePointId()
            db = DescriptorsDB()
            _ = featurePointIdclass.get_with_pixel(frame)
            expected_db = db.get_all()
            response = featurePointIdclass.get_with_pixel(frame)
            self.assertEqual(expected_db, db.get_all())
            self.assertEqual(len(expected_db), len(response))

    def test_unmatch_feature_point_id(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": self.db_table}):
            frame1 = cv.imread("tests/feature_point_id/sample1.jpg")
            frame2 = cv.imread("tests/feature_point_id/sample2.jpg")
            featurePointIdclass = FeaturePointId()
            db = DescriptorsDB()
            first_response = featurePointIdclass.get_with_pixel(frame1)
            second_response = featurePointIdclass.get_with_pixel(frame2)
            expected = len(db.get_all())
            self.assertEqual(expected, (len(first_response) + len(second_response)))

    def test_shift_pixel(self):
        with patch.dict("os.environ", {"DESCRIPTORS_DB_TABLE": self.db_table}):
            frame = cv.imread("tests/feature_point_id/sample1.jpg")
            shift_frame = cv.imread("tests/feature_point_id/sample1_shift30.jpg")
            featurePointIdclass = FeaturePointId()
            response = featurePointIdclass.get_with_pixel(frame)
            shift_response = featurePointIdclass.get_with_pixel(shift_frame)
            shift_id = shift_response[0][1]
            expected = [
                base + shift
                for (base, shift) in zip(list(response[shift_id -1][0]), [30, 30])
            ]
            self.assertEqual(expected, list(shift_response[0][0]))


if __name__ == "__main__":
    unittest.main()
