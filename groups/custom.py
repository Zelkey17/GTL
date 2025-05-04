from copy import deepcopy
from typing import Callable, Dict, Iterator, TypeVar, Generic

from elements.custom import CustomElement
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup

I = TypeVar("I")  # Тип ключа в словаре index


class CustomGroup[T]( FiniteGroup[T, CustomElement[T]]):
    """
    Конечная группа, построенная на пользовательских элементах с поддержкой проверки аксиом группы.

    Аргументы конструктора:
        index: отображение индексов (имен) на элементы группы.
        op: бинарная операция группы.
        inv: функция, возвращающая обратный элемент.
        verify: если True — проверяются аксиомы группы.
    """

    def __init__(self, index: Dict[I, T], op: Callable[[T, T], T],
                 inv: Callable[[T], T], verify=False):
        e = None
        if verify:
            if index is None or len(index) == 0:
                raise Exception("Group size must not be positive number")

            e = list(index.items())[0][1]
            e = op(inv(e), e)

            for ind1, el1 in index.items():
                for ind2, el2 in index.items():
                    # Проверка ассоциативности
                    for ind3, el3 in index.items():
                        if op(el1, op(el2, el3)) != op(op(el1, el2), el3):
                            raise Exception("Not associative")
                    # Проверка замкнутости
                    if op(el1, el2) not in index.values():
                        raise Exception("Not closed")

                # Проверка существования единицы и обратного
                if not (op(el1, e) == el1 and op(el1, inv(el1)) == e and
                        op(e, el1) == el1 and op(inv(el1), el1) == e and
                        inv(el1) in list(index.values())):
                    raise Exception("Incorrect inverse for element")

        if e is None:
            e = list(index.items())[0][1]
            e = op(inv(e), e)

        self._index = deepcopy(index)
        self._op = deepcopy(op)
        self._inv = deepcopy(inv)
        self._id = e

    def __iter__(self) -> Iterator[CustomElement[T]]:
        """Итерирует по всем элементам группы."""
        return (CustomElement(i, self) for i in self._index.values())

    def __contains__(self, item: CustomElement[T]) -> bool:
        """Проверяет, принадлежит ли элемент данной группе."""
        return item.group == self

    def identity(self) -> CustomElement[T]:
        """Возвращает единичный элемент группы."""
        return CustomElement(self._id, self)

    def op(self, a: CustomElement[T], b: CustomElement[T]) -> CustomElement[T]:
        """Групповая операция над двумя элементами."""
        return CustomElement(self._op(a.value, b.value), self)

    def inverse(self, a: CustomElement[T]) -> CustomElement[T]:
        """Возвращает обратный элемент."""
        return CustomElement(self._inv(a.value), self)

    def __len__(self) -> int:
        """Возвращает порядок группы."""
        return len(self._index)

    def is_lagrangian(self) -> bool:
        """Проверяет, удовлетворяет ли группа теореме Лагранжа (заглушка)."""
        return True  # TODO: реализовать

    def is_abelian(self) -> bool:
        """Проверяет, коммутативна ли группа."""
        for el in self._index.values():
            for el2 in self._index.values():
                if self._op(el, el2) != self._op(el2, el):
                    return False
        return True

    def is_simple(self) -> bool:
        """Проверяет, является ли группа простой (заглушка)."""
        return True  # TODO: реализовать

    def is_solvable(self) -> bool:
        """Проверяет, является ли группа разрешимой (заглушка)."""
        return True  # TODO: реализовать

    def comutator(self) -> SubGroup:
        """Возвращает коммутаторную подгруппу (заглушка)."""
        return SubGroup.trivial_identity(self)  # TODO

    def center(self) -> SubGroup:
        """Возвращает центр группы (заглушка)."""
        return SubGroup.trivial_all(self)  # TODO

    def __getitem__(self, item: I) -> CustomElement[T]:
        """Получить элемент по ключу в словаре index."""
        return CustomElement(self._index[item], self)

    def _all_elements(self) -> list[T]:
        """Список всех элементов по значению (без обёртки CustomElement)."""
        return list(self._index.values())

    @classmethod
    def from_cayley(cls, table: list[list[T]], verify=False, index=None,
                    save_index=False):
        """
        Создаёт группу по таблице Кэли.

        Аргументы:
            table: таблица Кэли, представленная как список списков.
            verify: проверка аксиом группы.
            index: словарь переименования элементов.
            save_index: сохранить имена из `index`.
        """
        if index is not None and save_index:
            raise Exception("Cannot both save and override index")

        if len(table) == 0:
            raise Exception("Group size must not be positive number")
        n = len(table)

        # Проверка, что таблица Кэли — латинский квадрат
        if not all(len(set(i)) == n for i in table):
            raise Exception("Cayley table must be latin square")
        if not all(len({table[j][i] for j in range(n)}) == n for i in range(n)):
            raise Exception("Cayley table must be latin square")

        # Определяем индексы и декодер
        if index is None and save_index:
            index = {table[0][i]: table[0][i] for i in range(n)}
        elif index is None:
            index = {i: table[0][i] for i in range(n)}
        else:
            index = {index[i]: table[0][i] for i in range(n)}

        decode = {table[0][i]: i for i in range(n)}
        id = table[0][0]

        # Вычисляем обратные элементы
        inv_table = {
            el: table[0][
                [i for i in range(n) if table[decode[el]][i] == id][0]
            ]
            for el in index.values()
        }

        def op(el1: T, el2: T) -> T:
            return table[decode[el1]][decode[el2]]

        def inv(el: T) -> T:
            return inv_table[el]

        return cls(index, op, inv, verify=verify)

    @classmethod
    def from_operation(cls, elems: Dict[str, T],
                       op: Callable[[T, T], T],
                       inv: Callable[[T], T],
                       verify=False):
        """
        Построить группу по частичной операции и обратным, автоматически дополняя недостающие элементы.

        Аргументы:
            elems: начальные именованные элементы.
            op: бинарная операция.
            inv: функция обратного.
            verify: проверка аксиом группы.
        """
        n = len(elems)
        while True:
            elem = deepcopy(elems)
            for ind, el in elem.items():
                for ind2, el2 in elem.items():
                    res = op(el, el2)
                    if res not in elems.values():
                        elems[ind + ind2] = res
                inv_el = inv(el)
                if inv_el not in elems.values():
                    elems["(" + ind + ")^-1"] = inv_el
            if n == len(elems):
                break
            n = len(elems)
        return cls(elems, op, inv, verify=verify)
