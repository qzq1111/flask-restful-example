import unittest
import os
from app.factory import create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        pwd = os.path.abspath(os.path.dirname(os.getcwd()))
        config_path = os.path.join(pwd, 'config/config.yaml')
        app = create_app(config_name="DEVELOPMENT", config_path=config_path)
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_logger(self):
        rv = self.app.get('/logs')
        self.assertEqual(rv.data.decode("utf-8"), "ok")

    def test_unified_response(self):
        rv = self.app.get('/unifiedResponse')
        data = rv.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["msg"], '成功')
        self.assertDictEqual(data["data"], {'age': 18, 'name': 'zhang'})

    def test_packed_response(self):
        rv = self.app.get('/packedResponse')
        data = rv.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["msg"], '成功')
        self.assertDictEqual(data["data"], dict(name="zhang", age=18))

    def test_type_response(self):
        rv = self.app.get('/typeResponse')
        data = rv.get_json()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["code"], 0)
        self.assertEqual(data["msg"], '成功')
        data = data["data"]
        self.assertIsInstance(data["now"], str)
        self.assertIsInstance(data["date"], str)
        self.assertIsInstance(data["num"], str)
        self.assertEqual(data["num"], '11.11')

