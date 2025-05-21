from itertools import permutations
from typing import Optional, Dict
from groups.finite_group import FiniteGroup

def is_isomorphic[G1, G2, E1, E2](group1: FiniteGroup[E1, G1], group2: FiniteGroup[E2, G2]) -> Optional[Dict[E1, E2]]:
    """
    Проверяет, изоморфны ли две конечные группы.
    Если да — возвращает отображение из group1 в group2, сохраняющее операцию.
    Если нет — возвращает None.

    Предполагается, что элементы групп сравним по равенству и имеют корректную хеш-функцию.
    """
    if len(group1) != len(group2):
        return None

    elems1 = list(group1)
    elems2 = list(group2)

    # Перебираем все биекции между множествами элементов
    for perm in permutations(elems2):
        mapping = dict(zip(elems1, perm))
        # Проверим, сохраняет ли операция: φ(a * b) == φ(a) * φ(b)
        valid = True
        for a in elems1:
            for b in elems1:
                lhs = mapping[group1.op(a, b)]
                rhs = group2.op(mapping[a], mapping[b])
                if lhs != rhs:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            return mapping
    return None