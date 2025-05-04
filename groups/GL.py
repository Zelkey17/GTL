from __future__ import annotations

from itertools import product
from math import prod

import numpy as np
from sympy import isprime, Matrix

from elements.linear import MatrixElement
from groups.cyclic_group import CyclicGroup
from groups.finite_group import FiniteGroup
from groups.SL import SL
from groups.symmetric_group import SymmetricGroup


class GLnm(FiniteGroup[np.ndarray, MatrixElement]):
    """
    Общая линейная группа GL(n, m) – группа невырожденных n×n матриц
    над полем ℤ/mℤ под умножением.

    При создании для некоторых (n, m) возвращаются более простые реализации:
      - GL(2, 2) ≅ S₃ (симметрическая группа порядка 3!).
      - GL(1, p) для p‑простого ≅ Cₚ₋₁ (циклическая группа порядка p-1).

    Attributes:
        n (int): Размерность матриц (n×n).
        m (int): Модуль (порядок кольца ℤ/mℤ).
    """

    def __new__(cls, n: int, m: int):
        """
        Переопределяет создание объекта, чтобы вернуть специализированные группы.

        Args:
            n (int): Размерность матриц.
            m (int): Модуль.

        Returns:
            SymmetricGroup | CyclicGroup | GLnm: Специализированный экземпляр.
        """
        # GL(2, 2) изоморфна симметрической группе S3
        if n == 2 and m == 2:
            return SymmetricGroup(3)
        # GL(1, p) для простого p – циклическая группа порядка p-1
        if n == 1 and isprime(m):
            return CyclicGroup(m - 1)
        return super().__new__(cls)

    def __init__(self, n: int, m: int):
        """
        Инициализирует GL(n, m).

        Args:
            n (int): Размерность матриц (n > 0).
            m (int): Модуль (m > 1).

        Raises:
            ValueError: Если n <= 0 или m <= 1.
        """
        if n <= 0 or m <= 1:
            raise ValueError("n должно быть > 0, а m > 1")
        self.n = n
        self.m = m

    def identity(self) -> MatrixElement:
        """
        Нейтральный элемент – единичная матрица Iₙ по модулю m.

        Returns:
            MatrixElement: Единичная матрица.
        """
        I = np.eye(self.n, dtype=int) % self.m
        return MatrixElement(I, self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        """
        Умножение матриц по модулю m.

        Args:
            a (MatrixElement): Левая матрица.
            b (MatrixElement): Правая матрица.

        Returns:
            MatrixElement: (a @ b) mod m.
        """
        M = (a.value @ b.value) % self.m
        return MatrixElement(M, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        """
        Обратная матрица по модулю m.

        Args:
            a (MatrixElement): Матрица, для которой ищем обратную.

        Returns:
            MatrixElement: a⁻¹ mod m.

        Raises:
            ValueError: Если матрица не обратима по модулю m.
        """
        inv_list = Matrix(a.value.tolist()).inv_mod(self.m).tolist()
        M_inv = np.array(inv_list, dtype=int) % self.m
        return MatrixElement(M_inv, self)

    def __len__(self) -> int:
        """
        Порядок группы |GL(n,m)| = ∏_{i=0..n-1} (m^n - m^i).

        Returns:
            int: Число всех невырожденных n×n матриц.
        """
        return prod(self.m ** self.n - self.m ** i for i in range(self.n))

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        """
        Доступ к элементу по его массиву.

        Args:
            matrix (np.ndarray): Любой целочисленный массив n×n.

        Returns:
            MatrixElement: Нормализованный элемент в GL(n, m).

        Raises:
            ValueError: Если форма не (n,n) или det ≡ 0 (mod m).
        """
        M = np.array(matrix, dtype=int) % self.m
        if M.shape != (self.n, self.n):
            raise ValueError(f"Ожидается матрица формы {self.n}×{self.n}")
        if Matrix(M.tolist()).det() % self.m == 0:
            raise ValueError("Сингулярная матрица не принадлежит GL(n, m)")
        return MatrixElement(M, self)

    def is_abelian(self) -> bool:
        """
        Проверяет, абелева ли группа.

        GL(n,m) абелева только при n=1.

        Returns:
            bool: True, если n == 1.
        """
        return self.n == 1

    def is_simple(self) -> bool:
        """
        Проверяет, простая ли группа.

        Для n ≥ 2 общая линейная группа не проста.
        Для n = 1 возвращает True, когда m-1 простое.

        Returns:
            bool: True, если простая.
        """
        if self.n >= 2:
            return False
        return isprime(self.m - 1)

    def is_lagrangian(self) -> bool:
        """
        Проверяет обратную теорему Лагранжа.

        Для n = 1 это циклическая группа, иначе не гарантируется.

        Returns:
            bool: True, если n == 1.
        """
        return self.n == 1

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость группы.

        GL(1,m) – абелева → разрешима.
        GL(2,2) = S3 – разрешима.
        Во всех остальных случаях не гарантируется.

        Returns:
            bool: True только для (n=1) или (n=2, m=2).
        """
        return self.n == 1 or (self.n == 2 and self.m == 2)

    def _all_elements(self) -> Iterator[MatrixElement]:
        """
        Генератор всех элементов GL(n, m).

        Проходит по всем матрицам m^{n×n} и отбирает невырожденные.

        Yields:
            MatrixElement: Следующий элемент группы.
        """
        for entries in product(range(self.m), repeat=self.n * self.n):
            M = np.array(entries, dtype=int).reshape(self.n, self.n) % self.m
            if Matrix(M.tolist()).det() % self.m != 0:
                yield MatrixElement(M, self)

    def comutator(self) -> SubGroup[np.ndarray, MatrixElement]:
        """
        Коммутант группы – SL(n, m), порождённый всеми коммутаторами.

        Returns:
            SubGroup: SL(n, m) как нормальная подгруппа GL(n, m).
        """
        return SubGroup.from_group(SL(self.n, self.m), self)

    def center(self) -> SubGroup[np.ndarray, MatrixElement]:
        """
        Центр группы – множество скалярных матриц λ·Iₙ.

        Returns:
            SubGroup: Подгруппа всех λ·Iₙ с λ ∈ (ℤ/mℤ)*.
        """
        return SubGroup.from_predicate(
            lambda elem: np.all(
                elem.value == np.eye(self.n, dtype=int) * elem.value[0, 0]),
            self
        )

    def __contains__(self, item: MatrixElement) -> bool:
        """
        Проверяет, принадлежит ли элемент этой группе.

        Args:
            item (MatrixElement): Элемент для проверки.

        Returns:
            bool: True, если item.group == self.
        """
        return isinstance(item, MatrixElement) and item.group == self

    def __iter__(self) -> Iterator[MatrixElement]:
        """
        Итератор по всем элементам группы.

        Returns:
            Iterator[MatrixElement]: Элементы от 0 до order-1.
        """
        return (i for i in self._all_elements())
