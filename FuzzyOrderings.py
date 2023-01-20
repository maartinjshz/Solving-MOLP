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

def Equivalence_Lukasiewicz(x,y,it):
    z_x = np.dot(x, Obj_fn[it])
    z_y = np.dot(y, Obj_fn[it])

    if z_x <= z_y:
        return 1
    else:
        return 1 - np.abs(z_x-z_y)/( z_max_value[it] -z_min_value[it])

# Function that Aggregates Orderings
def Agregation_Lukasiewicz(x,y):

# Return 0, if the point is outside of the set D.
    if Constraints(y) == False:
        return 0

    Val = 0
    for it in range(0, Size[0]):
        Val += Equivalence_Lukasiewicz(x,y,it) * Weights[it]/Weights[-1]
    return Val

# This function does the Minimisation part in the Max - Min problem.
def function_to_max(y):
    MinVal = 2
    for it in range(0, Size[0]):
        MinVal = min(  Agregation_Lukasiewicz(z_max[it],y),MinVal )
    return - MinVal


def Orderings(size = None, obj_fn = None, 
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

    global z_max_value,z_min_value, z_max
    z_max_value,z_min_value, z_max= [],[], np.zeros((size[0],size[1]))

    # Finds local extremums for each function. (Minimum and maximum)
    for i in range(0,size[0]):
        rez_max = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_max.success == False:
            Exsists_exstremum = False
        else:
            z_max[i]= rez_max.x
            z_max_value.append( np.dot(  -Obj_fn[i], rez_max.x ))
        Obj_fn *= -1
        # Atrod optimālo atrisinājumi otrai funkcijai ar simpleksa metodi
        rez_min = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_min.success == False:
            Exsists_exstremum = False
        else:
            z_min_value.append( np.dot(  Obj_fn[i], rez_min.x ))
        Obj_fn *= -1
    Obj_fn *= -1
    if Exsists_exstremum == False:
        warn( "Error while finding local extremum for objective functions" , RuntimeWarning)
    else:

        # Finds the optimal solution using Nelder Mead method from
        # Scipy module.
        x_start =  ( z_max[0] + z_max[1]) * 1/2
     
        # 
        # 
        Result = (minimize( function_to_max, x_start,method='Nelder-Mead',
        options={'xatol': 1e-12, 'disp': False,'maxiter': 10000} ))
        return Result.x