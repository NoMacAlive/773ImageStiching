import pandas as pd
import random

def readPhase1Result():
    df1 = pd.read_csv('phase1outputL.csv')
    df2 = pd.read_csv('phase1outputR.csv')
    # print(df.values)
    list_of_tuplesL = []
    list_of_tuplesR = []
    for index, row in df1.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        newtup = (x,y,row['C'])
        temp = tuple(newtup)
        list_of_tuplesL.append(temp)
    
    for index, row in df2.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        newtup = (x,y,row['C'])
        temp = tuple(newtup)
        list_of_tuplesR.append(temp)

    return list_of_tuplesL,list_of_tuplesR

def readPhase2Result():
    putativeMatches = []
    df1 = pd.read_csv('phase2Resultleft.csv')
    df2 = pd.read_csv('phase2Resultright.csv')
    # print(df.values)
    list_of_tuplesL = []
    list_of_tuplesR = []
    for index, row in df1.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        newtup = (x,y,row['NCC'])
        temp = tuple(newtup)
        list_of_tuplesL.append(temp)
    
    for index, row in df2.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        newtup = (x,y,row['NCC'])
        temp = tuple(newtup)
        list_of_tuplesR.append(temp)

    i=0
    for left_tuple in list_of_tuplesL:
        putativeMatches.append([left_tuple,list_of_tuplesR[i]])
        i = i + 1
    return putativeMatches
        

# if __name__ == "__main__":
#     readPhase2Result()