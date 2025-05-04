from itertools import product
from typing import Iterator
from sympy.combinatorics import Permutation

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
        perm = [b.value[a.value[i] - 1] for i in range(0, self._rank)]
        return PermutationElement(perm, self)

    def inverse(self, a: PermutationElement) -> PermutationElement:
        b = list(range(self._rank))
        perm = [0] * self._rank
        for i in range(self._rank):
            perm[a.value[i] - 1] = i + 1
        return PermutationElement(perm, self)

    def is_lagrangian(self) -> bool:
        return self._rank <= 5

    def is_abelian(self) -> bool:
        return self._rank <= 3

    def is_simple(self) -> bool:
        return self._rank != 4

    def is_solvable(self) -> bool:
        return self._rank <= 4

    def __len__(self) -> int:
        return (math.factorial(self._rank) + 1) // 2

    def commutator(self) -> SubGroup[PermutationElement]:
        if self._rank <= 3:
            return SubGroup.trivial_identity(self)
        elif self._rank > 4:
            return SubGroup.trivial_all(self)
        else:
            ...#TODO

    def center(self) -> SubGroup[PermutationElement]:
        if self._rank <= 3:
            return SubGroup.trivial_all(self)
        else:
            return SubGroup.trivial_identity(self)

    def __getitem__(self, item: list[int] | list[
        tuple[int]] | str) -> PermutationElement:

        def check_correct(permut):
            temp_perm = sorted(permut)
            if not temp_perm == list(range(1, self._rank + 1)):
                raise Exception("Перестановка не корректна")
            p_perm = Permutation(permut)
            if not p_perm.is_even:
                raise Exception("Перестановка нечётна")

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
        return item.group == self

    def __iter__(self) -> Iterator[PermutationElement]:
        return (self[list(per)] for per in
                product(list(range(1, self._rank + 1)), repeat=self._rank) if
                len(set(per)) == self._rank and Permutation(list(per)).is_even())
