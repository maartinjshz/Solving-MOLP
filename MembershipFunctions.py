from sympy import Min
from scipy.optimize import linprog, minimize
import numpy as np




# Checks if the point is inside the set D. 
def Constraints(x):
    for i in range(0,Size[2]):
        val = np.dot(  A_ub[i],x  )
        if val > B_ub[i]:
            return False
    return True


# Finds the value for membership function
def MembershipFunction(x,i):

# Returns 0, if any varialbe is less than 0
    if np.amin(x) < 0:
        return 0
# Or 0, if the x is outside of D 
    if Constraints(x) == False:
        return 0

    Obj_fun_val = np.dot(Obj_fn[i], x  )
    if Obj_fun_val<= z_min_value[i]:
        return 0
    elif z_min_value[i] < Obj_fun_val and Obj_fun_val < z_max_value[i] :
        return (Obj_fun_val - z_min_value[i])/(z_max_value[i] - z_min_value[i])
    else:
        return 1

# Find Product T-norm of membership function at point x
def ProdNorm(x):
    val = 1
    for i in range( 0,Size[0]):
        val = val* MembershipFunction(x,i)
    
    return  -val


def Tprod(size = None, obj_fn = None, 
    a_ub = None, b_ub = None, Weights = None):
    
# Variables are required to be global, because when using
# NelderMead method from scipy.minimze, 
# Only the vector x can be passed. Because other variables are needed
# They are passed as global variables

    global Size, A_ub, B_ub, Obj_fn
    Size, A_ub,B_ub,Obj_fn = size,a_ub,b_ub, obj_fn

    # Izveido mainīgo nosacījumus, lai varētu lietot
    # Iebūvēto simpleksa metodi
    Exsists_exstremum = True
    Obj_fn *= -1
    # Finds local extremums for each function. (Minimum and maximum)
    z_min = np.zeros((size[0], size[1]))
    z_max = np.zeros((size[0],size[1]))
    for i in range(0,size[0]):
        rez_max = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_max.success == False:
            Exsists_exstremum = False
        else:
            z_max[i]= rez_max.x
        Obj_fn *= -1
        # Atrod optimālo atrisinājumi otrai funkcijai ar simpleksa metodi
        rez_min = linprog(Obj_fn[i], A_ub = A_ub,b_ub = b_ub,method='revised simplex')
        if rez_min.success == False:
            Exsists_exstremum = False
        else:
            z_min[i]= rez_min.x
        Obj_fn *= -1
    Obj_fn *= -1
    if Exsists_exstremum == False:
        print("Error when trying to find a local extremum.")
    else:
        # Lists are made Global, because their values will be needed for 
        # Constructing Membership function but while using scipy.optimize, 
        # They cant be passed. 
        global z_max_value,z_min_value
        z_max_value = []
        z_min_value =[]

        for i in range(0,size[0]):
            z_max_value.append( np.dot(  Obj_fn[i], z_max[i] ))
            z_min_value.append( np.dot(  Obj_fn[i], z_min[i] ))

        # Atrod optimālo atrisinājumu, lietojot
        # "Nelder-Mead" metodi
        x_start =  ( z_max[0] + z_max[1]) * 1/2
     
        # Lai optimizētu lietojot citu T-normu
        # Nepieciešams nomainīt fwunkciju zemāk.
        Result = (minimize( ProdNorm, x_start,method='Nelder-Mead',
        options={'xatol': 1e-12, 'disp': True,'maxiter': 10000} ))

        return Result.x