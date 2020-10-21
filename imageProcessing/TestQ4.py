import numpy as np
def computeDerivative(pixel_array, image_width, image_height, kernelAlongX = [], kernelAlongY = []):

    kernelAlongX = np.array(
        [[-1, 0, 1], 
        [-2, 0, 2], 
        [-1, 0, 1 ]])
    kernelAlongY = np.array(
        [[-1, -2, -1], 
        [0, 0, 0], 
        [1, 2, 1 ]])

    # two pass algorithm for separable convolutions

    Ix = [[0 for i in range(image_width)] for j in range(image_height)]
    Iy = [[0 for i in range(image_width)] for j in range(image_height)]
    kernel_offset = 3//2
    #print("ntap kernel offset", kernel_offset)

    for y in range(image_height):
        for x in range(image_width):
            if x >= kernel_offset and x < image_width - kernel_offset and y >= kernel_offset and y < image_height - kernel_offset :
                convolution = 0.0
                for yy in range(-kernel_offset, kernel_offset+1):
                    for xx in range(-kernel_offset, kernel_offset+1):
                        convolution = convolution + kernelAlongX[kernel_offset+yy,kernel_offset+xx] * pixel_array[y+yy][x+xx]
                Ix[y][x] = convolution

    kernel_offset = 3//2

    for y in range(image_height):
        for x in range(image_width):
            if x >= kernel_offset and x < image_width - kernel_offset and y >= kernel_offset and y < image_height - kernel_offset:
                convolution = 0.0
                for yy in range(-kernel_offset, kernel_offset+1):
                    for xx in range(-kernel_offset, kernel_offset+1):
                        convolution = convolution + kernelAlongY[kernel_offset+yy,kernel_offset+xx] * pixel_array[y+yy][x+xx]
                Iy[y][x] = convolution

    return Ix,Iy

def computeMComponents(Ix,Iy):
    width = len(Ix[0])
    height = len(Ix)
    Ix2 = [[0 for i in range(width)] for j in range(height)]
    Iy2 = [[0 for i in range(width)] for j in range(height)]
    Ixy = [[0 for i in range(width)] for j in range(height)]
    for y in range(height):
        for x in range(width):
            Ix2[y][x] = Ix[y][x]**2
            Iy2[y][x] = Iy[y][x]**2
            Ixy[y][x] = Ix[y][x]*Iy[y][x]
    
    return Ix2,Iy2,Ixy

def cornerscore(Ix2,Iy2,Ixy):
    width = len(Ix2[0])
    height = len(Ix2)
    C = [[0 for i in range(width)] for j in range(height)]
    R = [[0 for i in range(width)] for j in range(height)]
    alpha = 0.04
    C_tuples = []
    for y in range(height):
        for x in range(width):
            C[y][x] = Ix2[y][x] * Iy2[y][x] - (Ixy[y][x])**2 - alpha * (Ix2[y][x] + Iy2[y][x])**2
            #threshold and non maximum supression

    for y in range(height):
        for x in range(width):
            #threshold and non maximum supression
            if C[y][x]>0 and isLocalMaximum(y,x,C):
                C_tuples.append((y,x,C[y][x]))
                R[y][x] = C[y][x]


    

    C_tuples.sort(key = lambda x:x[2])
    return C,C_tuples,R

def isLocalMaximum(y,x,C):
    if y != 0 or y != len(C) or x != len(C[0]) or x != 0:
        if C[y][x] >= C[y-1][x] and C[y][x] >= C[y][x-1] and C[y][x] >= C[y][x+1] and C[y][x] >= C[y+1][x] and C[y][x] >= C[y+1][x+1] and C[y][x] >= C[y-1][x-1] and C[y][x] >= C[y+1][x-1] and C[y][x] >= C[y-1][x+1]:
            if C[y][x] > 0:
                return True
    
    return False

if __name__ == "__main__":
    I = [[0,0,2,5,9],[2,0,5,7,11],[3,4,10,13,16],[4,7,10,14,16],[10,11,15,16,23]]
    Ix,Iy = computeDerivative(I,5,5)
    Ix2,Iy2,Ixy = computeMComponents(Ix,Iy)
    C,C_tuples,R = cornerscore(Ix2,Iy2,Ixy)
    Ix = [[4,-8,-4,-1,0],[7,-6,-7,-4,0],[12,-7,-8,-8,-4],[14,-5,-6,-8,-8],[16,-5,-6,-7,-10]]
    Iy = [[11,7,5,0,1],[7,8,8,4,1],[5,7,6,8,2],[4,4,6,6,7],[-16,-14,-11,-8,-3]]
    for i in range(5):
        for j in range(5):
            print(atan2(Ix[i][j],Iy[i][j]))