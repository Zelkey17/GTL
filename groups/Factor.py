from itertools import chain
from typing import Set, TypeVar

from elements.base import Element
from elements.coset import CosetElement
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup

E = TypeVar('E', bound=Element)


class FactorGroup[E](FiniteGroup[set[E], CosetElement[E]]):
    def __init__(
            self,
            group: FiniteGroup,  # без скобок — любой FiniteGroup
            subgroup: SubGroup[E]
    ):
        if subgroup.group is not group:
            raise ValueError("Подгруппа должна принадлежать указанной группе")
        if not subgroup.is_normal():
            raise ValueError(
                "Подгруппа должна быть нормальной для построения фактор-группы")
        self._group = group
        self._subgroup = subgroup

    def identity(self) -> CosetElement:
        return CosetElement(self._group.identity(), self)

    def op(self, a: CosetElement, b: CosetElement) -> CosetElement:
        if a.group is not self or b.group is not self:
            raise ValueError("Элемент из другой группы")
        prod_rep = self._group.op(a.representative, b.representative)
        return CosetElement(prod_rep, self)

    def inverse(self, a: CosetElement) -> CosetElement:
        inv_rep = self._group.inverse(a.representative)
        return CosetElement(inv_rep, self)

    def __len__(self) -> int:
        # |G/N| = |G| / |N|
        return len(self._group) // len(self._subgroup)

    def elements(self) -> Set[CosetElement]:
        """Возвращает множество всех смежных классов (элементы фактор-группы)."""
        seen: Set[CosetElement] = set()
        for g_el in self._group._all_elements():
            cos = CosetElement(g_el, self)
            seen.add(cos)
        return seen

    def contains(self, coset: CosetElement) -> bool:
        """Проверяет, принадлежит ли элемент этой фактор-группе."""
        return isinstance(coset, CosetElement) and coset.group is self

    def is_lagrangian(self) -> bool:
        """Для конечных фактор-групп теорема Лагранжа выполняется."""
        return True

    def is_abelian(self) -> bool:
        """G/N абелева тогда и только тогда, когда G' ⊆ N."""
        comm = self._group.comutator()
        return comm.is_subgroup(self._subgroup)

    def is_simple(self) -> bool:
        """G/N проста тогда и только тогда, когда N максимально нормальна в G."""
        # Проверяем, нет ли ненулевых нормальных подгрупп между N и G
        for H in self._group.subgroups():
            if H.is_normal() and H != self._subgroup and H != self._group and self._subgroup.is_subgroup(
                    H):
                return False
        return True

    def is_solvable(self) -> bool:
        """Фактор разрешим, если G разрешима."""
        return self._group.is_solvable()

    def comutator(self) -> CosetElement:
        """Коммутант фактор-группы: (G' N)/N."""
        comm = self._group.comutator()  # SubGroup G'
        # Объединяем G' и N
        H = SubGroup.generated_by(
            chain(comm.elements(), self._subgroup.elements()), self._group)
        return FactorGroup(self._group,
                           H).subgroup  # возвращаем подгруппу коммутатора фактор-группы

    def center(self) -> SubGroup[CosetElement]:
        """Центр фактор-группы: { gN | g x g' ∈ N ∀ g' ∈ G }."""

        def predicate(cos: CosetElement) -> bool:
            for g_el in self._group._all_elements():
                lhs = cos.representative
                rhs = self._group.op(g_el, cos.representative)
                if self._group.op(lhs,
                                  g_el.inv()) not in self._subgroup.elements():
                    return False
            return True

        return SubGroup.from_predicate(predicate, self)

    def __repr__(self) -> str:
        return f"FactorGroup({self._group!r}, {self._subgroup!r})"

    def __getitem__(self, item):
        return CosetElement(self._group[item], self)
