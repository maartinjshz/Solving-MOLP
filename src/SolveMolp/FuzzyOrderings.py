from scipy.optimize import linprog, minimize,brute
import numpy as np
from warnings import warn
from pypoman import compute_polytope_vertices


# Checks if the point is inside the set D. 
def Constraints(x):
    if np.amin(x) < 0:
        return False

    for i in range(0,Size[2]):
        val = np.dot(  A_ub[i],x  )
        if val > B_ub[i]:
            return False
    return True

###
# Functions to calculate the value of Product Fuzzy Orderings
###


# Calculates value of the i-th product-ordering
def Equivalence_Product(x,y,it):
    z_x = np.dot(x, Obj_fn[it])
    z_y = np.dot(y, Obj_fn[it])

    if z_x <= z_y:
        return 1
    else:
        return np.exp( - np.abs(z_x-z_y)/( z_max_value[it] -z_min_value[it]))

# Function that Aggregates Orderings
def Agregation_Product(x,y):

# Return 0, if the point is outside of the set D.
    if Constraints(y) == False:
        return 0

    Val = 0
    for it in range(0, Size[0]):
        Val *= Equivalence_Product(x,y,it)**(Weights[it]/Weights[-1])
    return Val

def function_to_max_Product(y):
    MinVal = 2
    for it in D_Vertices:
        MinVal = min(  Agregation_Product(it,y),MinVal )
    return - MinVal


###
# Functions to calculate the value of Lukasiewicz Fuzzy Orderings
###


# Calculates value of the i-th Lukasiewicz-ordering
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
def function_to_max_Lukasiewicz(y):
    MinVal = 2
    for it in D_Vertices:
        MinVal = min(  Agregation_Lukasiewicz(it,y),MinVal )
    return - MinVal


def Orderings(Method, size = None, obj_fn = None, 
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
    z_max_value,z_min_value= [],[]

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
            z_min_value.append( np.dot(  Obj_fn[i], rez_min.x ))
        Obj_fn *= -1
    Obj_fn *= -1
    if Exsists_exstremum == False:
        warn( "Error while finding local extremum for objective functions" , RuntimeWarning)
    else:

# Finds all the Vertices for set D. required for the Min part. 
        global D_Vertices
        D_Vertices = compute_polytope_vertices(np.vstack((A_ub, - np.eye(Size[1])))
        ,np.append(B_ub, np.zeros((Size[1],1))))
     
# Finds the upper bound for each variable. It is required for the Brute function. 
        Bounds = np.zeros((Size[1],2))
        for i in D_Vertices:
            for j in range(0,Size[1]):
                if i[j] > Bounds[j][1]:
                    Bounds[j][1] = i[j]

        # 
        # 

        if Method == "OrderLuk":
            Result = brute(  function_to_max_Lukasiewicz, Bounds, Ns = np.max(Bounds)* 10)

        if Method == "OrderProd":
            Result = brute(  function_to_max_Product, Bounds, Ns = np.max(Bounds)* 10)

        return Result