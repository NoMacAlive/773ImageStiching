
from matplotlib import pyplot
from matplotlib.patches import Circle, ConnectionPatch

from timeit import default_timer as timer
import numpy as np

import imageIO.readwrite as IORW
import imageProcessing.pixelops as IPPixelOps
import imageProcessing.utilities as IPUtils
import imageProcessing.smoothing as IPSmooth
import csv
import pandas as pd
import test
#my code for sobel filter
import imageProcessing.sobelFilter as sobelFilter
#my code for cornerness
import imageProcessing.cornerness as cornerScore

#mycode for assignment 2
import imageProcessing.alignment as alignment

#my code for assignment 3
import imageProcessing.findHomography as findHomography


# util I wrote
import readCSV as readCSV
# this is a helper function that puts together an RGB image for display in matplotlib, given
# three color channels for r, g, and b, respectively
def prepareRGBImageFromIndividualArrays(r_pixel_array,g_pixel_array,b_pixel_array,image_width,image_height):
    rgbImage = []
    for y in range(image_height):
        row = []
        for x in range(image_width):
            triple = []
            triple.append(r_pixel_array[y][x])
            triple.append(g_pixel_array[y][x])
            triple.append(b_pixel_array[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage


# takes two images (of the same pixel size!) as input and returns a combined image of double the image width
def prepareMatchingImage(left_pixel_array, right_pixel_array, image_width, image_height):

    matchingImage = IPUtils.createInitializedGreyscalePixelArray(image_width * 2, image_height)
    for y in range(image_height):
        for x in range(image_width):
            matchingImage[y][x] = left_pixel_array[y][x]
            matchingImage[y][image_width + x] = right_pixel_array[y][x]

    return matchingImage




# This is our code skeleton that performs the stitching
def main():
    # filename_left_image = "./images/panoramaStitching/bryce_left_02.png"
    # filename_right_image = "./images/panoramaStitching/bryce_right_02.png"
    filename_left_image = "./images/panoramaStitching/tongariro_left_01.png"
    filename_right_image = "./images/panoramaStitching/tongariro_right_01.png"

    (image_width, image_height, px_array_left_original)  = IORW.readRGBImageAndConvertToGreyscalePixelArray(filename_left_image)
    (image_width, image_height, px_array_right_original) = IORW.readRGBImageAndConvertToGreyscalePixelArray(filename_right_image)

    start = timer()
    px_array_left = IPSmooth.computeGaussianAveraging3x3(px_array_left_original, image_width, image_height)
    px_array_right = IPSmooth.computeGaussianAveraging3x3(px_array_right_original, image_width, image_height)
    end = timer()
    print("elapsed time image smoothing: ", end - start)
    
    start = timer()
    Ixl,Iyl = sobelFilter.computeDerivative(px_array_left, image_width, image_height)
    Ixr,Iyr = sobelFilter.computeDerivative(px_array_right, image_width, image_height)

    #comput M component
    Ixl2,Iyl2,Ixyl2 = sobelFilter.computeMComponents(Ixl,Iyl)
    Ixr2,Iyr2,Ixyr2 = sobelFilter.computeMComponents(Ixr,Iyr)

    #smooth Ix2 Iy2 Ixy
    SmoothedIxl2 = IPSmooth.computeGaussianAveraging9x9(Ixl2,image_width,image_height)
    SmoothedIyl2 = IPSmooth.computeGaussianAveraging9x9(Iyl2,image_width,image_height)
    SmoothedIxyl2 = IPSmooth.computeGaussianAveraging9x9(Ixyl2,image_width,image_height)

    SmoothedIxr2 = IPSmooth.computeGaussianAveraging9x9(Ixr2,image_width,image_height)
    SmoothedIyr2 = IPSmooth.computeGaussianAveraging9x9(Iyr2,image_width,image_height)
    SmoothedIxyr2 = IPSmooth.computeGaussianAveraging9x9(Ixyr2,image_width,image_height)

    #Compute Cornerness  R is for ploting
    C_L, C_L_tuples,R_L = cornerScore.cornerscore(SmoothedIxl2,SmoothedIyl2,SmoothedIxyl2)
    C_L_tuples.reverse()
    C_L_tuples = C_L_tuples[0:1000]

    C_R, C_R_tuples,R_R = cornerScore.cornerscore(SmoothedIxr2,SmoothedIyr2,SmoothedIxyr2)
    C_R_tuples.reverse()
    C_R_tuples = C_R_tuples[0:1000]


    # with open("phase1outputL.csv","w")  as f:
    #     writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
    #     writer.writerows(C_L_tuples)
    # with open("phase1outputR.csv","w")  as f:
    #     writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
    #     writer.writerows(C_R_tuples)
    # print("wrote phase 1 results")

    # start = timer()
    # C_L_tuples,C_R_tuples = readCSV.readPhase1Result()
   



    #compute matching descriptor
    newTuples_L,newTuples_R = alignment.preProcessing(C_L_tuples,C_R_tuples,image_width,image_height)
    descriptor_L = alignment.precomputeMatchingDescriptor(newTuples_L,px_array_left,image_width,image_height)
    descriptor_R = alignment.precomputeMatchingDescriptor(newTuples_R,px_array_right,image_width,image_height)


    print('got descriptors')
    putativeMatches,left_descriptors_minused_mean,right_descriptors_minused_mean = alignment.match(descriptor_L,descriptor_R,newTuples_L,newTuples_R)
    print('got putativeMatches')
    end = timer()
    print("elapsed time image smoothing: ", end - start)

    putativeMatches = np.array(putativeMatches)
    with open("phase2Resultleft.csv","w")  as f:
        writer = csv.DictWriter(f, fieldnames = ["y", "x", "NCC"])
        writer.writeheader()
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(putativeMatches[:,0])
    
    with open("phase2Resultright.csv","w")  as f:
        writer = csv.DictWriter(f, fieldnames = ["y", "x", "NCC"])
        writer.writeheader()
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(putativeMatches[:,1])

    # read phase 2 result
    putativeMatchesRead = readCSV.readPhase2Result()
    putativeMatchesRead = np.array(putativeMatchesRead)
    # print(putativeMatchesRead)

    H,left,right = findHomography.findhomography(putativeMatchesRead)
    # putativeMatches = np.array(putativeMatches)
    # H,left,right = findHomography.findhomography(putativeMatches)
    print(H)
    # print(left)
    # print(right)
    # make sure greyscale image is stretched to full 8 bit intensity range of 0 to 255
    px_array_left = IPPixelOps.scaleTo0And255AndQuantize(px_array_left, image_width, image_height)
    px_array_right = IPPixelOps.scaleTo0And255AndQuantize(px_array_right, image_width, image_height)




    # some visualizations

    # fig1, axs1 = pyplot.subplots(1, 2)
    # axs1[0].set_title('Harris response left overlaid on orig image')
    # axs1[1].set_title('Harris response right overlaid on orig image')
    # axs1[0].imshow(px_array_left, cmap='gray')
    # axs1[1].imshow(px_array_right, cmap='gray')

    # # plot a red point in the center of each image
    # circle = Circle((image_width/2, image_height/2), 3.5, color='r')
    # axs1[0].add_patch(circle)

    # for t in C_L_tuples:
    #     circle = Circle((t[1],t[0]), 0.5, color='r')
    #     axs1[0].add_patch(circle)

    # for t in C_R_tuples:
    #     circle = Circle((t[1],t[0]), 0.5, color='r')
    #     axs1[1].add_patch(circle)

    # circle = Circle((image_width/2, image_height/2), 3.5, color='r')
    # axs1[1].add_patch(circle)

    # #pyplot.show()

    # # a combined image including a red matching line as a connection patch artist (from matplotlib\)

    matchingImage = prepareMatchingImage(px_array_left, px_array_right, image_width, image_height)

    # pyplot.imshow(matchingImage, cmap='gray')
    # ax = pyplot.gca()
    # ax.set_title("Matching image")
    # for tuple in putativeMatchesRead[:,:]:
    #     print(tuple)
    #     pointA = (tuple[0][1], tuple[0][0]) #(x,y)
    #     pointB = (tuple[1][1]+image_width, tuple[1][0])
    #     connection = ConnectionPatch(pointA, pointB, "data", edgecolor='r', linewidth=0.3)
    #     ax.add_artist(connection)

    # pyplot.show()


    # plot inliers
    pyplot.imshow(matchingImage, cmap='gray')
    ax = pyplot.gca()
    ax.set_title("Matching image")
    for i in range(len(left)):
        pointA = (int(left[i][0]),int(left[i][1])) #(x,y)
        pointB = (int(right[i][0])+image_width, int(right[i][1]))
        connection = ConnectionPatch(pointA, pointB, "data", edgecolor='r', linewidth=0.3)
        ax.add_artist(connection)

    pyplot.show()

if __name__ == "__main__":
    main()
    

