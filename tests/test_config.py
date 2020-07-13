'''
@Author: KivenChen
@Date: 2019-04-22
@LastEditTime: 2019-04-30
'''
import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
from helper.config import Config


class TestConfig(unittest.TestCase):
    def test_init(self):
        pass

    def test_getUsername(self):
        config = Config()
        self.assertIsNotNone(config.username)

    def test_getPassword(self):
        config = Config()
        self.assertIsNotNone(config.password)

    def test_getOutputDir(self):
        config = Config()
        self.assertIsNotNone(config.outputDir)


if __name__ == "__main__":
    unittest.main()
