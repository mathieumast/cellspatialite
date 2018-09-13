import unittest
import cluster
import math

class CellTest(unittest.TestCase):
    def test_cell_to_pos_to_cell(self):
        for level in range(3, 12):
            for r in range(-3, 4):
                for q in range(-3, 4):
                    c1 = cluster.Cell(q, r, level)
                    p1 =  c1.center()
                    c2 = p1.cell(level)
                    p2 =  c2.center()
                    self.assertEqual(c1, c2)
                    self.assertEqual(p1, p2)

    def test_cell_to_wkt(self):
        c = cluster.Cell(10, 10, 5)
        self.assertEqual(c.wkt(), 'POLYGON((97856.5405006 56497.5, 94699.8779038 58320.0, 91543.215307 56497.5, 91543.215307 52852.5, 94699.8779038 51030.0, 97856.5405006 52852.5, 97856.5405006 56497.5))')

    def test_pos_to_cell(self):
        p = cluster.Pos(96000, 55000)
        self.assertEqual(p.cell(5), cluster.Cell(10, 10, 5))

if __name__ == '__main__':
    unittest.main()