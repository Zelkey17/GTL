from __future__ import annotations

from typing import Set, Callable, Iterable
from itertools import product


class SubGroup[E,G]:
    """
    Класс, представляющий подгруппу конечной группы G.

    Подгруппа определяется как непустое множество, замкнутое относительно
    групповой операции и обращения, и содержащее нейтральный элемент.
    """

    def __init__(self, group: G, elements: Set[E]):
        self._group = group
        self._elements = set(elements)
        self._validate()

    @property
    def group(self) -> G:
        """Возвращает родительскую группу G."""
        return self._group

    def elements(self) -> Set[E]:
        """Возвращает все элементы подгруппы."""
        return set(self._elements)

    def to_group(self) -> CustomGroup[T]:
        """
        Преобразует подгруппу в новый CustomGroup, используя «сырые» значения элементов и операции родительской группы.
        """
        # Собираем значения элементов подгруппы
        raw_values = [el.value for el in self._elements]
        # Присваиваем уникальные имена через индексы
        index = {str(i): raw_values[i] for i in range(len(raw_values))}

        # Операция, ограниченная на подгруппу
        def op(a: T, b: T) -> T:
            elem_a = CustomElement(a, self._group)
            elem_b = CustomElement(b, self._group)
            return self._group.op(elem_a, elem_b).value

        # Обратный элемент
        def inv(a: T) -> T:
            elem = CustomElement(a, self._group)
            return self._group.inverse(elem).value

        return CustomGroup(index, op, inv, verify=True)

    @classmethod
    def as_subgroup(cls, candidate: FiniteGroup[type_T, E], group: G) -> SubGroup[E, G]:
        """
        Конструирует SubGroup, рассматривая все элементы candidate как подмножество group.
        Проверяет, что каждое значение элемента candidate присутствует в group.
        """
        elems: Set[E] = set()
        for el in candidate:
            # пытаемся получить соответствующий элемент в целевой группе по значению
            try:
                target = group[el.value]
            except (KeyError, AttributeError):
                # альтернативный поиск по совпадению значения
                target = next((g_el for g_el in group if g_el.value == el.value), None)
            if target is None:
                raise ValueError(f"Элемент {el.value!r} не найден в целевой группе")
            elems.add(target)
        return cls(group, elems)

    def contains(self, element: E) -> bool:
        """Проверяет, содержится ли элемент в подгруппе."""
        return element in self._elements and element.group is self._group

    def is_subgroup(self, other: SubGroup[E, G]) -> bool:
        """Проверяет, является ли self подгруппой other."""
        return self._group is other._group and self._elements.issubset(other._elements)

    def is_normal(self) -> bool:
        """
        Проверяет, является ли подгруппа нормальной:
        ∀ g ∈ G, ∀ h ∈ H: g * h * g⁻¹ ∈ H.
        """
        for g in self._group:
            for h in self._elements:
                conjugate = self._group.op(g, self._group.op(h, self._group.inverse(g)))
                if conjugate not in self._elements:
                    return False
        return True

    @classmethod
    def generated_by(cls, generators: Iterable[E], group: G) -> SubGroup[E,G]:
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
                    new_elems.add(inv)
            if new_elems != elems:
                elems = new_elems
                changed = True
        return cls(group, elems)

    @classmethod
    def from_predicate(cls, predicate: Callable[[E], bool], group: G) -> SubGroup[E,G]:
        """
        Строит подгруппу по предикату (предикат должен задавать подгруппу).
        """
        elems = {el for el in group if predicate(el)}
        return cls(group, elems)

    @classmethod
    def trivial_identity(cls, group: G) -> SubGroup[E,G]:
        """Возвращает тривиальную подгруппу {e}."""
        return cls(group, {group.identity()})

    @classmethod
    def trivial_all(cls, group: G) -> SubGroup[E,G]:
        """Подгруппа, совпадающая с самой группой."""
        return cls(group, set(group))

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
