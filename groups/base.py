from __future__ import annotations

from abc import ABC, abstractmethod

class Group[T, E](ABC):
    """
    Абстрактный интерфейс для группы.

    Конкретные группы должны реализовывать:
    - нейтральный элемент (identity),
    - групповую операцию (op),
    - нахождение обратного элемента (inverse).

    Методы multiply и pow предоставлены по умолчанию.
    """

    @abstractmethod
    def identity(self) -> E:
        """
        Возвращает нейтральный элемент группы.

        Returns:
            E: Элемент, который не изменяет другие при умножении (a * identity == a).
        """
        ...

    @abstractmethod
    def op(self, a: E, b: E) -> E:
        """
        Групповая операция: ассоциативное бинарное произведение двух элементов.

        Args:
            a (E): Первый элемент.
            b (E): Второй элемент.

        Returns:
            E: Результат a * b.
        """
        ...

    @abstractmethod
    def inverse(self, a: E) -> E:
        """
        Возвращает обратный к элементу элемент.

        Args:
            a (E): Элемент группы.

        Returns:
            E: Такой элемент b, что op(a, b) == identity().
        """
        ...

    def multiply(self, *elements: E) -> E:
        """
        Перемножает последовательность элементов: a1 * a2 * ... * an.

        Если аргументов нет, возвращает нейтральный элемент.

        Args:
            *elements (E): Последовательность элементов группы.

        Returns:
            E: Результат последовательного применения операции op.

        Raises:
            ValueError: Если хотя бы один элемент не принадлежит этой группе.
        """
        result = self.identity()
        for el in elements:
            if el.group is not self:
                raise ValueError("Элемент принадлежит другой группе")
            result = self.op(result, el)
        return result

    def pow(self, a: E, exponent: int) -> E:
        """
        Возводит элемент в целую степень с помощью бинарного (быстрого) алгоритма.

        Поддерживаются отрицательные степени через вызов inverse().

        Args:
            a (E): Элемент группы.
            exponent (int): Целое число (может быть отрицательным или нулём).

        Returns:
            E: Результат возведения элемента a в степень exponent.
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
