from __future__ import annotations

from typing import Generic, TypeVar

from elements.base import Element
from groups.base import Group



class CustomElement[T](Element[T]):
    """
    Обобщённый элемент группы, значение которого — объект произвольного типа T.

    Использует ссылку на экземпляр группы для выполнения операций, как делегат.
    """

    def __init__(self, value: T,
                 reference_to_group: Group[T, CustomElement[T]]):
        self._value = value
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> T:
        """Сырое значение элемента (например, int, str и т.п.)."""
        return self._value

    @property
    def group(self) -> Group[T, CustomElement[T]]:
        """Группа, к которой принадлежит элемент."""
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        """
        Сравнение двух элементов: по группе и значению.

        Raises:
            TypeError: если элемент другого типа или из другой группы.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: CustomElement[T]) -> CustomElement[T]:
        """
        Умножение двух элементов (делегируется группе).

        Raises:
            TypeError: если группы несовместимы.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> CustomElement[T]:
        """
        Возведение элемента в степень (делегируется группе).

        Параметр `modulo` игнорируется, т.к. группа не обязана быть по модулю.
        """
        return self._reference_to_group.pow(self, power)

    def inv(self) -> CustomElement[T]:
        """Обратный элемент (делегируется группе)."""
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        """Отображает значение как строку."""
        return str(self._value)

    def __hash__(self) -> int:
        """Хэш элемента по его значению."""
        return hash(self._value)
