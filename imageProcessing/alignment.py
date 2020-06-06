import numpy as np
import pysnooper
import math
#remove out of boundary points
def preProcessing(left_corners_tuples,right_corners_tuples,width,height):
    left_corners_num = len(left_corners_tuples)
    right_corners_num = len(right_corners_tuples)
    newTuples_L = []
    newTuples_R = []
    if left_corners_num == right_corners_num:
        for i in range(left_corners_num):
            if left_corners_tuples[i][0]>=7 and left_corners_tuples[i][0]<=height-8 and left_corners_tuples[i][1]>=7 and left_corners_tuples[i][1]<=width-8:
                newTuples_L.append(left_corners_tuples[i])
            if right_corners_tuples[i][0]>=7 and right_corners_tuples[i][1]<=width-8 and right_corners_tuples[i][1]>=7 and right_corners_tuples[i][0]<=height-8:
                newTuples_R.append(right_corners_tuples[i])
            
    return newTuples_L,newTuples_R


# return matching descriptor with sum of value - mean 
#@pysnooper.snoop()
def precomputeMatchingDescriptor(newTuples,image,width,height,wid = 7):
    disc = []
    i = 0
    for tuple in newTuples:
        y = tuple[0]
        x = tuple[1]
        img = []
        img = np.array(image)
        patch = img[y-wid:y+wid+1,x-wid:x+wid+1]
        flattend = patch.flatten()
        disc.append(flattend)
        #print(len(flattend))
    
    #print(len(disc))
    return disc

#input descriptors from both images
#output a tuple ((y_L,x_L,C),(y_R,x_R,C),NCC)
def match(left,right,left_tuples,right_tuples,threshold = 0.9):
    print('entered Match')
    #i means the index in left descriptor list
    #j means index in right descriptor list

    putativeMatches = []
    left_list,left_sqr,right_list,right_sqr = calculateMinusMeanandSqr(left,right)
    for i in range(len(left)):
        bestMatch = (0,0,0)
        secondBestMatch = (0,0,0)
        for j in range(len(right)):
            newNcc = calculateNCC(left_list[i],left_sqr[i],right_list[j],right_sqr[j])

            if bestMatch[2]<newNcc:
                secondBestMatch = bestMatch
                bestMatch = (i,j,newNcc)
            if secondBestMatch[2]<newNcc and bestMatch[2]>newNcc:
                secondBestMatch = (i,j,newNcc)
                
        
        if secondBestMatch[2]/bestMatch[2]<threshold:
            #print(bestMatch)
            putativeMatches.append((left_tuples[bestMatch[0]],right_tuples[bestMatch[1]],bestMatch[2]))
    # print(putativeMatches)
    return putativeMatches,left_list,right_list

    
                
def calculateNCC(left_list,left_sqr,right_list,right_sqr):
    top = 0
    for i in range(len(left_list)):
        top = top + left_list[i]*right_list[i]

    bottom = math.sqrt(left_sqr)*math.sqrt(right_sqr)

    return top/bottom

    

# #input two descriptors, each contain a descriptor
# def calculateNCC(desc_L,desc_R):
#     leftMean = np.mean(desc_L)
#     rightMean = np.mean(desc_R)
#     fminus_mean = []
#     gminus_mean = []
#     fminus_mean_sqr = []
#     gminus_mean_sqr = []
#     top = 0
#     bottom = 0
#     for f in desc_L:
#         for g in desc_R:
#             fminus_mean.append(f-leftMean)
#             gminus_mean.append(g-rightMean)
#             top = top + (f-leftMean)*(g-rightMean)
#             fminus_mean_sqr.append((f-leftMean)**2)
#             gminus_mean_sqr.append((g-rightMean)**2)

#     bottom = math.sqrt(sum(fminus_mean_sqr)*sum(gminus_mean_sqr))

#     return top/bottom


def calculateMinusMeanandSqr(left,right):
    left_list = []   #pre calculate the fi-fmean
    right_list = []     #pre calculate the gi-gmean
    left_sqr = []
    right_sqr = []


    gminus_mean = []
    gminus_mean_sqr = []
    for desc_L in left:
        leftMean = np.mean(desc_L)
        fminus_mean = []
        fminus_mean_sqr = []
        for f in desc_L:
            fminus_mean.append(f-leftMean)
            fminus_mean_sqr.append((f-leftMean)**2)
        left_list.append(fminus_mean)
        left_sqr.append(sum(fminus_mean_sqr))
    
    for desc_R in right:
        rightMean = np.mean(desc_R)
        gminus_mean = []
        gminus_mean_sqr = []
        for g in desc_R:
            rightMean = np.mean(desc_R)
            gminus_mean.append(g-rightMean)
            gminus_mean_sqr.append((g-rightMean)**2)
        right_list.append(gminus_mean)
        right_sqr.append(sum(gminus_mean_sqr))

    return left_list,left_sqr,right_list,right_sqr

            