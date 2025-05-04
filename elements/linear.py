from __future__ import annotations

import numpy as np

from elements.base import Element
from groups.base import Group


class MatrixElement(Element[np.ndarray]):
    """
    Элемент группы матриц над numpy.ndarray.

    Реализует интерфейс `Element[np.ndarray]`, где операции
    (умножение, возведение в степень, взятие обратного) выполняются
    согласно правилам, заданным связанной группой.

    Attributes:
        _matrix (np.ndarray): Внутреннее представление матрицы.
        _reference_to_group (Group[np.ndarray, MatrixElement]):
            Группа, управляющая операциями над матрицами.
    """

    def __init__(
            self,
            matrix: np.ndarray,
            reference_to_group: Group[np.ndarray, MatrixElement]
    ):
        """
        Инициализирует новый элемент-матрицу.

        Args:
            matrix (np.ndarray): Двумерный массив, представляющий матрицу.
            reference_to_group (Group[np.ndarray, MatrixElement]):
                Ссылка на группу, реализующую операции над матрицами.

        Raises:
            TypeError: Если matrix не является np.ndarray.
        """
        if not isinstance(matrix, np.ndarray):
            raise TypeError("matrix must be a numpy.ndarray")
        self._matrix = matrix
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> np.ndarray:
        """
        Внутреннее значение элемента.

        Returns:
            np.ndarray: Массив, хранящий данные матрицы.
        """
        return self._matrix

    @property
    def group(self) -> Group[np.ndarray, MatrixElement]:
        """
        Группа, к которой принадлежит данный элемент.

        Returns:
            Group[np.ndarray, MatrixElement]: Экземпляр группы.
        """
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает две матрицы на равенство.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True, если other — MatrixElement той же группы
                  и матрицы идентичны поэлементно.

        Raises:
            TypeError: Если other не является Element или принадлежит другой группе.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return np.array_equal(self._matrix, other.value)

    def __mul__(self, other: MatrixElement) -> MatrixElement:
        """
        Групповая операция над матрицами (делегируется группе).

        Args:
            other (MatrixElement): Элемент той же группы.

        Returns:
            MatrixElement: Результат op(self, other) из связанной группы.

        Raises:
            TypeError: Если other не является Element или принадлежит другой группе.
        """
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> MatrixElement:
        """
        Быстрое возведение матрицы в целую степень.

        Аргумент modulo игнорируется (для совместимости с сигнатурой Python).

        Args:
            power (int): Показатель степени.
            modulo: Не используется.

        Returns:
            MatrixElement: Результат pow(self, power) из связанной группы.
        """
        return self._reference_to_group.pow(self, power)

    def inv(self) -> MatrixElement:
        """
        Возвращает обратный к матрице элемент.

        Делегирует операцию inverse() связанной группе.

        Returns:
            MatrixElement: Обратная матрица.
        """
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        """
        Человеко‑читаемое представление элемента.

        Returns:
            str: Строка, содержащая repr(self._matrix) с префиксом.
        """
        return "Matrix:\n" + repr(self._matrix)

    def __hash__(self) -> int:
        """
        Позволяет использовать элемент в множествах и ключах словарей.

        Хэшируется по байтовому представлению массива.

        Returns:
            int: Хэш от tobytes() матрицы.
        """
        return hash(self._matrix.tobytes())
