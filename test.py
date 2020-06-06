import numpy as np
H = [[ 1.13027411e+00 ,5.14837414e-02,-5.45949905e+01],[ 1.55226561e-02 ,1.16910770e+00,-7.45823504e+02],[-1.55121721e-05, 1.79008277e-04, 1.00000000e+00]]
H = np.array(H)
left_homogenous_point = (444, 947, 1)
point = np.array(left_homogenous_point)
point = point.T
transformed_point = H.dot(point)

transformed_point[:] = [x / transformed_point[2] for x in transformed_point]
print("left point")
print(left_homogenous_point)

print("transformed point")
print(transformed_point)

print("right point")
print((426.0, 317.0))

