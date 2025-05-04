from finite_group import FiniteGroup
from elements.permutation_element import PermutationElement
import math


class SymmetricGroup(FiniteGroup):

    def __init__(self, rank: int):
        if rank <= 0:
            raise Exception("Ранг группы положительное число")
        self._rank = rank

    def identity(self) -> list[int]:
        return list(range(1, self._rank + 1))

    def op(self, a: PermutationElement,
                 b: PermutationElement) -> PermutationElement:
        perm = [b._value[a._value[i]] for i in range(0, self._rank)]
        return PermutationElement(perm, self)

    @abstractmethod
    def inverse(self, a: E) -> E:
        """Обратный элемент: inverse(a) такое, что op(a, inverse(a)) == identity."""
        ...

    def multiply(self, *elements: E) -> E:
        """
        Последовательное умножение: a1 * a2 * ... * an.
        Если нет аргументов, возвращает identity().
        """
        result = self.identity()
        for el in elements:
            if el.group is not self:
                raise ValueError("Элемент из другой группы")
            result = self.op(result, el)
        return result

    def pow(self, a: E, exponent: int) -> E:
        """
        Быстрое возведение элемента в степень (алгоритм двоичного возведения).
        Поддерживает отрицательные степени через inverse().
        """
        if exponent == 0:
            return self.identity()
        base = a
        exp = exponent
        if exp < 0:
            base = self.inverse(a)
            exp = -exp
        result = self.identity()
        while exp:
            if exp & 1:
                result = self.op(result, base)
            base = self.op(base, base)
            exp >>= 1
        return result

    @abstractmethod
    def is_lagrangian(self) -> bool:
        """
        Проверяет, является ли группа лагранжевой

        Группа называется «лагранжевой», если для каждого делителя её порядка существует
        хотя бы одна подгруппа такого порядка.

        Returns:
            bool: True, если группа удовлетворяет обратной теореме Лагранжа,
                False в иначе.
        """

    @abstractmethod
    def is_abelian(self) -> bool:
        """
        Проверяет, является ли группа абелевой (коммутативной).

        Returns:
            bool: True, если группа абелева, False в противном случае.
        """

    @abstractmethod
    def is_simple(self) -> bool:
        """
        Проверяет, является ли группа простой.

        Группа называется простой, если у неё нет нетривиальных нормальных подгрупп
        (т.е. только тривиальная подгруппа и сама группа).

        Returns:
            bool: True, если группа простая, False в противном случае.
        """

    @abstractmethod
    def is_solvable(self) -> bool:
        """
        Проверяет, является ли группа разрешимой.

        Группа называется разрешимой, если существует субнормальный ряд,
        все фактор-группы которого абелевы. Эквивалентно, её производный ряд
        достигает тривиальной подгруппы.

        Returns:
            bool: True, если группа разрешима, False в противном случае.
        """

    def __len__(self) -> int:
        return math.factorial(self._rank)

    @abstractmethod
    def comutator(self) -> "SubGroup":
        """
        Вычисляет коммутант группы (подгруппу, порождённую коммутаторами).

        Коммутант — это подгруппа, порождённая всеми элементами вида [a, b] = a*b*a^{-1}*b^{-1},
        где a и b принадлежат группе.

        Returns:
            SubGroup: Коммутант данной группы.
        """

    @abstractmethod
    def center(self) -> "SubGroup":
        """
        Вычисляет центр группы.

        Центр — это множество элементов, которые коммутируют со всеми элементами группы.

        Returns:
            SubGroup: Центр группы.
        """

    @abstractmethod
    def __getitem__(self, item: T) -> E:
        ...

    @abstractmethod
    def __contains__(self, item: E) -> bool:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[E]:
        ...
