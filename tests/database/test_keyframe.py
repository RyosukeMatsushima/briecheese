import unittest
import json
from random import randint
from unittest.mock import patch
from database.keyframe_db import KeyframeDB
from database.db_protocol import DBProtocol


class KeyframeDBTest(unittest.TestCase):
    db_table = "test_keyframe"

    def setUp(self):
        DBProtocol(
            self.db_table,
            "(id INT, position JSON, rotation JSON, observed_position JSON, observed_rotation JSON)",
        ).delete_all()

    def tearDownAfterClass(self):
        DBProtocol(
            self.db_table,
            "(id INT, position JSON, rotation JSON, observed_position JSON, observed_rotation JSON)",
        ).delete_all()

    def test_create_and_find(self):
        with patch.dict("os.environ", {"KEYFRAME_DB_TABLE": self.db_table}):
            db = KeyframeDB()
            params = [
                1,
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
                [randint(0, 10), randint(0, 10), randint(0, 10)],
            ]
            db.create(
                params[0],
                params[1],
                params[2],
                params[3],
                params[4],
            )
            expected = (
                params[0],
                json.dumps(params[1]),
                json.dumps(params[2]),
                json.dumps(params[3]),
                json.dumps(params[4]),
            )

            self.assertEqual(expected, db.find(params[0]))
