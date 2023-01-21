from warnings import warn
import numpy as np


from src.SolveMolp.MembershipFunctions import T_norm
from src.SolveMolp.FuzzyOrderings import Orderings
# Function, that checks inout data.

# Paramters: 
#  - Method
#  - Objective functions coefficients
#  - Matrix A: 
#  - Vector B 
#  - Weights
def SolveMolp( Method = "Tprod" , Obj_fn = None, 
    A_ub = None, b_ub = None,  Weights = None):

    if any(it is None for it in  ( Obj_fn, A_ub, b_ub)):
        warn("Missing one or many input parameters: Obj_fn, A_ub, b_ub " , RuntimeWarning  )

    size = [ Obj_fn.shape[0], A_ub.shape[1], A_ub.shape[0] ]
    
    if Weights is None:
        Weights = np.ones(( size[0] , 1))

    if np.amin(Weights) <= 0:
        warn( "Error while assining Weights. Wheights cant be zero or negative" , RuntimeWarning)
    
    Weights = np.append( Weights, np.sum(Weights))

    if Method in ("Tprod","Tmin"):
        Result = T_norm(Method,size,  Obj_fn, A_ub,  b_ub, Weights)
        return(Result)

    if Method in ("OrderLuk", "OrderProd"):
        Result = Orderings(Method,size,  Obj_fn, A_ub,  b_ub, Weights)
        return(Result)




