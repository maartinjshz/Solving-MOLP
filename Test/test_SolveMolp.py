from src.SolveMolp.Optimeze import SolveMolp
import numpy as np



def test_FuzzyOrders():
    A = np.array([[-1,3],[1,3],[4,3],[3,1]])
    b = np.array([21,27,45,30])
    objFun = np.array([[-1,2],[2,1]])
    SolveMolp("OrderLuk",objFun,A,b)
    SolveMolp("OrderProd",objFun,A,b)

    A = np.array([[1,1]])
    b = np.array([1])
    objFun = np.array([[1,0], [0,1]])
    SolveMolp("OrderLuk",objFun,A,b)
    SolveMolp("OrderProd",objFun,A,b)

def test_MebershipFunctions():
    A = np.array([[-1,3],[1,3],[4,3],[3,1]])
    b = np.array([21,27,45,30])
    objFun = np.array([[-1,2],[2,1]])
    SolveMolp("Tprod",objFun,A,b)
    SolveMolp("Tmin",objFun,A,b)

    A = np.array([[1,1]])
    b = np.array([1])
    objFun = np.array([[1,0], [0,1]])
    SolveMolp("Tprod",objFun,A,b)
    SolveMolp("Tmin",objFun,A,b)
