import pandas as pd


df_L = pd.read_csv('phase1outputL.csv', delimiter=',')
df_R = pd.read_csv('phase1outputR.csv', delimiter=',')
C_L_tuples = [tuple(row) for row in df_L.values]
C_R_tuples = [tuple(row) for row in df_R.values]

print(C_L_tuples)