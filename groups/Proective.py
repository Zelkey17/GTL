from groups.SL import SLnm
from groups.GL import GLnm
from groups.Factor import FactorGroup

class PSLnm:
    def __new__(cls, n: int, m: int):
        sl = SLnm(n, m)
        return FactorGroup(sl, sl.center())

class PGLnm:
    def __new__(cls, n: int, m: int):
        gl = GLnm(n, m)
        return FactorGroup(gl, gl.center())
