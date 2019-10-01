import unittest

from guess_my_x import GMX


class TestGMX(unittest.TestCase):

    def test_initialization(self):
        """
        Simple test to confirm that you can initialize a
        GMX instance.
        """

        guess_my_number = GMX(list(range(100)))

        self.assertIsInstance(guess_my_number, GMX)


