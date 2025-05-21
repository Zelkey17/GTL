from itertools import chain
from typing import Set, TypeVar

from elements.base import Element
from elements.coset import CosetElement
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup

E = TypeVar("E", bound=Element)

class FactorGroup[E](FiniteGroup[set[E], CosetElement[E]]):
    """
    Класс для представления фактор-группы G/N,
    где G — конечная группа, а N — её нормальная подгруппа.
    Элементы фактор-группы — смежные классы.
    """

    def __contains__(self, item: CosetElement[E]) -> bool:
        """
        Проверяет, принадлежит ли смежный класс фактор-группе.

        :param item: Смежный класс.
        :return: True, если это корректный элемент этой фактор-группы.
        """
        return isinstance(item, CosetElement) and item.group is self

    def __iter__(self) -> Iterator[CosetElement[E]]:
        """
        Итератор по представителям смежных классов G/N.

        :return: Итератор по элементам фактор-группы.
        """
        seen_reprs = set()
        for g in self._group:
            repr_coset = CosetElement(g, self)
            # Используем set, чтобы избежать дубликатов
            if repr_coset not in seen_reprs:
                seen_reprs.add(repr_coset)
                yield repr_coset


    def __init__(self, group: FiniteGroup, subgroup: SubGroup[E]):
        """
        Инициализирует фактор-группу по группе и её нормальной подгруппе.

        :param group: Исходная конечная группа G.
        :param subgroup: Нормальная подгруппа N ⊴ G.
        :raises ValueError: Если подгруппа не принадлежит группе или не является нормальной.
        """
        if subgroup.group is not group:
            raise ValueError("Подгруппа должна принадлежать указанной группе")
        if not subgroup.is_normal():
            raise ValueError("Подгруппа должна быть нормальной для построения фактор-группы")
        self._group = group
        self._subgroup = subgroup

    def identity(self) -> CosetElement:
        """
        Возвращает нейтральный элемент фактор-группы (N).
        """
        return CosetElement(self._group.identity(), self)

    def op(self, a: CosetElement, b: CosetElement) -> CosetElement:
        """
        Операция умножения в фактор-группе:
        (aN)(bN) = (ab)N.

        :param a: Элемент фактор-группы.
        :param b: Элемент фактор-группы.
        :return: Результат произведения в фактор-группе.
        """
        if a.group is not self or b.group is not self:
            raise ValueError("Элемент из другой группы")
        prod_rep = self._group.op(a.representative, b.representative)
        return CosetElement(prod_rep, self)

    def inverse(self, a: CosetElement) -> CosetElement:
        """
        Возвращает обратный элемент к заданному в фактор-группе.

        :param a: Элемент фактор-группы.
        :return: Обратный элемент.
        """
        inv_rep = self._group.inverse(a.representative)
        return CosetElement(inv_rep, self)

    def __len__(self) -> int:
        """
        Возвращает порядок фактор-группы: |G/N| = |G| / |N|.
        """
        return len(self._group) // len(self._subgroup)

    def elements(self) -> Set[CosetElement]:
        """
        Возвращает множество всех различных смежных классов G по N.

        :return: Множество элементов фактор-группы.
        """
        seen: Set[CosetElement] = set()
        for g_el in self._group._all_elements():
            cos = CosetElement(g_el, self)
            seen.add(cos)
        return seen

    def contains(self, coset: CosetElement) -> bool:
        """
        Проверяет, принадлежит ли заданный элемент этой фактор-группе.

        :param coset: Кандидат на элемент фактор-группы.
        :return: True, если принадлежит, иначе False.
        """
        return isinstance(coset, CosetElement) and coset.group is self

    def is_lagrangian(self) -> bool:
        """
        Теорема Лагранжа всегда выполняется для конечных групп.

        :return: True
        """
        return True

    def is_abelian(self) -> bool:
        """
        Проверяет, является ли фактор-группа абелевой.

        :return: True, если G' ⊆ N, иначе False.
        """
        comm = self._group.comutator()
        return comm.is_subgroup(self._subgroup)

    def is_simple(self) -> bool:
        """
        Проверяет, является ли фактор-группа простой.
        G/N проста ⟺ N — максимально нормальная подгруппа в G.

        :return: True, если проста, иначе False.
        """
        for H in self._group.subgroups():
            if H.is_normal() and H != self._subgroup and H != self._group and self._subgroup.is_subgroup(H):
                return False
        return True

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость фактор-группы.

        :return: True, если G разрешима, иначе False.
        """
        return self._group.is_solvable()

    def comutator(self) -> SubGroup:
        """
        Возвращает коммутант фактор-группы: (G' * N) / N.

        :return: Подгруппа в фактор-группе, соответствующая (G' * N) / N.
        """
        comm = self._group.comutator()
        combined = SubGroup.generated_by(
            chain(comm.elements(), self._subgroup.elements()), self._group)
        return FactorGroup(self._group, combined).subgroup

    def center(self) -> SubGroup[CosetElement]:
        """
        Центр фактор-группы: элементы gN такие, что ∀g'∈G: g g' g⁻¹ g'⁻¹ ∈ N.

        :return: Подгруппа центра в фактор-группе.
        """
        def predicate(cos: CosetElement) -> bool:
            for g_el in self._group._all_elements():
                lhs = cos.representative
                rhs = self._group.op(g_el, cos.representative)
                if self._group.op(lhs, g_el.inv()) not in self._subgroup.elements():
                    return False
            return True

        return SubGroup.from_predicate(predicate, self)

    def __repr__(self) -> str:
        """
        Представление объекта: FactorGroup(G, N)
        """
        return f"FactorGroup({self._group!r}, {self._subgroup!r})"

    def __getitem__(self, item) -> CosetElement:
        """
        Возвращает смежный класс по представителю.

        :param item: Элемент исходной группы.
        :return: Смежный класс, содержащий item.
        """
        return CosetElement(self._group[item], self)
