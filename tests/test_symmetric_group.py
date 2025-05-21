import unittest
from elements.permutation_element import PermutationElement
from groups.symmetric_group import SymmetricGroup
from utils.is_isomorphic import is_isomorphic


class TestSymmetricGroup(unittest.TestCase):
    def setUp(self):
        self.rank_test_cases = [1, 2, 3, 4, 5]

    # Тесты инициализации
    def test_initialization_invalid_rank(self):
        with self.assertRaises(ValueError):
            SymmetricGroup(0)
        with self.assertRaises(ValueError):
            SymmetricGroup(-1)

    def test_initialization_valid_rank(self):
        for rank in [1, 2, 3]:
            SymmetricGroup(rank)

    # Тесты для identity()
    def test_identity(self):
        s3 = SymmetricGroup(3)
        self.assertEqual(s3.identity().value, [1, 2, 3])

    # Тесты операции композиции
    def test_op_composition(self):
        s3 = SymmetricGroup(3)
        a = s3[[2, 1, 3]]  # (1 2)
        b = s3[[3, 2, 1]]  # (1 3)
        self.assertEqual((a * b).value, [2, 3, 1])

    def test_op_different_groups(self):
        s2 = SymmetricGroup(2)
        s3 = SymmetricGroup(3)
        a = s2[[2, 1]]
        b = s3[[2, 1, 3]]
        with self.assertRaises(TypeError):
            s3.op(a, b)

    # Тесты inverse()
    def test_inverse(self):
        s3 = SymmetricGroup(3)
        a = s3[[2, 3, 1]]
        self.assertEqual(s3.inverse(a).value, [3, 1, 2])

    # Параметризованные тесты через subTest
    def test_group_properties(self):
        test_cases = [
            ('abelian', [(1, True), (2, True), (3, False), (4, False)]),
            ('simple', [(1, True), (2, True), (3, False), (4, False)]),
            ('solvable',
             [(1, True), (2, True), (3, True), (4, True), (5, False)]),
            ('lagrangian',
             [(1, True), (2, True), (3, True), (4, True), (5, False)]),
        ]

        for prop, cases in test_cases:
            with self.subTest(property=prop):
                for rank, expected in cases:
                    group = SymmetricGroup(rank)
                    method = getattr(group, f'is_{prop}')
                    self.assertEqual(method(), expected)

    # Тесты порядка группы
    def test_order(self):
        self.assertEqual(len(SymmetricGroup(3)), 6)
        self.assertEqual(len(SymmetricGroup(4)), 24)

    # Тесты центра
    def test_center(self):
        s2 = SymmetricGroup(2)
        self.assertEqual(len(s2.center()), 2)

        s3 = SymmetricGroup(3)
        self.assertEqual(len(s3.center()), 1)

    # Тесты создания элементов
    def test_element_creation(self):
        s3 = SymmetricGroup(3)

        test_cases = [
            ('list', [2, 1, 3], [2, 1, 3]),
            ('cycle', [(1, 2)], [2, 1, 3]),
            ('string', "(1,2)", [2, 1, 3])
        ]

        for case_type, input_val, expected in test_cases:
            with self.subTest(case=case_type):
                elem = s3[input_val]
                self.assertEqual(elem.value, expected)

    def test_invalid_element(self):
        s3 = SymmetricGroup(3)
        with self.assertRaises(ValueError):
            s3[[1, 1, 2]]

    # Тесты принадлежности
    def test_contains(self):
        s3 = SymmetricGroup(3)
        self.assertIn(s3[[2, 1, 3]], s3)

        s2 = SymmetricGroup(2)
        self.assertNotIn(s2[[2, 1]], s3)

    # Тесты итератора
    def test_iterator(self):
        s2 = SymmetricGroup(2)
        elements = list(s2)
        self.assertEqual(len(elements), 2)
        self.assertTrue(
            all(isinstance(e, PermutationElement) for e in elements))

    # Тест коммутанта
    def test_comutator_exception(self):
        s3 = SymmetricGroup(3)
        with self.assertRaises(NotImplementedError):
            s3.comutator()

    # Тесты изоморфизма
    def test_isomorphism(self):
        s2a = SymmetricGroup(2)
        s2b = SymmetricGroup(2)
        mapping = is_isomorphic(s2a, s2b)
        self.assertIsNotNone(mapping)

        # Проверка сохранения операций
        for a in s2a:
            for b in s2a:
                self.assertEqual(
                    mapping[s2a.op(a, b)],
                    s2b.op(mapping[a], mapping[b])
                )

        # Группы разного порядка
        s3 = SymmetricGroup(3)
        self.assertIsNone(is_isomorphic(s2a, s3))


if __name__ == '__main__':
    unittest.main()