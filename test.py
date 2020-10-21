import numpy as np
import math

H = np.array([[ 1.34376576e+00,-2.59822655e-02 ,-2.76359394e+02],
 [ 1.26652755e-01 , 1.17295657e+00 ,-5.83733890e+01],
 [ 3.57779925e-04 ,-3.80543974e-05 , 1.00000000e+00]])

mappedPoint = np.array([241,723,1])
sourcePoint = H.dot(mappedPoint)
print(sourcePoint)
# sourcePoint[:] = [x / mappedPoint[2] for x in mappedPoint]
point = [sourcePoint[0]/sourcePoint[2],sourcePoint[1]/sourcePoint[2]]
print(point)
