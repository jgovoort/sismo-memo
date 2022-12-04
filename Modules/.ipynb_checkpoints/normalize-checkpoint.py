import numpy as np

def normalize(array) :
    array = np.array(array)
    retarray = (array - np.min(array))/(np.max(array)-np.min(array))
    
    return retarray