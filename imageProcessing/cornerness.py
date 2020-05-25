
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