import unittest
import json
from random import randint
from unittest.mock import patch
from database.feature_point_db import FeaturePointDB
from database.db_protocol import DBProtocol


class FeaturePointDBTest(unittest.TestCase):
    db_table = "test_feature_point"

    def setUp(self):
        DBProtocol(
            self.db_table,
            "(id INT, position JSON)",
        ).delete_all()

    def tearDownAfterClass(self):
        DBProtocol(
            self.db_table,
            "(id INT, position JSON)",
        ).delete_all()

    def test_create_and_find(self):
        with patch.dict("os.environ", {"FEATURE_POINT_DB_TABLE": self.db_table}):
            db = FeaturePointDB()
            params = [1, [randint(0, 10), randint(0, 10), randint(0, 10)]]
            db.create(params[0], params[1])
            expected = (params[0], json.dumps(params[1]))

            self.assertEqual(expected, db.find(params[0]))
