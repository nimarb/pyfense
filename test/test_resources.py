# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:20:10 2015

@author: Matthias
"""

import unittest
import pyfense_resources


class TestResources(unittest.TestCase):
    def test_tower(self):
        for towername in pyfense_resources.tower:
            self.assertIn(1, pyfense_resources.tower[towername])
            self.assertIn("damage", pyfense_resources.tower[towername][1])
            self.assertIn("cost", pyfense_resources.tower[towername][1])
            self.assertIn("range", pyfense_resources.tower[towername][1])
            self.assertIn("image", pyfense_resources.tower[towername][1])
            self.assertIn("firerate", pyfense_resources.tower[towername][1])

    def test_enemy(self):
        for enemyname in pyfense_resources.enemy:
            self.assertIn("worth", pyfense_resources.enemy[enemyname][1])
            self.assertIn("image", pyfense_resources.enemy[enemyname][1])

if __name__ == '__main__':
    unittest.main()
