import unittest
from groups.custom import CustomGroup

class TestCustomGroup(unittest.TestCase):

    def test_creation_and_basic_operations(self):
        """Тест создания группы и базовых операций."""
        index = {0: 0, 1: 1, 2: 2}
        op = lambda a, b: (a + b) % 3
        inv = lambda a: (3 - a) % 3
        group = CustomGroup(index, op, inv, verify=True)

        self.assertEqual(len(group), 3)
        self.assertEqual(group.identity().value, 0)

        a = group[1]
        b = group[2]
        self.assertEqual(group.op(a, b).value, 0)
        self.assertEqual(group.inverse(a).value, 2)

        elements = list(group)
        self.assertEqual(len(elements), 3)
        self.assertEqual({e.value for e in elements}, {0, 1, 2})

    def test_is_abelian(self):
        """Тест проверки абелевости группы."""
        # Абелева группа (циклическая порядка 3)
        index = {0: 0, 1: 1, 2: 2}
        group = CustomGroup(index,
                            op=lambda a, b: (a + b) % 3,
                            inv=lambda a: (3 - a) % 3
                            )
        self.assertTrue(group.is_abelian())

    def test_is_solvable(self):
        """Тест разрешимости группы."""
        # Абелева группа порядка 2
        group = CustomGroup(
            index={0: 0, 1: 1},
            op=lambda a, b: (a + b) % 2,
            inv=lambda a: a
        )
        self.assertTrue(group.is_solvable())

    def test_comutator(self):
        """Тест вычисления коммутанта."""
        # Абелева группа
        group = CustomGroup(
            index={0: 0, 1: 1, 2: 2},
            op=lambda a, b: (a + b) % 3,
            inv=lambda a: (-a) % 3
        )
        self.assertEqual(len(group.comutator()), 1)

    def test_center(self):
        """Тест вычисления центра."""
        # Абелева группа
        group = CustomGroup(
            index={0: 0, 1: 1, 2: 2},
            op=lambda a, b: (a + b) % 3,
            inv=lambda a: (-a) % 3
        )
        self.assertEqual(len(group.center()), 3)

    def test_from_cayley(self):
        """Тест создания группы из таблицы Кэли."""
        # Циклическая группа порядка 2
        group = CustomGroup.from_cayley(
            table=[[0, 1], [1, 0]],
            verify=True
        )
        self.assertEqual(len(group), 2)
        self.assertEqual(group.op(group[0], group[1]).value, 1)

    def test_from_operation(self):
        """Тест создания группы из операции с замыканием."""
        # Группа порядка 2
        group = CustomGroup.from_operation(
            elems={'e': 'e', 'a': 'a'},
            op=lambda x,
                      y: 'e' if x != 'e' and y != 'e' else x if y == 'e' else y,
            inv=lambda x: x
        )
        self.assertEqual(len(group), 2)
        self.assertEqual(group.op(group['a'], group['a']).value, 'e')

    def test_invalid_cayley_table(self):
        """Тест обработки некорректной таблицы Кэли."""
        with self.assertRaises(Exception):
            CustomGroup.from_cayley(
                table=[[0, 1], [0, 1]],  # Не латинский квадрат
                verify=True
            )

    def test_verify_group_axioms(self):
        """Тест проверки аксиом группы при создании."""
        with self.assertRaises(Exception):
            CustomGroup(
                index={0: 0, 1: 1},
                op=lambda a, b: 1,  # Неассоциативная операция
                inv=lambda a: a,
                verify=True
            )


if __name__ == '__main__':
    unittest.main()