import unittest
from algorithms.dynamic_programming import get_stations, get_lcs, _lcs_length

class TestDynamicProgrmming(unittest.TestCase):

    def test_get_stations(self):
        a = [[7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]]
        e = [2, 4]
        x = [3, 2]
        t = [[2, 3, 1, 3, 4, 0], [2, 1, 2, 2, 1, 0]]
        min, path, stations = get_stations(a, t, e, x, 6)
        self.assertEqual(min, 38)
        self.assertListEqual(path, [0, 5])
        self.assertListEqual(stations,
                             [(1, 4), (1, 3), (0, 2), (1, 1), (0, 0)])

    def test_get_lcs(self):
        x = "ABCBDAB"
        y = "BDCABA"
        b = _lcs_length(x, y)[1]
        lcs = []
        get_lcs(x, b, len(x), len(y), lcs)
        self.assertListEqual(lcs, ['B', 'C', 'B', 'A'])
