"""
Test resources.
"""
import unittest
from pyfense import resources


class TestResources(unittest.TestCase):
    def test_tower(self):
        for towername in resources.tower:
            self.assertIn(1, resources.tower[towername])
            self.assertIn("damage", resources.tower[towername][1])
            self.assertIn("cost", resources.tower[towername][1])
            self.assertIn("range", resources.tower[towername][1])
            self.assertIn("image", resources.tower[towername][1])
            self.assertIn("firerate", resources.tower[towername][1])

    def test_enemy(self):
        for enemyname in resources.enemy:
            self.assertIn("worth", resources.enemy[enemyname][1])
            self.assertIn("image", resources.enemy[enemyname][1])

    def test_waves(self):
        self.assertIn(1, resources.waves)

if __name__ == '__main__':
    unittest.main()
