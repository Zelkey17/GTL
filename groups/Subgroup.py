
from typing import Generic, TypeVar, Set, Callable, Iterable
from itertools import product

from groups.finite_group import FiniteGroup

class SubGroup[E]():
    """
    Класс, представляющий подгруппу группы G.

    Подгруппа определяется набором элементов, замкнутым относительно операции группы,
    обращений и содержащим нейтральный элемент.
    """
    def __init__(self, group: FiniteGroup, elements: Set[E]):
        self._group = group
        self._elements = set(elements)
        self._validate()

    @property
    def group(self) -> FiniteGroup:
        """Возвращает родительскую группу G."""
        return self._group

    def elements(self) -> Set[E]:
        """Возвращает все элементы подгруппы."""
        return set(self._elements)

    def contains(self, element: E) -> bool:
        """Проверяет, содержит ли подгруппа данный элемент."""
        return element in self._elements and element.group is self._group

    def is_subgroup(self, other: 'SubGroup[E]') -> bool:
        """Проверяет, является ли self подгруппой other."""
        return self._group is other._group and self._elements.issubset(other._elements)

    def is_normal(self) -> bool:
        """Проверяет нормальность подгруппы: gHg^{-1} = H для всех g ∈ G."""
        for g in self._group._all_elements():
            for h in self._elements:
                conjugate = self._group.op(g, self._group.op(h, self._group.inverse(g)))
                if conjugate not in self._elements:
                    return False
        return True

    @classmethod
    def generated_by(cls, generators: Iterable[E], group: FiniteGroup) -> "SubGroup[E]":
        """
        Строит наименьшую подгруппу, порожденную переданными элементами.
        Итеративно замыкает генераторы под операциями и инверсией.
        """
        gens = set(generators)
        elems = {group.identity()} | gens
        changed = True
        while changed:
            changed = False
            new_elems = set(elems)
            for a, b in product(elems, repeat=2):
                new = group.op(a, b)
                if new not in elems:
                    new_elems.add(new)
            for a in elems:
                inv = group.inverse(a)
                if inv not in elems:
                    new_elems.add(inv)
            if new_elems != elems:
                elems = new_elems
                changed = True
        return cls(group, elems)

    @classmethod
    def from_predicate(cls, predicate: Callable[[E], bool], group: FiniteGroup) -> 'SubGroup[E]':
        """
        Строит подгруппу по предикату на элементы группы.
        Предикат должен задавать замкнутое множество.
        """
        elems = {el for el in group._all_elements() if predicate(el)}
        return cls(group, elems)

    @classmethod
    def trivial_identity(cls, group: FiniteGroup) -> 'SubGroup[E]':
        """Тривиальная подгруппа из одного нейтрального элемента."""
        return cls(group, {group.identity()})

    @classmethod
    def trivial_all(cls, group: FiniteGroup) -> 'SubGroup[E]':
        """Подгруппа, совпадающая с самой группой."""
        elems = set(group._all_elements())
        return cls(group, elems)

    def __len__(self) -> int:
        """Порядок подгруппы (количество элементов)."""
        return len(self._elements)

    def _validate(self):
        # Нейтральный элемент
        if group_identity := self._group.identity() not in self._elements:
            raise ValueError("Подгруппа должна содержать нейтральный элемент группы")
        # Замкнутость относительно операции
        for a, b in product(self._elements, repeat=2):
            if self._group.op(a, b) not in self._elements:
                raise ValueError("Подгруппа не замкнута относительно групповой операции")
        # Замкнутость относительно инверсии
        for a in self._elements:
            if self._group.inverse(a) not in self._elements:
                raise ValueError("Подгруппа не замкнута относительно обращения")

    def __repr__(self) -> str:
        return f"SubGroup({{ {', '.join(repr(e) for e in self._elements)} }})"

