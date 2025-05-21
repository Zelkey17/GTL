from __future__ import annotations


from groups.SL import SLnm
from groups.GL import GLnm
from groups.Factor import FactorGroup
from elements.linear import MatrixElement



class PSLnm:
    """
    Фабрика для проективной специальной линейной группы PSL(n, m).

    PSL(n, m) определяется как фактор-группа SL(n, m) по её центру:
        PSL(n, m) = SL(n, m) / Z(SL(n, m)).

    Эта группа часто обозначает «проективную» версию SL, где скалярные матрицы
    (центральные элементы) отождествляются с нейтральным.

    Usage:
        psl = PSLnm(n, m)  # вернёт FactorGroup для SL(n,m) по центру
    """

    def __new__(cls, n: int, m: int)->FactorGroup[MatrixElement]:
        """
        Создает фактор-группу PSL(n, m).

        Args:
            n (int): Размерность квадратных матриц (n > 0).
            m (int): Модуль (m > 1).

        Returns:
            FactorGroup: Экземпляр фактор-группы SL(n, m) по её центру.

        Raises:
            AssertionError: Если аргументы n или m некорректны,
                            делегируется SLnm.
        """
        # Строим SL(n, m)
        sl_group = SLnm(n, m)
        # Делим на центр SL, получая PSL
        return FactorGroup(sl_group, sl_group.center())


class PGLnm:
    """
    Фабрика для проективной общей линейной группы PGL(n, m).

    PGL(n, m) определяется как фактор-группа GL(n, m) по её центру:
        PGL(n, m) = GL(n, m) / Z(GL(n, m)).

    Проективная группа «отбрасывает» скалярные матрицы, делая их тривиальными.

    Usage:
        pgl = PGLnm(n, m)  # вернёт FactorGroup для GL(n,m) по центру
    """

    def __new__(cls, n: int, m: int) -> FactorGroup[MatrixElement]:
        """
        Создает фактор-группу PGL(n, m).

        Args:
            n (int): Размерность квадратных матриц (n > 0).
            m (int): Модуль (m > 1).

        Returns:
            FactorGroup: Экземпляр фактор-группы GL(n, m) по её центру.

        Raises:
            AssertionError: Если аргументы n или m некорректны,
                            делегируется GLnm.
        """
        # Строим GL(n, m)
        gl_group = GLnm(n, m)
        # Делим на центр GL, получая PGL
        return FactorGroup(gl_group, gl_group.center())
