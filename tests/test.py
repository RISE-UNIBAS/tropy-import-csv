import unittest
from main import _Utility, Transform


class TestTransform(unittest.TestCase):
    """ Test Transform class. """

    def test_csv2json_1(self):
        """ Test csv2json where photos_path is None """

        Transform.csv2json("test_1.csv", "output.json")
        self.assertEqual(_Utility.load_json("gold_1.json"), _Utility.load_json("output.json"))

    def test_csv2json_2(self):
        """ Test csv2json where photos_path is not None """

        Transform.csv2json("test_2.csv", "output.json", photos_path="\\Path\\to\\photos\\")
        self.assertEqual(_Utility.load_json("gold_1.json"), _Utility.load_json("output.json"))


if __name__ == '__main__':
    unittest.main()