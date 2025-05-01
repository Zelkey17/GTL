from base import Element
from groups.base import Group

class IntegerElement(Element):
    """
    Представляет элемент группы с цеочисленными элементами.

    Этот класс реализует поведение элемента группы,
    где операции выполняются по правилам, заданным группой (Group).

    Attributes:
        _value (int): Значение элемента.
        _reference_to_group (Group[int, Element[int]]): Группа, к которой принадлежит элемент.
    """

    def __init__(self, value: int, reference_to_group: Group[int, 'Element[int]']):
        """
        Инициализирует элемент группы.

        Args:
            value: Целочисленное значение элемента.
            reference_to_group: Группа, к которой принадлежит элемент.
        """
        self._value = value
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> int:
        """Возвращает целочисленное значение элемента (геттер)."""
        return self._value

    @property
    def group(self) -> Group[int, Element[int]]:
        """Возвращает группу, к которой принадлежит элемент."""
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        """
        Проверяет равенство элементов.

        Raises:
            TypeError: Если элементы принадлежат разным группам.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: 'Element[int]') -> 'Element[int]':
        """
        Групповая операция.

        Args:
            other: Элемент той же группы.

        Returns:
            Новый элемент - результат групповой операции.

        Raises:
            TypeError: Если элементы принадлежат разным группам.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> 'Element[int]':
        """
        Возведение элемента в степень.

        Args:
            power: Показатель степени.

        Returns:
            Элемент, возведённый в указанную степень.
        """
        return self._reference_to_group.pow(self, power)

    def inv(self) -> 'Element[int]':
        """Возвращает обратный элемент относительно групповой операции."""
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        """Строковое представление элемента."""
        return str(self._value)