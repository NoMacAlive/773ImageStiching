import numpy as np
import random
from itertools import combinations
# def normalise(descriptors,descriptors_minus_mean):
#     normalised_disc = []
    
#     for descriptor in descriptors:
#         i = 0
#         n = []
#         for j in range(len(d[i])):
#             no = descriptors_minus_mean[i][j] / std(descriptor)
#             n.append(no)
#         normalised_disc.append(n)
#     len(normalised_disc)
#     len(normalised_disc[0])
#     return normalised_disc

def constructMatrixA(putativeMatch):
    # putativeMatch[0][0][0] 第一行左边tuple的X
    four_index = []
    # Random四个match random.randint(0, 9)
    samplePool = [i for i in range(len(putativeMatch))]
    notcolinear = False
    while notcolinear == False:
        four_index = random.sample(samplePool,4)
        combination_index = combinations(four_index, 3) 
        notcolinear = True
        for combination in list(combination_index):
            c = collinear(putativeMatch[combination[0]][0][0],putativeMatch[combination[0]][0][1],putativeMatch[combination[1]][0][0],putativeMatch[combination[1]][0][1],putativeMatch[combination[2]][0][0],putativeMatch[combination[2]][0][1])
            if c == True:
                notcolinear == False

    # [170, 88, 65, 183]
    A = []
    # print(four_index)
    for i in four_index:
        row1 = [0,0,0]
        row2 = [0,0,0]
        # how many matches
        # how many columns
        # 左边的xy
        xi = [putativeMatch[i][0][0],putativeMatch[i][0][1],1] 
        negative_yislash_xi = [-putativeMatch[i][1][1]*x for x in xi]
        row1.extend(xi)
        row1.extend(negative_yislash_xi)

        negative_xislash_xi = [-putativeMatch[i][1][0]*x for x in xi]
        xi.extend(row2)
        xi.extend(negative_xislash_xi)
        A.append(row1)
        A.append(xi)
    # print("A:")
    # print(A)
    return A

# function to check if  
# point collinear or not 
def collinear(x1, y1, x2, y2, x3, y3): 

    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2) 
  
    if (a == 0): 
        return True
    else: 
        return False
  

def computeFianlH(left_points,right_points):
    A = []
    # print(four_index)
    for i in range(len(left_points)):
        row1 = [0,0,0]
        row2 = [0,0,0]
        # how many matches
        # how many columns
        # 左边的xy
        xi = [left_points[i][0],left_points[i][1],1] 
        negative_yislash_xi = [-right_points[i][1]*x for x in xi]
        row1.extend(xi)
        row1.extend(negative_yislash_xi)

        negative_xislash_xi = [-right_points[i][0]*x for x in xi]
        xi.extend(row2)
        xi.extend(negative_xislash_xi)
        A.append(row1)
        A.append(xi)
    u,s,vt = np.linalg.svd(A)
    vLastRow = vt[len(vt)-1,:]
    vLastRow[:] = [x / vLastRow[-1] for x in vLastRow]
    # print(vLastRow)
    H = np.reshape(vLastRow,(3, 3))
    return H

def findhomography(putativeMatch):
    threshold = 1
    putativeMatches = np.array(putativeMatch)
    left_tuples = putativeMatches[:,0]
    right_tuples = putativeMatches[:,1]
    inliers = {
        "point_left": [],
        "point_right": [],
        "count": [],
        "H" : []
    }
    # print(left_tuples)
    # print(right_tuples)
    for i in range(1000):
        A = constructMatrixA(putativeMatch)
        # print(A)

        u,s,vt = np.linalg.svd(A)
        vLastRow = vt[len(vt)-1,:]
        vLastRow[:] = [x / vLastRow[-1] for x in vLastRow]
        # print(vLastRow)
        H = np.reshape(vLastRow,(3, 3))
        # print(H) 
    

        j = 0
        count = 0        
        point_left = []
        point_right = []
        # left point times H
        for point in left_tuples:
            x = point[0]
            y = point[1]
            left_homogenous_point = [x,y,1]
            point = np.array(left_homogenous_point)
            point = point.T
            # transform
            transformed_point = H.dot(point)

            # normalize
            transformed_point[:] = [x / transformed_point[2] for x in transformed_point]
            # compute distance with right point
            distance = np.sqrt(pow((transformed_point[0]-right_tuples[j][0]),2) + pow((transformed_point[1]-right_tuples[j][1]),2))

            # print("left point:")
            # print(point)

            # print("transformed point:")
            # print(transformed_point)


            # print("right point:")
            # print((right_tuples[j][0],right_tuples[j][1]))



            # if distance smaller than threshold
            if distance<=threshold:
                # store H and the 小于的点和个数
                point_left.append((x,y))
                point_right.append((right_tuples[j][0],right_tuples[j][1]))
                count = count + 1
            j = j + 1

        inliers['point_left'].append(point_left)
        inliers['point_right'].append(point_right)
        inliers['count'].append(count)
        inliers['H'].append(H)

    # find the larges count H
    largest_count_index = inliers['count'].index(max(inliers['count']))

    best_H = inliers['H'][largest_count_index]

    inlier_left = inliers['point_left'][largest_count_index]
    inlier_right = inliers['point_right'][largest_count_index]

    # print("left points:")
    # print(inlier_left)
    # print("right points:")
    # print(inlier_right)
    # print("H")
    # print(best_H)
    H = computeFianlH(inlier_left,inlier_right)
    return H,inlier_left,inlier_right








