from __future__ import annotations

from typing import List, Tuple
from copy import copy

from elements.base import Element
from groups.base import Group


class PermutationElement(Element[List[int]]):
    """
    Элемент группы перестановок, заданный списком образов.

    Представляет перестановку множества {1,…,n}, где _value[i-1] — образ i-го элемента.

    Attributes:
        _value (List[int]): Список образов перестановки длины n.
        _reference_to_group (Group[List[int], PermutationElement]):
            Ссылка на группу, к которой принадлежит элемент.
    """

    def __init__(
        self,
        value: List[int],
        reference_to_group: Group[List[int], PermutationElement],
    ):
        """
        Инициализирует элемент перестановки.

        Args:
            value (List[int]): Список длины n, где value[i-1] — образ элемента i.
            reference_to_group (Group[List[int], PermutationElement]):
                Группа перестановок, содержащая этот элемент.
        """
        # Копируем, чтобы внешние изменения списка не влияли на элемент
        self._value = copy(value)
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> List[int]:
        """
        Внутреннее представление перестановки.

        Returns:
            List[int]: Список образов элементов.
        """
        return self._value

    @property
    def group(self) -> Group[List[int], PermutationElement]:
        """
        Группа, к которой принадлежит элемент.

        Returns:
            Group[List[int], PermutationElement]: Экземпляр группы перестановок.
        """
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает две перестановки на равенство.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True, если other — PermutationElement той же группы
                  и у них одинаковые списки образов.

        Raises:
            TypeError: Если other не Element или принадлежит другой группе.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: PermutationElement) -> PermutationElement:
        """
        Композиция перестановок (групповая операция).

        Args:
            other (PermutationElement): Перестановка справа.

        Returns:
            PermutationElement: Результат композиции self ◦ other.

        Raises:
            TypeError: Если other не Element или принадлежит другой группе.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> PermutationElement:
        """
        Возведение перестановки в целую степень.

        Args:
            power (int): Показатель степени (может быть отрицательным).
            modulo: Не используется (для совместимости с сигнатурой Python).

        Returns:
            PermutationElement: Результат self^power.
        """
        return self._reference_to_group.pow(self, power)

    def inv(self) -> PermutationElement:
        """
        Обратная перестановка.

        Returns:
            PermutationElement: Перестановка, обратная self (self ◦ inv = identity).
        """
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        """
        Читаемое представление перестановки.

        Returns:
            str: Образы, соединённые пробелом, например "2 3 1".
        """
        return " ".join(map(str, self._value))

    def cyclic_presentation(self, is_add_trivial: bool) -> List[Tuple[int, ...]]:
        """
        Возвращает циклическое представление перестановки.

        Args:
            is_add_trivial (bool): Если True, включает тривиальные 1‑циклы.

        Returns:
            List[Tuple[int, ...]]: Список кортежей, каждый — один цикл перестановки.

        Алгоритм:
            1. Создаем булев список used размера n+1.
            2. Для каждого i=1..n, если i не использован,
               следуем по образам, пока не вернемся к началу, формируя цикл.
            3. Добавляем цикл, если его длина >1 или is_add_trivial.
        """
        n = len(self._value)
        used = [False] * (n + 1)
        cycles: List[Tuple[int, ...]] = []

        for i in range(1, n + 1):
            if not used[i]:
                current = i
                cycle = []
                # Собираем цикл
                while not used[current]:
                    used[current] = True
                    cycle.append(current)
                    current = self._value[current - 1]
                if len(cycle) > 1 or is_add_trivial:
                    cycles.append(tuple(cycle))

        return cycles

    def __hash__(self) -> int:
        """
        Хэш для использования в множествах и словарях.

        Returns:
            int: Хэш от кортежа образов.
        """
        return hash(tuple(self._value))
