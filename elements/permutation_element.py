from .element import Element
from groups.base import Group

class PermutationElement(Element[list]):
    def __init__(self, value: list, reference_to_group: Group[list, 'PermutationElement']):
        self._value = value
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> list:
        return self._value

    @property
    def group(self) -> Group[list, 'PermutationElement']:
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return self._value == other.value

    def __mul__(self, other: 'PermutationElement') -> 'PermutationElement':
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> 'PermutationElement':
        return self._reference_to_group.pow(self, power)

    def inv(self) -> 'PermutationElement':
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        return str(*self._value)

    def cyclic_presentation(self, include_trivial : bool) -> list[tuple[int]]:
        perm = []
        used = [range(1, len(self) + 1)]

        for i in range(1, len(self) + 1):
            if not used[i]:
                cyc = (self._value[i], )
                while (self._value[cyc[-1] - 1] != cyc[0]):
                    cyc += (self._value[cyc[-1] - 1], )
                if len(cyc) > 1 or include_trivial:
                    perm += [cyc]
        return perm

    def __hash__(self) -> int:
        return hash(tuple(self._value))
