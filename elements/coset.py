from typing import Set, TypeVar

from elements.base import Element

E = TypeVar('E', bound=Element)

class CosetElement(Element[Set[E]]):
    """
    Элемент фактор-группы в виде левого смежного класса aN.
    """
    def __init__(self, representative: E, factor_group: "FactorGroup[E]"):
        self._rep = representative
        self._factor_group = factor_group

    @property
    def representative(self) -> E:
        """Представитель смежного класса."""
        return self._rep

    @property
    def value(self) -> Set[E]:
        """Набор всех элементов смежного класса: aN = { n * a | n ∈ N }."""
        N = self._factor_group._subgroup
        G = self._factor_group._group
        return { G.op(n, self._rep) for n in N.elements() }

    @property
    def group(self) -> "FactorGroup[E]":
        return self._factor_group

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CosetElement) or self.group is not other.group:
            raise TypeError("Несовместимые элементы для сравнения в фактор-группе")
        # aN = bN <=> b^{-1} * a ∈ N
        N = self._factor_group._subgroup
        diff = other._rep.inv() * self._rep
        return N.contains(diff)

    def __mul__(self, other: "CosetElement[E]") -> "CosetElement[E]":
        if not isinstance(other, CosetElement) or self.group is not other.group:
            raise TypeError("Несовместимые элементы для умножения в фактор-группе")
        prod_rep = self._factor_group._group.op(self._rep, other._rep)
        return CosetElement(prod_rep, self._factor_group)

    def __pow__(self, exponent: int) -> "CosetElement[E]":
        pow_rep = self._factor_group._group.pow(self._rep, exponent)
        return CosetElement(pow_rep, self._factor_group)

    def inv(self) -> "CosetElement[E]":
        inv_rep = self._factor_group._group.inverse(self._rep)
        return CosetElement(inv_rep, self._factor_group)

    def __repr__(self) -> str:
        return f"Coset({self._rep!r}N)"
