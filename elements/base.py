from __future__ import annotations

from abc import ABC, abstractmethod


class Element[T](ABC):
    """
    Абстрактный интерфейс для элемента группы.

    Любой конкретный элемент
    должен наследовать этот интерфейс и реализовать базовые операции.
    """

    @property
    @abstractmethod
    def value(self) -> T:
        """
        Внутреннее представление элемента.

        Returns:
            T: Типизированное значение, например int, tuple или numpy.ndarray.
        """
        ...

    @property
    @abstractmethod
    def group(self) -> Group[T, Element]:  # type: ignore[name-defined]
        """
        Ссылка на объект группы, к которой принадлежит данный элемент.

        Returns:
            Group[T, Element]: Экземпляр группы данного элемента.
        """
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Проверка равенства двух элементов одной группы.

        Args:
            other (object): Другой объект для сравнения.

        Returns:
            bool: True, если элементы равны в контексте одной группы.
        """
        ...

    @abstractmethod
    def __mul__(self, other: Element[T]) -> Element[T]:
        """
        Групповая операция умножения (композиции) двух элементов.

        Args:
            other (Element[T]): Элемент той же группы.

        Returns:
            Element[T]: Результат операции a * b.
        """
        ...

    @abstractmethod
    def __pow__(self, exponent: int) -> Element[T]:
        """
        Возведение элемента в целую степень.

        Args:
            exponent (int): Целая степень, положительная или отрицательная.

        Returns:
            Element[T]: Результат a ** n.
        """
        ...

    @abstractmethod
    def inv(self) -> Element[T]:
        """
        Получение обратного (инверсного) элемента.

        Returns:
            Element[T]: Обратный элемент, удовлетворяющий a * a.inv() == identity.
        """
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """
        Строковое представление элемента для отладки.

        Returns:
            str: Человекочитаемый формат описания элемента.
        """
        ...

    @abstractmethod
    def __hash__(self) -> int:
        """
        Хэш функции, позволяющий использовать элемент в множествах или в качестве ключа словаря.

        Returns:
            int: Целочисленный хэш этого элемента.
        """
        ...

