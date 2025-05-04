from __future__ import annotations

from typing import Set, Callable, Iterable
from itertools import product
from groups.finite_group import FiniteGroup



class SubGroup[E]:
    """
    Класс, представляющий подгруппу конечной группы G.

    Подгруппа определяется как непустое множество, замкнутое относительно
    групповой операции и обращения, и содержащее нейтральный элемент.
    """

    def __init__(self, group: FiniteGroup[E], elements: Set[E]): # TODO
        self._group = group
        self._elements = set(elements)
        self._validate()

    @property
    def group(self) -> FiniteGroup[E]: # TODO
        """Возвращает родительскую группу G."""
        return self._group

    def elements(self) -> Set[E]:
        """Возвращает все элементы подгруппы."""
        return set(self._elements)

    def contains(self, element: E) -> bool:
        """Проверяет, содержится ли элемент в подгруппе."""
        return element in self._elements and element.group is self._group

    def is_subgroup(self, other: SubGroup[E]) -> bool:
        """Проверяет, является ли self подгруппой other."""
        return self._group is other._group and self._elements.issubset(other._elements)

    def is_normal(self) -> bool:
        """
        Проверяет, является ли подгруппа нормальной:
        ∀ g ∈ G, ∀ h ∈ H: g * h * g⁻¹ ∈ H.
        """
        for g in self._group._all_elements():
            for h in self._elements:
                conjugate = self._group.op(g, self._group.op(h, self._group.inverse(g)))
                if conjugate not in self._elements:
                    return False
        return True

    @classmethod
    def generated_by(cls, generators: Iterable[E], group: FiniteGroup[E]) -> SubGroup[E]: # TODO
        """
        Строит подгруппу, порожденную указанными элементами (итеративное замыкание).
        """
        gens = set(generators)
        elems = {group.identity()} | gens
        changed = True
        while changed:
            changed = False
            new_elems = set(elems)
            for a, b in product(elems, repeat=2):
                c = group.op(a, b)
                if c not in elems:
                    new_elems.add(c)
            for a in elems:
                inv = group.inverse(a)
                if inv not in elems:
                    new_elems.add(inv) # TODO
            if new_elems != elems:
                elems = new_elems
                changed = True
        return cls(group, elems)

    @classmethod
    def from_predicate(cls, predicate: Callable[[E], bool], group: FiniteGroup[E]) -> SubGroup[E]: # TODO
        """
        Строит подгруппу по предикату (предикат должен задавать подгруппу).
        """
        elems = {el for el in group._all_elements() if predicate(el)}
        return cls(group, elems)

    @classmethod
    def trivial_identity(cls, group: FiniteGroup[E]) -> SubGroup[E]: # TODO
        """Возвращает тривиальную подгруппу {e}."""
        return cls(group, {group.identity()})

    @classmethod
    def trivial_all(cls, group: FiniteGroup[E]) -> SubGroup[E]: # TODO
        """Подгруппа, совпадающая с самой группой."""
        return cls(group, set(group._all_elements()))

    def __len__(self) -> int:
        """Порядок подгруппы (количество элементов)."""
        return len(self._elements)

    def _validate(self):
        """Проверяет аксиомы подгруппы."""
        identity = self._group.identity()
        if identity not in self._elements:
            raise ValueError("Подгруппа должна содержать нейтральный элемент группы")
        for a, b in product(self._elements, repeat=2):
            if self._group.op(a, b) not in self._elements:
                raise ValueError("Подгруппа не замкнута относительно групповой операции")
        for a in self._elements:
            if self._group.inverse(a) not in self._elements:
                raise ValueError("Подгруппа не замкнута относительно обращения")

    def __repr__(self) -> str:
        """Читаемое строковое представление подгруппы."""
        elems_str = ", ".join(repr(e) for e in sorted(self._elements, key=repr))
        return f"SubGroup({{{elems_str}}})"
