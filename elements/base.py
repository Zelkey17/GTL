from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Element(ABC, Generic[T]):
    """
    Абстрактный интерфейс для элемента группы.

    Любой конкретный элемент
    должен наследовать этот интерфейс и реализовать базовые операции.
    """

    @property
    @abstractmethod
    def value(self) -> T:
        """Внутреннее представление элемента (например, int, tuple, numpy.ndarray)."""
        ...

    @property
    @abstractmethod
    def group(self) -> Group[T, Element]:  # type: ignore[name-defined]
        """Ссылка на группу, к которой принадлежит элемент."""
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Проверка равенства двух элементов той же группы."""
        ...

    @abstractmethod
    def __mul__(self, other: Element[T]) -> Element[T]:
        """Групповая операция: a * b (элементы одной группы)."""
        ...

    @abstractmethod
    def __pow__(self, exponent: int) -> Element[T]:
        """Возведение элемента в целую степень: a ** n."""
        ...

    @abstractmethod
    def inv(self) -> Element[T]:
        """Обратный элемент: a.inv() такое, что a * a.inv() == identity."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Строковое представление элемента (для отладки)."""
        ...
