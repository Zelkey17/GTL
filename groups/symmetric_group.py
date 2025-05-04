from itertools import product
from typing import Iterator

from elements.permutation_parser import PermutationParser
from elements.permutation_element import PermutationElement
import math

from groups.Subgroup import SubGroup
from groups.finite_group import FiniteGroup


class SymmetricGroup(FiniteGroup):

    def __init__(self, rank: int):
        if rank <= 0:
            raise Exception("Ранг группы положительное число")
        self._rank = rank

    def identity(self) -> list[int]:
        return list(range(1, self._rank + 1))

    def op(self, a: PermutationElement,
           b: PermutationElement) -> PermutationElement:
        perm = [b._value[a._value[i] - 1] for i in range(0, self._rank)]
        return PermutationElement(perm, self)

    def inverse(self, a: PermutationElement) -> PermutationElement:
        b = list(range(self._rank))
        perm = [0] * self._rank
        for i in range(self._rank):
            perm[a._value[i] - 1] = i + 1
        return PermutationElement(perm, self)

    def is_lagrangian(self) -> bool:
        return self._rank <= 4

    def is_abelian(self) -> bool:
        return self._rank <= 2

    def is_simple(self) -> bool:
        return self._rank <= 2

    def is_solvable(self) -> bool:
        return self._rank <= 4

    def __len__(self) -> int:
        return math.factorial(self._rank)

    def comutator(self) -> SubGroup[PermutationElement]:
        ...  # TODO

    def center(self) -> SubGroup[PermutationElement]:
        if self._rank <= 2:
            return SubGroup.trivial_all(self)
        else:
            return SubGroup.trivial_identity(self)

    def __getitem__(self, item: list[int] | list[
        tuple[int]] | str) -> PermutationElement:

        def check_correct(perm):
            temp_perm = sorted(perm)
            if not temp_perm == list(range(1, self._rank + 1)):
                raise Exception("Перестановка не корректна")

        def list_of_tuple_perm_parse(perm) -> PermutationElement:
            temp_perm = list(range(1, self._rank + 1))
            perm_stat = list(range(1, self._rank + 1))
            for e in perm:
                if not len(set(e)) == len(e):
                    raise Exception("Перестановка не корректна")
                for i in range(0, len(e)):
                    print(temp_perm)
                    temp_perm[e[(i + 1) % len(e)] - 1] = perm_stat[e[i] - 1]
                    print(temp_perm)
            print(temp_perm)
            check_correct(temp_perm)
            return PermutationElement(temp_perm, self)

        if isinstance(item, list) and all(isinstance(e, int) for e in item):
            check_correct(item)
            return PermutationElement(item, self)
        elif (isinstance(item, list) and all(
                isinstance(e, tuple) for e in item) and all(
            all(isinstance(x, int) for x in e) for e in item)):
            return list_of_tuple_perm_parse(item)
        elif isinstance(item, str):
            parser = PermutationParser()
            perm = parser.parse(item)
            return list_of_tuple_perm_parse(perm)
        else:
            raise Exception("Неверный формат индекса")

    def __contains__(self, item: PermutationElement) -> bool:
        return item._reference_to_group == self

    def __iter__(self) -> Iterator[PermutationElement]:
        return (self[list(per)] for per in
                product(list(range(1, self._rank + 1)), repeat=self._rank) if
                len(set(per)) == self._rank)
