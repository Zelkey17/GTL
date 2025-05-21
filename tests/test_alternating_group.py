import unittest

from elements.permutation_element import PermutationElement
from groups.AlternatingGroup import AlternatingGroup
from sympy.combinatorics import Permutation

class TestAlternatingGroup(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(ValueError):
            AlternatingGroup(0)
        with self.assertRaises(ValueError):
            AlternatingGroup(-2)
        self.assertEqual(AlternatingGroup(1)._rank, 1)

    def test_identity(self):
        g = AlternatingGroup(3)
        self.assertEqual(g.identity().value, [1, 2, 3])

    def test_group_operation(self):
        g = AlternatingGroup(3)
        a = g["(1, 3, 2)"]
        b = g["(3, 1, 2)"]
        product = a * b
        self.assertEqual(product, g.identity())

    def test_inverse(self):
        g = AlternatingGroup(3)
        a = g["(1, 2, 3)"]
        inv_a = g.inverse(a)
        self.assertEqual(inv_a.value, [2, 3, 1])
        self.assertEqual(a * inv_a, g.identity())

    def test_abelian_property(self):
        self.assertTrue(AlternatingGroup(3).is_abelian())
        self.assertFalse(AlternatingGroup(4).is_abelian())

    def test_simple_property(self):
        self.assertTrue(AlternatingGroup(5).is_simple())
        self.assertFalse(AlternatingGroup(4).is_simple())

    def test_solvable_property(self):
        self.assertTrue(AlternatingGroup(4).is_solvable())
        self.assertFalse(AlternatingGroup(5).is_solvable())

    def test_group_order(self):
        self.assertEqual(len(AlternatingGroup(3)), 3)
        self.assertEqual(len(AlternatingGroup(4)), 12)
        self.assertEqual(len(AlternatingGroup(1)), 1)

    def test_commutator_subgroup(self):
        a3 = AlternatingGroup(3)
        self.assertEqual(len(a3.comutator()), 1)

        a5 = AlternatingGroup(5)
        self.assertEqual(len(a5.comutator()), len(a5))

        with self.assertRaises(NotImplementedError):
            AlternatingGroup(4).comutator()

    def test_center(self):
        a3 = AlternatingGroup(3)
        self.assertEqual(len(a3.center()), 3)

        a4 = AlternatingGroup(4)
        self.assertEqual(len(a4.center()), 1)

    def test_element_creation_from_string(self):
        g = AlternatingGroup(3)
        elem = g["(3, 2, 1)"]
        self.assertEqual(elem.value, [2, 3, 1])

    def test_element_creation_from_cycles(self):
        g = AlternatingGroup(4)
        elem = g[[(1, 2),(3, 4)]]
        self.assertEqual(elem.value, [2, 1, 4, 3])

    def test_invalid_permutation_parity(self):
        g = AlternatingGroup(3)
        with self.assertRaises(ValueError):
            g[[2, 4, 1]]

    def test_membership(self):
        g = AlternatingGroup(3)
        elem = g["(1, 2, 3)"]
        self.assertIn(elem, g)

        g2 = AlternatingGroup(4)
        self.assertNotIn(elem, g2)

    def test_group_iterator(self):
        g = AlternatingGroup(3)
        elements = list(g)
        self.assertEqual(len(elements), 3)
        expected = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
        for elem in elements:
            self.assertIn(elem.value, expected)

    def test_cycle_parsing_edge_cases(self):
        g = AlternatingGroup(4)
        elem = g["(1, 2)(3, 4)"]
        self.assertEqual(len(elem.value), 4)

if __name__ == '__main__':
    unittest.main()