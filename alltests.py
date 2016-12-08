import unittest
import sys

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('tests', 'test*.py')
    unittest.TextTestRunner().run(all_tests)
