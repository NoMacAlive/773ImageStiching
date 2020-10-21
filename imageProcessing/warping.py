import numpy as np
import math
def warpImage(H, Left_image,Right_image):
    # H = np.array([[1.34,-0.02,-277.56],[0.12,1.18,-60.5],[0.12,0.000001,1]])
    print(H)
    height = len(Left_image)
    width = len(Left_image[0])
    stitchedImage = [[0 for i in range(width*2)] for j in range(height)]
    i = 0
    
    for y in range(height):
        for x in range(2*width):
            printMa = False
            
            # forward warping
            mappedPoint = np.array([x,y,1])
            sourcePoint = H.dot(np.transpose(mappedPoint))
            point = [sourcePoint[0]/sourcePoint[2],sourcePoint[1]/sourcePoint[2]]
            
            map_x = point[0]
            map_y = point[1]
            # if(x > width and y>200 and i<50):
            #     printMa = True
            #     print("_x: "+str(x)+" _y: "+str(y))
            #     print("map_x: "+map_x.astype('str')+" map_y: "+map_y.astype('str') + " sourcePoint: "+sourcePoint[0].astype('str'))
            #     i = i + 1
            # bilinear interpolation
            x1 = math.floor(map_x)
            x2 = math.ceil(map_x)
            y1 = math.floor(map_y)
            y2 = math.ceil(map_y)
            a = map_x - x1
            b = y2 - map_y


            In_Left_Not_In_Right = (x < width-1 and y < height-1 and ( map_x < 0 or map_y < 0 or map_x > width-1 or map_y > height-1))

            In_Left_mapped_In_Right = (y < height-1 and x < width-1 and map_x >= 0 and map_y >= 0 and map_x < width-1 and map_y < height-1)

            Not_In_Left_mapped_Not_In_Right = (x > width-1 and( map_x < 0 or map_y < 0 or map_x > width-1 or map_y > height-1))

            Not_In_Left_In_Right = (x > width-1 and map_x < width-1 and map_y < height-1 and map_x >= 0 and map_y >= 0)


            if (In_Left_Not_In_Right): #outside right image and in left
                stitchedImage[y][x] = Left_image[y][x]
            elif (Not_In_Left_mapped_Not_In_Right): #source outside of left and mapped outside right
                stitchedImage[y][x] = 0.0
            elif (In_Left_mapped_In_Right):
                intensity = (1-a)*(1-b)*Right_image[y2][x1] + a*(1-b) * Right_image[y2][x2] + (1-a)*b*Right_image[y1][x1] + a*b*Right_image[y1][x2]
                stitchedImage[y][x] = Left_image[y][x]*0.5 + intensity*0.5
            elif (Not_In_Left_In_Right):
                stitchedImage[y][x] = (1-a)*(1-b)*Right_image[y2][x1] + a*(1-b) * Right_image[y2][x2] + (1-a)*b*Right_image[y1][x1] + a*b*Right_image[y1][x2]
                # print(map_x,map_y)

    return stitchedImage

            
