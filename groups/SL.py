from __future__ import annotations

from itertools import product
from math import gcd
from typing import Iterator

import numpy as np
from sympy import factorint, isprime, Matrix

from elements.linear import MatrixElement
from groups.finite_group import FiniteGroup
from groups.Subgroup import SubGroup
from groups.symmetric_group import SymmetricGroup


class SLnm(FiniteGroup[np.ndarray, MatrixElement]):
    """
    Специальная линейная группа SL(n, m):
    все невырожденные n×n матрицы над кольцом ℤ/mℤ
    с детерминантом, сравнимым с 1 по модулю m.
    """

    def __new__(cls, n: int, m: int):
        """
        Переопределённый конструктор, возвращает в некоторых случаях более простые группы:
          - SL(2,2) ≅ S₃ (симметрическая группа порядка 6);
          - иначе — стандартный SLnm.

        Args:
            n (int): Размерность матриц (n > 0).
            m (int): Модуль (m > 1).

        Returns:
            SLnm | SymmetricGroup: Экземпляр соответствующей группы.
        """
        if n == 2 and m == 2:
            # SL(2,2) изоморфна S₃
            return SymmetricGroup(3)
        return super().__new__(cls)

    def __init__(self, n: int, m: int):
        """
        Инициализирует параметры группы.

        Args:
            n (int): Должно быть > 0.
            m (int): Должно быть > 1.

        Raises:
            AssertionError: Если входные параметры некорректны.
        """
        assert isinstance(n, int) and n > 0, "n должно быть целым > 0"
        assert isinstance(m, int) and m > 1, "m должно быть целым > 1"
        self.n = n
        self.m = m

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
        Итератор по всем элементам SL(n, m).

        Uses:
            _all_elements — генератор всех матриц det ≡ 1 (mod m).

        Returns:
            Iterator[MatrixElement]: Поочерёдно все элементы группы.
        """
        return self._all_elements()

    def identity(self) -> MatrixElement:
        """
        Нейтральный элемент группы.

        Returns:
            MatrixElement: Единичная матрица Iₙ по модулю m.
        """
        I = np.eye(self.n, dtype=int) % self.m
        return MatrixElement(I, self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        """
        Групповая операция: умножение матриц по модулю m.

        Args:
            a (MatrixElement): Левая матрица.
            b (MatrixElement): Правая матрица.

        Returns:
            MatrixElement: (a @ b) % m.
        """
        C = (a.value @ b.value) % self.m
        return MatrixElement(C, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        """
        Обратный элемент (обратная матрица по модулю m).

        Args:
            a (MatrixElement): Элемент, для которого ищем обратный.

        Returns:
            MatrixElement: Обратная матрица a⁻¹ mod m.

        Raises:
            ValueError: Если матрица не обратима по модулю m.
        """
        inv_list = Matrix(a.value.tolist()).inv_mod(self.m).tolist()
        inv = np.array(inv_list, dtype=int) % self.m
        return MatrixElement(inv, self)

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        """
        Доступ к элементу по его двумерному массиву.

        Args:
            matrix (np.ndarray): Входная матрица.

        Returns:
            MatrixElement: Корректированный элемент SL(n, m).

        Raises:
            ValueError: Если форма ≠ (n,n) или det ≠ 1 (mod m).
        """
        M = np.array(matrix, dtype=int) % self.m
        if M.shape != (self.n, self.n):
            raise ValueError(f"Ожидается матрица {self.n}×{self.n}, получили {M.shape}")
        det_mod = Matrix(M.tolist()).det() % self.m
        if det_mod != 1:
            raise ValueError(f"det ≡ 1 (mod {self.m}), а det ≡ {det_mod}")
        return MatrixElement(M, self)

    def __len__(self) -> int:
        """
        Порядок группы SL(n, m).

        Формула:
            |SL(n,m)| = m^{n(n−1)/2} × ∏_{i=2..n} (m^i − 1)

        Returns:
            int: Число элементов группы.
        """
        total = 1
        for i in range(2, self.n + 1):
            total *= (self.m**i - 1)
        return (self.m ** (self.n * (self.n - 1) // 2)) * total

    def _all_elements(self) -> Iterator[MatrixElement]:
        """
        Генератор всех элементов SL(n, m) (для небольших n, m).

        Проходит по всем возможным матрицам m^{n×n} и отбирает невырожденные с det ≡ 1.

        Yields:
            MatrixElement: Следующий элемент группы.
        """
        for entries in product(range(self.m), repeat=self.n * self.n):
            M = np.array(entries, dtype=int).reshape(self.n, self.n) % self.m
            if Matrix(M.tolist()).det() % self.m == 1:
                yield MatrixElement(M, self)

    def is_lagrangian(self) -> bool:
        """
        Проверяет обратную теорему Лагранжа.

        SL(n,m) в общем случае не лагранжева, кроме n=1.

        Returns:
            bool: True, если n == 1.
        """
        return self.n == 1

    def is_abelian(self) -> bool:
        """
        Проверяет коммутативность группы.

        SL(n,m) абелева только при n=1.

        Returns:
            bool: True, если n == 1.
        """
        return self.n == 1

    def is_simple(self) -> bool:
        """
        Проверяет, является ли группа простой.

        Условия для простоты SL(n,q) над конечным полем q=p^k:
          1. n ≥ 2;
          2. q = p^k для простого p;
          3. (n, q) ∉ {(2,2), (2,3)};
          4. gcd(n, q−1) = 1.

        Returns:
            bool: True, если все условия выполнены.
        """
        if self.n < 2:
            return False
        q = self.m
        factors = factorint(q)
        # q должно быть степенью простого
        if len(factors) != 1 or not isprime(next(iter(factors))):
            return False
        if (self.n, q) in {(2, 2), (2, 3)}:
            return False
        # центр тривиален ⇔ gcd(n, q-1) == 1
        return gcd(self.n, q - 1) == 1

    def is_solvable(self) -> bool:
        """
        Проверяет разрешимость группы.

        Разрешима, если:
          - n = 1 (абелева);
          - или n = 2 и m ∈ {2, 3} (S3 и SL(2,3)).

        Returns:
            bool: True для перечисленных случаев.
        """
        return self.n == 1 or (self.n == 2 and self.m in (2, 3))

    def comutator(self) -> SubGroup[np.ndarray, MatrixElement]:
        """
        Коммутант (производная группа).

        Для n ≥ 2 SL(n,m) совершенная ⇒ коммутант = сама группа.
        Иначе — тривиальная подгруппа.

        Returns:
            SubGroup: Коммутант SL(n,m).
        """
        if self.n >= 2:
            return SubGroup.from_group(self, self)
        return SubGroup.trivial_identity(self)

    def center(self) -> SubGroup[np.ndarray, MatrixElement]:
        """
        Центр группы — все скалярные матрицы λIₙ, где λ^n ≡ 1 (mod m).

        Returns:
            SubGroup: Подгруппа скалярных матриц λIₙ.
        """
        def predicate(elem: MatrixElement) -> bool:
            M = elem.value
            scalar = M[0, 0] % self.m
            # Проверяем форму λIₙ
            if not np.array_equal(M, np.eye(self.n, dtype=int) * scalar):
                return False
            # Проверяем λ^n ≡ 1 mod m
            return pow(int(scalar), self.n, self.m) == 1

        return SubGroup.from_predicate(predicate, self)
