from __future__ import annotations

from typing import Set
from elements.base import Element
from groups.Factor import FactorGroup




class CosetElement[E](Element[Set[E]]):
    """
    Элемент фактор‑группы G/N, представленный левым смежным классом aN.

    Смежный класс aN = { n · a | n ∈ N }, где N — нормальная подгруппа G.
    Представитель (_rep) — элемент a из G, а _factor_group — экземпляр FactorGroup(G, N).

    Attributes:
        _rep (E): Представитель смежного класса.
        _factor_group (FactorGroup[E]): Фактор‑группа, которой принадлежит элемент.
    """

    def __init__(self, representative: E, factor_group: FactorGroup[E]):
        """
        Инициализирует элемент фактор‑группы.

        Args:
            representative (E): Элемент G, задающий класс aN.
            factor_group (FactorGroup[E]): Фактор‑группа G/N.

        """
        self._rep = representative
        self._factor_group = factor_group

    @property
    def representative(self) -> E:
        """
        Представитель смежного класса.

        Returns:
            E: Элемент G, выбранный в качестве репрезентанта класса.
        """
        return self._rep

    @property
    def value(self) -> Set[E]:
        """
        Все элементы смежного класса aN.

        Вычисляется как {n * a | n ∈ N.elements()}.

        Returns:
            Set[E]: Набор элементов G, составляющих класс aN.
        """
        # N — нормальная подгруппа
        N = self._factor_group._subgroup
        G = self._factor_group._group
        # строим множество n · a
        return {G.op(n, self._rep) for n in N.elements()}

    @property
    def group(self) -> FactorGroup[E]:
        """
        Фактор‑группа, которой принадлежит элемент.

        Returns:
            FactorGroup[E]: Экземпляр G/N.
        """
        return self._factor_group

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает два смежных класса aN и bN.

        Классы равны ⇔ b⁻¹·a ∈ N.

        Args:
            other (object): Другой CosetElement для сравнения.

        Returns:
            bool: True, если классы совпадают.

        Raises:
            TypeError: Если other не CosetElement или не из той же фактор‑группы.
        """
        if not isinstance(other, CosetElement) or self.group is not other.group:
            raise TypeError("Несовместимые элементы для сравнения в фактор‑группе")
        N = self._factor_group._subgroup
        # проверяем, что b⁻¹ * a лежит в N
        diff = other._rep.inv() * self._rep
        return N.contains(diff)

    def __mul__(self, other: CosetElement[E]) -> CosetElement[E]:
        """
        Умножение смежных классов: (aN)·(bN) = (a·b)N.

        Args:
            other (CosetElement[E]): Другой смежный класс.

        Returns:
            CosetElement[E]: Класс (a·b)N.

        Raises:
            TypeError: Если other не CosetElement или не из той же фактор‑группы.
        """
        if not isinstance(other, CosetElement) or self.group is not other.group:
            raise TypeError("Несовместимые элементы для умножения в фактор‑группе")
        # умножаем представителей a·b
        prod_rep = self._factor_group._group.op(self._rep, other._rep)
        return CosetElement(prod_rep, self._factor_group)

    def __pow__(self, exponent: int) -> CosetElement[E]:
        """
        Возведение класса в целую степень: (aN)^k = (a^k)N.

        Args:
            exponent (int): Показатель степени (целое число).

        Returns:
            CosetElement[E]: Класс a^k N.
        """
        # используем pow() группы G
        pow_rep = self._factor_group._group.pow(self._rep, exponent)
        return CosetElement(pow_rep, self._factor_group)

    def inv(self) -> CosetElement[E]:
        """
        Обратный смежный класс: (aN)⁻¹ = a⁻¹N.

        Returns:
            CosetElement[E]: Класс inverse(a) N.
        """
        inv_rep = self._factor_group._group.inverse(self._rep)
        return CosetElement(inv_rep, self._factor_group)

    def __repr__(self) -> str:
        """
        Читаемое представление элемента.

        Returns:
            str: Строка вида "Coset(aN)".
        """
        return f"Coset({self._rep!r}N)"

    def __hash__(self) -> int:
        """
        Хэш на основе представителя.

        Гарантирует, что одинаковые классы дают одинаковый hash.

        Returns:
            int: Хэш от представителя.
        """
        return hash(self._rep)
