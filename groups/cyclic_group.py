from .base import E, Group
from ..elements.element import IntegerElement
from .finite_group import FiniteGroup

class CyclicGroup(FiniteGroup):
    """

    """
    def __init__(self, order : int):
        if order <= 0:
            raise Exception("Порядок группы положительное число")
        self._order = order

    def identity(self) -> IntegerElement:
        return IntegerElement(0, self)

    def op(self, a: IntegerElement, b: IntegerElement) -> IntegerElement:
        return IntegerElement((a.value + b.value) % self._order, self)

    def inverse(self, a: IntegerElement) -> IntegerElement:
        return IntegerElement(self._order - a.value - 1)

    def __len__(self):
        return self._order

    def is_lagrangian(self) -> bool:
        return True

    def is_abelian(self) -> bool:
        return True

    def is_simple(self) -> bool:
        return True

    def is_solvable(self) -> bool:
        return True

    def comutator(self) -> "SubGroup":
        return SubGroup.trivial_all(self)

    def center(self) -> "SubGroup":
        return SubGroup.trivial_all(self)
