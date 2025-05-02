import unittest
from ..groups.cyclic_group import CyclicGroup, IntegerElement

class TestCyclicGroup(unittest.TestCase):
    """
    Тесты для циклической группы
    """
    def setUp(self):
        """Создаём тестовые группы разных порядков перед каждым тестом."""
        self.group_order_1 = CyclicGroup(1)  # Тривиальная группа
        self.group_order_2 = CyclicGroup(2)  # Простая группа
        self.group_order_4 = CyclicGroup(4)  # Непростая группа
        self.group_order_5 = CyclicGroup(5)  # Простая группа

    def TestNegativeOrderRaisesException(self):
        """Проверяем обработку отрицательного порядка."""
        with self.assertRaises(Exception) as context:
            CyclicGroup(-1)
        self.assertEqual(str(context.exception), "Порядок группы положительное число")

    def TestZeroOrderRaisesException(self):
        """Проверяем обработку нулевого порядка."""
        with self.assertRaises(Exception) as context:
            CyclicGroup(0)
        self.assertEqual(str(context.exception), "Порядок группы положительное число")

    def TestIdentity(self):
        """Тестируем получение нейтрального элемента."""
        self.assertEqual(self.group_order_1.identity().value, 0)
        self.assertEqual(self.group_order_2.identity().value, 0)

    def TestOp(self):
        """Тестируем групповую операцию (сложение по модулю)."""
        elem1 = IntegerElement(1, self.group_order_4)
        elem2 = IntegerElement(3, self.group_order_4)
        self.assertEqual(self.group_order_4.op(elem1, elem2).value, 0)  # 1 + 3 mod 4 = 0

    def TestInverseForZeroElement(self):
        """Тестируем получение обратного элемента для нуля."""
        zero_elem = IntegerElement(0, self.group_order_5)
        self.assertEqual(self.group_order_5.inverse(zero_elem).value, 0,
                         "Обратный к 0 должен быть 0 в любой группе")

    def TestInverseConsistency(self):
        """Тестируем, что двойное взятие обратного элемента возвращает исходный элемент."""
        elem = IntegerElement(3, self.group_order_4)
        inverse_elem = self.group_order_4.inverse(elem)
        inverse_inverse_elem = self.group_order_4.inverse(inverse_elem)
        self.assertEqual(inverse_inverse_elem.value, elem.value,
                         "Двойное взятие обратного должно давать исходный элемент")

    def TestIsSimple(self):
        """Тестируем проверку на
         группы."""
        self.assertTrue(self.group_order_1.is_simple())
        self.assertTrue(self.group_order_5.is_simple())
        self.assertFalse(self.group_order_4.is_simple())

if __name__ == '__main__':
    unittest.main()