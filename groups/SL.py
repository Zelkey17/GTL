from itertools import product
import numpy as np
from sympy import Matrix, factorint, isprime
from math import gcd

from elements.Linear import MatrixElement
from groups.finite_group import FiniteGroup
from groups.infinite_group import InfiniteGroup
from groups.subgroup import SubGroup


class SLnR(InfiniteGroup[np.ndarray, MatrixElement]):
    """
    Специальная линейная группа SL(n, R):
    невырожденные вещественные матрицы размера n×n с det = 1.
    """
    def __init__(self, n: int):
        self.n = n

    def identity(self) -> MatrixElement:
        I = np.eye(self.n, dtype=float)
        return MatrixElement(I, self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        return MatrixElement(a.value @ b.value, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        return MatrixElement(np.linalg.inv(a.value), self)

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        M = np.array(matrix, dtype=float)
        if M.shape != (self.n, self.n):
            raise ValueError(f"Нужна матрица {self.n}×{self.n}, получили {M.shape}")
        det = np.linalg.det(M)
        if not np.isclose(det, 1.0, atol=1e-8):
            raise ValueError(f"Детерминант должен быть 1, а det = {det}")
        return MatrixElement(M, self)


class SLnm(FiniteGroup[np.ndarray, MatrixElement]):
    """
    Специальная линейная группа SL(n, m):
    невырожденные матрицы n×n над Z/mZ с det ≡ 1 (mod m).
    """

    def __new__(cls, n:int,m:int):
        # TODO n=2 m=2 return S3
        # TODO n=2 m=4 return A5
        # TODO n=4 m=2 return A8
        return super().__new__(cls)

    def __init__(self, n: int, m: int):
        assert isinstance(n, int) and n > 0, "n должно быть целым >0"
        assert isinstance(m, int) and m > 1, "m должно быть целым >1"
        self.n = n
        self.m = m

    def identity(self) -> MatrixElement:
        I = np.eye(self.n, dtype=int) % self.m
        return MatrixElement(I, self)

    def op(self, a: MatrixElement, b: MatrixElement) -> MatrixElement:
        C = (a.value @ b.value) % self.m
        return MatrixElement(C, self)

    def inverse(self, a: MatrixElement) -> MatrixElement:
        inv_mat = Matrix(a.value.tolist()).inv_mod(self.m).tolist()
        inv = np.array(inv_mat, dtype=int) % self.m
        return MatrixElement(inv, self)

    def __getitem__(self, matrix: np.ndarray) -> MatrixElement:
        M = np.array(matrix, dtype=int) % self.m
        if M.shape != (self.n, self.n):
            raise ValueError(f"Нужна матрица {self.n}×{self.n}, получили {M.shape}")
        det_mod = Matrix(M.tolist()).det() % self.m
        if det_mod != 1:
            raise ValueError(f"det ≡ 1 (mod {self.m}), а det ≡ {det_mod}")
        return MatrixElement(M, self)

    def __len__(self) -> int:
        # |SL(n, m)| = m^{n(n-1)/2} * ∏_{i=2..n}(m^i - 1)
        total = 1
        for i in range(2, self.n + 1):
            total *= (self.m**i - 1)
        return (self.m**(self.n * (self.n - 1) // 2)) * total

    def all_elements(self):
        """Перечисление всех элементов SL(n, m) (для небольших n, m)."""
        for entries in product(range(self.m), repeat=self.n * self.n):
            M = np.array(entries, dtype=int).reshape(self.n, self.n) % self.m
            if Matrix(M.tolist()).det() % self.m == 1:
                yield MatrixElement(M, self)

    def is_lagrangian(self) -> bool:
        """
        Группа лагранжева, если для каждого делителя порядка группы
        существует подгруппа такого порядка. SL(n,m) в общем случае
        не удовлетворяет теореме Лагранжа, кроме n=1.
        """
        return self.n == 1

    def is_abelian(self) -> bool:
        """
        SL(n,m) абелева только при n=1.
        """
        return self.n == 1

    def is_simple(self) -> bool:
        """
        Проверяет, является ли группа простой.

        SL(n,q) простая тогда и только тогда,
        когда центр тривиален (gcd(n,q-1)=1),
        поле конечно (q=p^k),
        n>=2 и (n,q) не в {(2,2),(2,3)}.
        """
        if self.n < 2:
            return False
        q = self.m
        # проверяем, что q — степень простого числа
        f = factorint(q)
        if len(f) != 1 or not isprime(next(iter(f))):
            return False
        if (self.n, q) in {(2, 2), (2, 3)}:
            return False
        # центр тривиален <=> gcd(n, q-1) = 1
        if gcd(self.n, q - 1) != 1:
            return False
        return True

    def is_solvable(self) -> bool:
        if self.n == 1:
            return True
        return self.n == 2 and self.m in (2, 3)

    def comutator(self) -> SubGroup:
        """
        Коммутант (производная группа).
        SL(n,m) совершенная для n>=2, иначе тривиальная.
        """
        if self.n >= 2:
            return SubGroup.from_group(self, self)
        return SubGroup.from_predicate(lambda g: True, self)

    def center(self) -> SubGroup:
        """
        Центр: скалярные матрицы λI, где λ^n ≡ 1 (mod m).
        """
        def pred(g: MatrixElement) -> bool:
            M = g.value
            if not np.array_equal(M, np.eye(self.n, dtype=int) * (M[0,0] % self.m)):
                return False
            return pow(int(M[0,0]), self.n, self.m) == 1
        return SubGroup.from_predicate(pred, self)
