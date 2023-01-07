from MembershipFunctions import Tprod

# Function, that checks inout data.

# Paramters: 
#  - List : [ number of Ojb. functions, number of variables, number of constraints]
#  - List of Objective functions coefficients
#  - Matrix A: 
#  - Vector B 
#  - Weights
def SolveMolp( Method = None ,size = None, Obj_fn = None, 
    A_ub = None, b_ub = None,  Weights = None):
    
    if Method == "Tprod":
        Result = Tprod(size,  Obj_fn, A_ub,  b_ub, Weights)
        return(Result)