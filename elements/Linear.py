import numpy as np

from elements.base import Element


class MatrixElement(Element[np.ndarray]):
    def __init__(self, matrix: np.ndarray,
                 reference_to_group: 'Group[np.ndarray, MatrixElement]'):
        if not isinstance(matrix, np.ndarray):
            raise TypeError("matrix must be a numpy.ndarray")
        self._matrix = matrix
        self._reference_to_group = reference_to_group

    @property
    def value(self) -> np.ndarray:
        return self._matrix

    @property
    def group(self) -> "Group[np.ndarray, MatrixElement]":
        return self._reference_to_group

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для сравнения")
        return np.array_equal(self._matrix, other.value)

    def __mul__(self, other: 'MatrixElement') -> 'MatrixElement':
        if not isinstance(other, Element) or self.group != other.group:
            raise TypeError("Несовместимые элементы для умножения")
        return self._reference_to_group.op(self, other)

    def __pow__(self, power: int, modulo=None) -> 'MatrixElement':
        return self._reference_to_group.pow(self, power)

    def inv(self) -> 'MatrixElement':
        return self._reference_to_group.inverse(self)

    def __repr__(self) -> str:
        return "Matrix:\n" + repr(self._matrix)

    def __hash__(self):
        return hash(self._matrix.tobytes())
