from scipy.optimize import linprog, minimize
import numpy as np
from warnings import warn




# Checks if the point is inside the set D. 
def Constraints(x):
    if np.amin(x) < 0:
        return False

    for i in range(0,Size[2]):
        val = np.dot(  A_ub[i],x  )
        if val > B_ub[i]:
            return False
    return True


# Finds the value for membership function
def MembershipFunction(x,i):


# Returns 0, if the x is outside of the set D.
    if Constraints(x) == False:
        return 0

    Obj_fun_val = np.dot(Obj_fn[i], x  )
    if Obj_fun_val<= z_min_value[i]:
        return 0
    elif z_min_value[i] < Obj_fun_val and Obj_fun_val < z_max_value[i] :
        return (Obj_fun_val - z_min_value[i])/(z_max_value[i] - z_min_value[i])
    else:
        return 1

# Functions to optimize: 

# Find Product T-norm of membership function at point x
def ProdNorm(x):
    val = 1
    for i in range( 0,Size[0]):
        val = val* MembershipFunction(x,i)* Weights[i]/Weights[-1]
    
    return  -val

def MinNorm(x):
    val = 1
    for i in range(0, Size[0]):
        val = min(val,MembershipFunction(x,i))
    return - val

def T_norm(Method,size = None, obj_fn = None, 
    a_ub = None, b_ub = None, weights = None):
    
# Variables are required to be global, because when using
# NelderMead method from scipy.minimze, 
# Only the vector x can be passed. Because other variables are needed
# They are passed as global variables

    global Size, A_ub, B_ub, Obj_fn, Weights
    Size, A_ub,B_ub,Obj_fn,Weights = size,a_ub,b_ub, obj_fn, weights

    # Izveido mainīgo nosacījumus, lai varētu lietot
    # Iebūvēto simpleksa metodi
    Exsists_exstremum = True
    Obj_fn *= -1

    # Lists are made Global, because their values will be needed for 
    # Constructing Membership function but while using scipy.optimize, 
    # They cant be passed. 

    global z_max_value,z_min_value
    z_max_value,z_min_value = [],[]

    # Finds local extremums for each function. (Minimum and maximum)
    for i in range(0,size[0]):
        rez_max = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_max.success == False:
            Exsists_exstremum = False
        else:
            z_max_value.append( np.dot(  -Obj_fn[i], rez_max.x ))
        Obj_fn *= -1
        # Atrod optimālo atrisinājumi otrai funkcijai ar simpleksa metodi
        rez_min = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_min.success == False:
            Exsists_exstremum = False
        else:
            z_min_value.append( np.dot(  Obj_fn[i], rez_min.x))
        Obj_fn *= -1
    Obj_fn *= -1
    if Exsists_exstremum == False:
        warn( "Error while finding local extremum for objective functions" , RuntimeWarning)
    else:
        # Lists are made Global, because their values will be needed for 
        # Constructing Membership function but while using scipy.optimize, 
        # They cant be passed. 


        # Finds the optimal solution using Nelder Mead method from
        # Scipy module.
        x_start =  ( rez_max.x + rez_min.x) * 1/2
     
        # 
        # 

        if Method == "Tprod":
            Result = (minimize( ProdNorm, x_start,method='Nelder-Mead',
            options={'xatol': 1e-12, 'disp': True,'maxiter': 10000} ))
            
        if Method == "Tmin":
            Result = (minimize( MinNorm, x_start,method='Nelder-Mead',
            options={'xatol': 1e-12, 'disp': True,'maxiter': 10000} ))

        return Result.x