from __future__ import annotations

from abc import ABC, abstractmethod


class Group[T,E](ABC):
    """
    Абстрактный интерфейс для группы.

    Конкретные группы должны наследовать этот класс и реализовать его методы.
    """

    @abstractmethod
    def identity(self) -> E:
        """Нейтральный элемент группы."""
        ...

    @abstractmethod
    def op(self, a: E, b: E) -> E:
        """Групповая операция: a*b, ассоциативная."""
        ...

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
