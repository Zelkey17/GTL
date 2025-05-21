from __future__ import annotations

import math
from itertools import product
from typing import Iterator, List, Tuple, Union

from elements.permutation_element import PermutationElement
from elements.permutation_parser import PermutationParser
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup


class SymmetricGroup(FiniteGroup[List[int], PermutationElement]):
    """
    Симметрическая группа S_n ранга n.

    Группа всех перестановок множества {1, 2, ..., n} с операцией композиции.
    """

    def __init__(self, rank: int):
        """
        Инициализирует симметрическую группу.

        Args:
            rank (int): Ранг группы, количество элементов (n > 0).

        Raises:
            ValueError: Если rank <= 0.
        """
        if rank <= 0:
            raise ValueError("Ранг группы должен быть положительным числом")
        self._rank = rank

    def identity(self) -> PermutationElement:
        """
        Нейтральный элемент группы — тождественная перестановка.

        Returns:
            List[int]: Список [1, 2, ..., n].
        """
        return PermutationElement(list(range(1, self._rank + 1)), self)

    def op(self, a: PermutationElement,
           b: PermutationElement) -> PermutationElement:
        """
        Композиция перестановок: сначала выполняется a, затем b.

        Args:
            a (PermutationElement): Левая перестановка.
            b (PermutationElement): Правая перестановка.

        Returns:
            PermutationElement: Перестановка, эквивалентная b ◦ a.

        Raises:
            TypeError: Если a или b не принадлежат этой группе.
        """
        if a.group is not self or b.group is not self:
            raise TypeError("Элементы из разных групп")
        # Новый образ i = b(a(i))
        perm = [b.value[a.value[i] - 1] for i in range(self._rank)]
        return PermutationElement(perm, self)

    def inverse(self, a: PermutationElement) -> PermutationElement:
        """
        Обратная перестановка для a: находит b такую, что a ◦ b = identity.

        Args:
            a (PermutationElement): Исходная перестановка.

        Returns:
            PermutationElement: Инверсия перестановки a.

        Raises:
            TypeError: Если a не принадлежит этой группе.
        """
        if a.group is not self:
            raise TypeError("Элемент из другой группы")
        # Строим обратную перестановку: b[a[i]-1] = i+1
        perm = [0] * self._rank
        for i in range(self._rank):
            perm[a.value[i] - 1] = i + 1
        return PermutationElement(perm, self)

    def is_lagrangian(self) -> bool:
        """
        Проверяет, удовлетворяет ли группа обратной теореме Лагранжа.

        Для S_n это верно лишь для n ≤ 4.

        Returns:
            bool: True, если rank ≤ 4.
        """
        return self._rank <= 4

    def is_abelian(self) -> bool:
        """
        Проверяет, является ли группа коммутативной.

        S_n абелева только для n ≤ 2.

        Returns:
            bool: True, если rank ≤ 2.
        """
        return self._rank <= 2

    def is_simple(self) -> bool:
        """
        Проверяет простоту группы.

        S_n проста только для n ≤ 2.

        Returns:
            bool: True, если rank ≤ 2.
        """
        return self._rank <= 2

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость группы.

        S_n разрешима только для n ≤ 4.

        Returns:
            bool: True, если rank ≤ 4.
        """
        return self._rank <= 4

    def __len__(self) -> int:
        """
        Количество элементов группы.

        Returns:
            int: n! (факториал ранга).
        """
        return math.factorial(self._rank)

    def comutator(self) -> SubGroup[PermutationElement,SymmetricGroup]:
        """
        Коммутант (производная группа) S_n.

        Этот метод пока не реализован: для n ≥ 3 коммутант = A_n.

        Raises:
            NotImplementedError: Чтобы указать на необходимость реализации.
        """
        raise NotImplementedError("Метод comutator для SymmetricGroup ещё не реализован")

    def center(self) -> SubGroup[PermutationElement,SymmetricGroup]:
        """
        Центр группы — элементы, коммутирующие со всей группой.

        Для S_n центр тривиален:
          - n ≤ 2: все элементы (группа абелева) → SubGroup.trivial_all
          - n ≥ 3: только тождественная перестановка → SubGroup.trivial_identity

        Returns:
            SubGroup[PermutationElement]: Соответствующая тривиальная подгруппа.
        """
        if self._rank <= 2:
            return SubGroup.trivial_all(self)
        return SubGroup.trivial_identity(self)

    def __getitem__(
        self,
        item: Union[List[int], List[Tuple[int, ...]], str]
    ) -> PermutationElement:
        """
        Позволяет создавать элемент группы разными способами:

        1. По списку образов: [σ(1), σ(2), ..., σ(n)].
        2. По циклическому представлению: [(i₁, i₂, ...), ...].
        3. По строке формата "(1,2,3)(4,5)".

        Args:
            item (Union[List[int], List[Tuple[int, ...]], str]):
                — Список int;
                — Список кортежей int;
                — Строка с циклической записью.

        Returns:
            PermutationElement: Полученная перестановка.

        Raises:
            ValueError: Если передан неверный формат или некорректная перестановка.
        """
        def _check_correct(perm: List[int]) -> None:
            """
            Проверяет, что perm — перестановка {1..n}.

            Raises:
                ValueError: Если perm не содержит все числа от 1 до n ровно по одному.
            """
            if sorted(perm) != list(range(1, self._rank + 1)):
                raise ValueError("Перестановка некорректна")

        def _from_cycle_list(cycles: List[Tuple[int, ...]]) -> PermutationElement:
            """
            Строит перестановку из списка циклов.

            Args:
                cycles (List[Tuple[int, ...]]): Каждый кортеж — цикл.

            Returns:
                PermutationElement: Перестановка, полученная из последовательного применения циклов.

            Raises:
                ValueError: Если циклы некорректны.
            """
            # Начинаем с тождественной перестановки
            base = list(range(1, self._rank + 1))
            original = base.copy()
            for cycle in cycles:
                if len(set(cycle)) != len(cycle):
                    raise ValueError("Цикл содержит повторяющиеся элементы")
                # Применяем один цикл: склеиваем base по правилу
                for i in range(len(cycle)):
                    src = cycle[i] - 1
                    dst = cycle[(i + 1) % len(cycle)] - 1
                    base[dst] = original[src]
                original = base.copy()  # обновляем состояние перед следующим циклом
            _check_correct(base)
            return PermutationElement(base, self)

        # 1) Список образов
        if isinstance(item, list) and all(isinstance(x, int) for x in item):
            _check_correct(item)
            return PermutationElement(item, self)

        # 2) Список циклов
        if (isinstance(item, list)
                and all(isinstance(c, tuple) for c in item)
                and all(all(isinstance(x, int) for x in c) for c in item)): # TODO
            return _from_cycle_list(item)

        # 3) Строка с циклической записью
        if isinstance(item, str):
            parser = PermutationParser()
            cycles = parser.parse(item)
            return _from_cycle_list(cycles)

        raise ValueError("Неверный формат индекса для SymmetricGroup")

    def __contains__(self, item: PermutationElement) -> bool:
        """
        Проверяет, принадлежит ли элемент этой группе.

        Args:
            item (PermutationElement): Элемент для проверки.

        Returns:
            bool: True, если item.group == self.
        """
        return isinstance(item, PermutationElement) and item.group == self

    def __iter__(self) -> Iterator[PermutationElement]:
        """
        Итератор по всем перестановкам S_n.

        Порождает все кортежи длины n без повторов и конвертирует их в элементы.

        Returns:
            Iterator[PermutationElement]: Последовательность всех n! элементов.
        """
        for perm in product(range(1, self._rank + 1), repeat=self._rank):
            if len(set(perm)) == self._rank:
                yield self[list(perm)]
