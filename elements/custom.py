from elements.base import Element
from groups.base import Group


class CustomElement[T](Element[T]):
    def __init__(self, value: T,
                 reference_to_group: Group[T, 'CustomElement[T]']):
        self._value = value
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> T:
        return self._value

    @property
    def group(self) -> Group[T, 'CustomElement[T]']:

        return self._reference_to_group

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: 'CustomElement[T]') -> 'CustomElement[T]':

        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> 'CustomElement[T]':

        return self._reference_to_group.pow(self, power)

    def inv(self) -> 'CustomElement[T]':

        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:

        return str(self._value)

    def __hash__(self):
        return hash(self._value)
