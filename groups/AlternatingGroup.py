from __future__ import annotations

import math
from itertools import product
from typing import Iterator, List, Tuple, Union

from sympy.combinatorics import Permutation

from elements.permutation_parser import PermutationParser
from elements.permutation_element import PermutationElement
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup



class AlternatingGroup(FiniteGroup[List[int], PermutationElement]):
    """
    Группа чётных перестановок ранга n.

    Каждый элемент — это перестановка множества {1, ..., n}, удовлетворяющая условию чётности.
    Реализует лишь чётные перестановки (подгруппа A_n симметрической группы).

    Attributes:
        _rank (int): Ранг (n), число элементов, над которыми действуют перестановки.
    """

    def __init__(self, rank: int):
        """
        Инициализирует группу чётных перестановок.

        Args:
            rank (int): Положительный ранг группы.

        Raises:
            ValueError: Если rank <= 0.
        """
        if rank <= 0:
            raise ValueError("Ранг группы должен быть положительным числом")
        self._rank = rank

    def identity(self) -> List[int]:
        """
        Тождественная перестановка (нейтральный элемент).

        Returns:
            List[int]: [1, 2, ..., n].
        """
        return list(range(1, self._rank + 1))

    def op(self, a: PermutationElement,
           b: PermutationElement) -> PermutationElement:
        """
        Композиция перестановок: сначала a, затем b.

        Args:
            a (PermutationElement): Левая перестановка.
            b (PermutationElement): Правая перестановка.

        Returns:
            PermutationElement: Результат композиции b ◦ a.

        Raises:
            TypeError: Если a или b не принадлежат этой группе.
        """
        if a.group is not self or b.group is not self:
            raise TypeError("Элементы принадлежат разным группам")
        perm = [b.value[a.value[i] - 1] for i in range(self._rank)]
        return PermutationElement(perm, self)

    def inverse(self, a: PermutationElement) -> PermutationElement:
        """
        Обратная перестановка (a⁻¹), удовлетворяющая a ◦ a⁻¹ = identity.

        Args:
            a (PermutationElement): Перестановка для инверсии.

        Returns:
            PermutationElement: Инверсия a.

        Raises:
            TypeError: Если a не принадлежит этой группе.
        """
        if a.group is not self:
            raise TypeError("Элемент принадлежит другой группе")
        perm = [0] * self._rank
        for i in range(self._rank):
            perm[a.value[i] - 1] = i + 1
        return PermutationElement(perm, self)

    def is_lagrangian(self) -> bool:
        """
        Проверяет теорему Лагранжа для группы чётных перестановок.

        Возвращает True для n ≤ 5 (известно, что A_n лагранжева до n=5).

        Returns:
            bool: True, если rank ≤ 5.
        """
        return self._rank <= 5

    def is_abelian(self) -> bool:
        """
        Проверяет коммутативность группы.

        A_n абелева лишь для n ≤ 3.

        Returns:
            bool: True, если rank ≤ 3.
        """
        return self._rank <= 3

    def is_simple(self) -> bool:
        """
        Проверяет, простая ли группа.

        A_n проста для всех n ≠ 4.

        Returns:
            bool: False только при rank == 4.
        """
        return self._rank != 4

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость группы.

        A_n разрешима лишь для n ≤ 4.

        Returns:
            bool: True, если rank ≤ 4.
        """
        return self._rank <= 4

    def __len__(self) -> int:
        """
        Порядок группы чётных перестановок.

        |A_n| = n! / 2 для n ≥ 2, и 1 для n=1.

        Returns:
            int: (n! + 1) // 2.
        """
        return (math.factorial(self._rank) + 1) // 2

    def comutator(self) -> SubGroup[PermutationElement]:
        """
        Коммутант (производная группа) A_n.

        Для n ≤ 3 A_n абелева ⇒ коммутант тривиален.
        Для n > 4 A_n проста ⇒ коммутант = сама группа.
        Для n = 4 коммутант не реализован

        Returns:
            SubGroup[PermutationElement]: Коммутант A_n.

        Raises:
            NotImplementedError: Для rank == 4.
        """
        if self._rank <= 3:
            return SubGroup.trivial_identity(self)
        if self._rank > 4:
            return SubGroup.trivial_all(self)
        raise NotImplementedError("comutator не реализован для n = 4")

    def center(self) -> SubGroup[PermutationElement]:
        """
        Центр группы A_n.

        Для n ≤ 3 (абелева) центр = вся группа.
        Для n ≥ 4 центр тривиален = {identity}.

        Returns:
            SubGroup[PermutationElement]: Соответствующая подгруппа центра.
        """
        if self._rank <= 3:
            return SubGroup.trivial_all(self)
        return SubGroup.trivial_identity(self)

    def __getitem__(
        self,
        item: Union[List[int], List[Tuple[int, ...]], str]
    ) -> PermutationElement:
        """
        Создаёт элемент группы из различных представлений перестановки.

        Поддерживается:
          - Список образов [σ(1), ..., σ(n)].
          - Список циклов [(i1, i2, ...), ...].
          - Строка в циклической записи "(1,2)(3,4)".

        Args:
            item (Union[List[int], List[Tuple[int, ...]], str]):
                Описание перестановки.

        Returns:
            PermutationElement: Соответствующий элемент A_n.

        Raises:
            ValueError: Если формат неверен, перестановка некорректна или нечётна.
        """
        def _check_list(perm: List[int]) -> None:
            if sorted(perm) != list(range(1, self._rank + 1)):
                raise ValueError("Перестановка некорректна")
            if not Permutation(perm).is_even:
                raise ValueError("Перестановка нечётна")

        def _from_cycles(cycles: List[Tuple[int, ...]]) -> PermutationElement:
            base = list(range(1, self._rank + 1))
            current = base.copy()
            for cycle in cycles:
                if len(set(cycle)) != len(cycle):
                    raise ValueError("Цикл содержит повторяющиеся элементы")
                original = current.copy()
                for i in range(len(cycle)):
                    src = cycle[i] - 1
                    dst = cycle[(i + 1) % len(cycle)] - 1
                    current[dst] = original[src]
            _check_list(current)
            return PermutationElement(current, self)

        # 1) По списку образов
        if isinstance(item, list) and all(isinstance(x, int) for x in item):
            _check_list(item)
            return PermutationElement(item, self)

        # 2) По списку циклов
        if (isinstance(item, list)
                and all(isinstance(c, tuple) for c in item)
                and all(all(isinstance(x, int) for x in c) for c in item)): # TODO
            return _from_cycles(item)

        # 3) По строке циклической записи
        if isinstance(item, str):
            parser = PermutationParser()
            cycles = parser.parse(item)
            return _from_cycles(cycles)

        raise ValueError("Неверный формат индекса для SymmetricGroup")

    def __contains__(self, item: object) -> bool:
        """
        Проверяет принадлежность элемента группе.

        Args:
            item (object): Объект для проверки.

        Returns:
            bool: True, если item — PermutationElement этой группы.
        """
        return isinstance(item, PermutationElement) and item.group == self

    def __iter__(self) -> Iterator[PermutationElement]:
        """
        Итератор по всем чётным перестановкам ранга n.

        Генерирует все списки длины n без повторений и фильтрует по чётности.

        Returns:
            Iterator[PermutationElement]: Все n!/2 элементов группы.
        """
        for perm in product(range(1, self._rank + 1), repeat=self._rank):
            if len(set(perm)) == self._rank and Permutation(list(perm)).is_even:
                yield self[list(perm)]
