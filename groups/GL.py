from itertools import product
from math import prod

import numpy as np
from sympy import isprime, Matrix

from elements.Linear import MatrixElement
from groups.finite_group import FiniteGroup
from groups.infinite_group import InfiniteGroup


class GLnR(InfiniteGroup[np.ndarray, MatrixElement]):

    def __init__(self, n: int):
        self.n = n

    def identity(self) -> MatrixElement:
        return MatrixElement(np.eye(self.n), self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        return MatrixElement(a.value @ b.value, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        return MatrixElement(np.linalg.inv(a.value), self)

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        M = np.array(matrix, dtype=float)
        if M.shape != (self.n, self.n):
            raise ValueError(f"Ожидается матрица {self.n}×{self.n}")
        if abs(np.linalg.det(M)) < 1e-12:
            raise ValueError("Сингулярная матрица не в GL(n,R)")
        return MatrixElement(M, self)


class GLnm(FiniteGroup[np.ndarray, MatrixElement]):

    def __new__(cls, n:int, m:int):
        # TODO n=2 m=2 return S3
        # TODO n=1 m=p return Z(p-1)
        return super().__new__(cls)

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m

    def identity(self) -> MatrixElement:
        I = np.eye(self.n, dtype=int) % self.m
        return MatrixElement(I, self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        M = (a.value @ b.value) % self.m
        return MatrixElement(M, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        return MatrixElement(
            np.array(Matrix(a.value.tolist()).inv_mod(self.m).tolist(),
                     dtype=int) % self.m, self)

    def __len__(self) -> int:
        # |GL(n,m)| = \prod_0^{n-1}(m^n - m^i)
        return prod(self.m ** self.n - self.m ** i for i in range(self.n))

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        M = np.array(matrix, dtype=int) % self.m
        if M.shape != (self.n, self.n):
            raise ValueError(f"Ожидается матрица {self.n}×{self.n}")

        if Matrix(M.tolist()).det() % self.m == 0:
            raise ValueError("Сингулярная матрица не в GL(n, m)")
        return MatrixElement(M, self)

    def is_abelian(self) -> bool:
        return self.n == 1

    def is_simple(self) -> bool:
        if self.n >= 2:
            return False
        return isprime(self.m-1)

    def is_lagrangian(self) -> bool:
        return self.n == 1

    def _all_elements(self):
        for entries in product(range(self.m), repeat=self.n * self.n):
            M = np.array(entries, dtype=int).reshape(self.n, self.n) % self.m
            if Matrix(M.tolist()).det() % self.m != 0:
                yield MatrixElement(M, self)

    def comutator(self) -> "SubGroup":
        return SubGroup.from_group(SL(n, m), self)

    def center(self) -> "SubGroup":
        return SubGroup.from_predicate(
            lambda m: m.value == np.eye(self.n, dtype=int) * m.value[0][0],
            self)

    def solvable(self) -> bool:
        if self.n == 1:
            return True
        return self.n == 2 and self.m in (2, 3)
