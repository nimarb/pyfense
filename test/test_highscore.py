"""
Test highscore class.
"""

import unittest

from pyfense import highscore


class TestHighscore(unittest.TestCase):

    """test highscore class"""

    def test_handling_wrong_charakters(self):
        """Test whether wrong charakters are handled correctly"""
        name = "§3.+"
        wave = 5
        highscore.new_score(name, wave)

    def test_check_score_with_wave_0(self):
        """Check whether wave 0 can be checked"""
        highscore.check_score(0)

    def test_check_score_with_very_high_wave(self):
        """Check whether a very high wave is checked correctly"""
        result = highscore.check_score(9999999)
        actualResult = 1
        self.assertEqual(result, actualResult)

    def test_get_score(self):
        """Test whether get_score runs without error"""
        highscore.get_score()
