import unittest
import json
from random import randint
from unittest.mock import patch
from database.keyframe_feature_point_db import KeyframeFeaturePointDB
from database.keyframe_db import KeyframeDB
from database.feature_point_db import FeaturePointDB
from database.db_protocol import DBProtocol


class KeyframeFeaturePointDBTest(unittest.TestCase):
    db_table = "test_keyframe_feature_point"
    db_table_keyframe = "test_keyframe"
    db_table_feature_point = "test_feature_point"

    def setUp(self):
        DBProtocol(
            self.db_table,
            "(keyframe_id INT, feature_point_id INT, direction JSON)",
        ).delete_all()
        DBProtocol(
            self.db_table_keyframe,
            "(id INT AUTO_INCREMENT, position JSON, rotation JSON, observed_position JSON, observed_rotation JSON, PRIMARY KEY (id))",
        ).delete_all()
        DBProtocol(
            self.db_table_feature_point,
            "(id INT AUTO_INCREMENT, position JSON, PRIMARY KEY (id))",
        ).delete_all()

    def tearDownAfterClass(self):
        DBProtocol(
            self.db_table,
            "(keyframe_id INT, feature_point_id INT, direction JSON)",
        ).delete_all()
        DBProtocol(
            self.db_table_keyframe,
            "(id INT AUTO_INCREMENT, position JSON, rotation JSON, observed_position JSON, observed_rotation JSON, PRIMARY KEY (id))",
        ).delete_all()
        DBProtocol(
            self.db_table_feature_point,
            "(id INT AUTO_INCREMENT, position JSON, PRIMARY KEY (id))",
        ).delete_all()

    def test_create_and_get_all(self):
        with patch.dict(
            "os.environ",
            {
                "KEYFRAME_FEATURE_POINT_DB_TABLE": self.db_table,
                "KEYFRAME_DB_TABLE": self.db_table_keyframe,
                "FEATURE_POINT_DB_TABLE": self.db_table_feature_point,
            },
        ):
            keyframe_db = KeyframeDB()
            keyframe_params = [
                1,
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
            ]
            keyframe_db.create(
                keyframe_params[1],
                keyframe_params[2],
                keyframe_params[3],
                keyframe_params[4],
            )
            feature_point_db = FeaturePointDB()
            feature_point_params = [1, [randint(0, 10), randint(0, 10), randint(0, 10)]]
            feature_point_db.create(feature_point_params[1])

            db = KeyframeFeaturePointDB()
            direction = [randint(0, 10), randint(0, 10), randint(0, 10)]
            db.create(keyframe_params[0], feature_point_params[0], direction)
            expected = [
                [
                    (
                        keyframe_params[0],
                        json.dumps(keyframe_params[1]),
                        json.dumps(keyframe_params[2]),
                        json.dumps(keyframe_params[3]),
                        json.dumps(keyframe_params[4]),
                    ),
                    (feature_point_params[0], json.dumps(feature_point_params[1])),
                    json.dumps(direction),
                ]
            ]
            self.assertEqual(expected, db.get_all())
