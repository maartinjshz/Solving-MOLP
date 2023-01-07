from warnings import warn
import numpy as np


from MembershipFunctions import Tprod
# Function, that checks inout data.

# Paramters: 
#  - Method
#  - Objective functions coefficients
#  - Matrix A: 
#  - Vector B 
#  - Weights
def SolveMolp( Method = "Tprod" , Obj_fn = None, 
    A_ub = None, b_ub = None,  Weights = None):

    size = [ Obj_fn.shape[0], A_ub.shape[0], A_ub.shape[1] ]
    
    if np.amin(Weights) <= 0:
        warn( "Error while assining Weights. Wheights cant be zero or negative" , RuntimeWarning)

    if Weights is None:
        Weights = np.ones(( size[0] , 1))
    
    Weights = np.append( Weights, np.sum(Weights))

    if None in ( Obj_fn, A_ub, b_ub):
        warn("Missing one or many input parameters: Obj_fn, A_ub, b_ub " , RuntimeWarning  )

    if Method == "Tprod":
        Result = Tprod(size,  Obj_fn, A_ub,  b_ub, Weights)
        return(Result)