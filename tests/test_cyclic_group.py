import unittest
from groups.cyclic_group import CyclicGroup, IntegerElement

class TestCyclicGroup(unittest.TestCase):
    def setUp(self):
        self.group_order_1 = CyclicGroup(1)
        self.group_order_2 = CyclicGroup(2)
        self.group_order_4 = CyclicGroup(4)
        self.group_order_5 = CyclicGroup(5)

    def test_negative_order_raises_exception(self):
        with self.assertRaises(Exception) as context:
            CyclicGroup(-1)
        self.assertEqual(str(context.exception), "Порядок группы положительное число")

    def test_zero_order_raises_exception(self):
        with self.assertRaises(Exception) as context:
            CyclicGroup(0)
        self.assertEqual(str(context.exception), "Порядок группы положительное число")

    def test_identity(self):
        self.assertEqual(self.group_order_1.identity().value, 0)
        self.assertEqual(self.group_order_2.identity().value, 0)

    def test_op(self):
        elem1 = IntegerElement(1, self.group_order_4)
        elem2 = IntegerElement(3, self.group_order_4)
        self.assertEqual(self.group_order_4.op(elem1, elem2).value, 0)

    def test_inverse_for_zero_element(self):
        zero_elem = IntegerElement(0, self.group_order_5)
        self.assertEqual(self.group_order_5.inverse(zero_elem).value, 0)

    def test_inverse_consistency(self):
        elem = IntegerElement(3, self.group_order_4)
        inverse_elem = self.group_order_4.inverse(elem)
        inverse_inverse_elem = self.group_order_4.inverse(inverse_elem)
        self.assertEqual(inverse_inverse_elem.value, elem.value)

    def test_is_simple(self):
        self.assertTrue(self.group_order_1.is_simple())
        self.assertTrue(self.group_order_5.is_simple())
        self.assertFalse(self.group_order_4.is_simple())

if __name__ == '__main__':
    unittest.main()
