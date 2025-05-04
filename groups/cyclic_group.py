from __future__ import annotations

from collections.abc import Iterator
import sympy

from elements.integer import IntegerElement
from groups.finite_group import FiniteGroup



class CyclicGroup(FiniteGroup[int, IntegerElement]):
    """
    Циклическая группа целых чисел по модулю заданного порядка.

    Все элементы представляются как целые числа 0..order-1, операция — сложение по модулю order.

    Attributes:
        _order (int): Порядок группы (количество элементов).
    """

    def __init__(self, order: int):
        """
        Инициализирует циклическую группу.

        Args:
            order (int): Порядок группы. Должен быть положительным числом.

        Raises:
            ValueError: Если order <= 0.
        """
        if order <= 0:
            raise ValueError("Порядок группы должен быть положительным числом")
        self._order = order

    def __contains__(self, item: IntegerElement) -> bool:
        """
        Проверяет, принадлежит ли элемент этой группе.

        Args:
            item (IntegerElement): Элемент для проверки.

        Returns:
            bool: True, если item.group == self.
        """
        return isinstance(item, IntegerElement) and item.group == self

    def __iter__(self) -> Iterator[IntegerElement]:
        """
        Итератор по всем элементам группы.

        Returns:
            Iterator[IntegerElement]: Элементы от 0 до order-1.
        """
        return (IntegerElement(i, self) for i in range(self._order))

    def __len__(self) -> int:
        """
        Количество элементов группы.

        Returns:
            int: Порядок группы.
        """
        return self._order

    def identity(self) -> IntegerElement:
        """
        Нейтральный элемент группы.

        Returns:
            IntegerElement: Элемент 0 (модуль order).
        """
        return IntegerElement(0, self)

    def op(self, a: IntegerElement, b: IntegerElement) -> IntegerElement:
        """
        Групповая операция: сложение по модулю order.

        Args:
            a (IntegerElement): Первый операнд.
            b (IntegerElement): Второй операнд.

        Returns:
            IntegerElement: (a.value + b.value) % order.
        """
        return IntegerElement((a.value + b.value) % self._order, self)

    def inverse(self, a: IntegerElement) -> IntegerElement:
        """
        Обратный элемент.

        Args:
            a (IntegerElement): Элемент, для которого ищем обратный.

        Returns:
            IntegerElement: (-a.value) % order.
        """
        return IntegerElement((-a.value) % self._order, self)

    def is_lagrangian(self) -> bool:
        """
        Проверяет теорему Лагранжа.

        Для циклических групп всегда True.

        Returns:
            bool: True.
        """
        return True

    def is_abelian(self) -> bool:
        """
        Проверяет, является ли группа коммутативной.

        CyclicGroup всегда абелева.

        Returns:
            bool: True.
        """
        return True

    def is_simple(self) -> bool:
        """
        Проверяет простоту группы.

        Возвращает True, если order == 1 или order — простое число.

        Returns:
            bool: True, если простая.
        """
        return self._order == 1 or sympy.isprime(self._order)

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость группы.

        Все абелевы группы разрешимы.

        Returns:
            bool: True.
        """
        return True

    def comutator(self) -> SubGroup[int, IntegerElement]:
        """
        Возвращает коммутант группы — подгруппу, порождённую всеми коммутаторами.

        Для абелевых групп коммутант тривиален (только нейтральный элемент).

        Returns:
            SubGroup[int, IntegerElement]: Тривиальная подгруппа.
        """
        return SubGroup.trivial_identity(self)

    def center(self) -> SubGroup[int, IntegerElement]:
        """
        Возвращает центр группы — элементы, коммутирующие со всеми остальными.

        Для абелевых групп центр совпадает со всей группой.

        Returns:
            SubGroup[int, IntegerElement]: Подгруппа, содержащая все элементы группы.
        """
        return SubGroup.trivial_all(self)

    def __getitem__(self, item: int) -> IntegerElement:
        """
        Доступ к элементу по его целочисленному представлению.

        Args:
            item (int): Целочисленное значение.

        Returns:
            IntegerElement: Элемент с value == item % order.
        """
        return IntegerElement(item % self._order, self)
