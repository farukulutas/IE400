import gurobipy as gp
from gurobipy import *
import numpy as np

m = gp.Model()
ownedcities = [0, 1, 2, 3, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 25, 26, 27, 33, 34]
num_rows = 5
num_cols = 7
seats = {}
seat_count = {}
n = 35

seats = m.addVars(7, vtype=gp.GRB.BINARY, name="seat")
seat_count = m.addVars(7, vtype=gp.GRB.INTEGER, name="seat_count")

A = m.addVars(n, vtype=gp.GRB.BINARY, name="A")
B = m.addVars(n, vtype=gp.GRB.BINARY, name="B")
C = m.addVars(n, vtype=gp.GRB.BINARY, name="C")
D = m.addVars(n, vtype=gp.GRB.BINARY, name="D")
E = m.addVars(n, vtype=gp.GRB.BINARY, name="E")
F = m.addVars(n, vtype=gp.GRB.BINARY, name="F")
G = m.addVars(n, vtype=gp.GRB.BINARY, name="G")

m.setObjective(gp.quicksum(seats[col] for col in seats), GRB.MAXIMIZE)

m.addConstr(gp.quicksum(A) == 5, name='5A')
m.addConstr(gp.quicksum(B) == 5, name='5B')
m.addConstr(gp.quicksum(C) == 5, name='5C')
m.addConstr(gp.quicksum(D) == 5, name='5D')
m.addConstr(gp.quicksum(E) == 5, name='5E')
m.addConstr(gp.quicksum(F) == 5, name='5F')
m.addConstr(gp.quicksum(G) == 5, name='5G')

m.addConstrs((A[i] + B[i] + C[i] + D[i] + E[i] + F[i] + G[i] <= 1
             for i in range(n)), name='ONE CITY')

for i in range(5):
    m.addConstr(F[i * 7] == 1, name='F')
    m.addConstr(G[(i + 1) * 7 - 1] == 1, name='G')

    
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        neighbors = []
        if i > 0:
            neighbors.append((i - 1) * num_cols + j)
        if i < num_rows - 1:
            neighbors.append((i + 1) * num_cols + j)
        if j > 0:
            neighbors.append(i * num_cols + (j - 1))
        if j < num_cols - 1:
            neighbors.append(i * num_cols + (j + 1))

        m.addConstr(gp.quicksum(A[neighbor] for neighbor in neighbors) >= A[index])
        m.addConstr(gp.quicksum(B[neighbor] for neighbor in neighbors) >= B[index])
        m.addConstr(gp.quicksum(C[neighbor] for neighbor in neighbors) >= C[index])
        m.addConstr(gp.quicksum(D[neighbor] for neighbor in neighbors) >= D[index])
        m.addConstr(gp.quicksum(E[neighbor] for neighbor in neighbors) >= E[index])

for i in range(num_rows):
    for j in range(num_cols-1):
        index = i * num_cols + j
        neighbors = []
        if i > 0:
            neighbors.append((i-1)*num_cols+j)
            neighbors.append((i-1)*num_cols+(j+1))
        if i < num_rows-1:
            neighbors.append((i+1)*num_cols+j)
            neighbors.append((i+1)*num_cols+(j+1))
        if j > 0:
            neighbors.append(i*num_cols+(j-1))
        if j < num_cols-2:
            neighbors.append(i*num_cols+(j+2))

        m.addConstr(gp.quicksum(A[neighbor] for neighbor in neighbors) >= A[index])
        m.addConstr(gp.quicksum(B[neighbor] for neighbor in neighbors) >= B[index])
        m.addConstr(gp.quicksum(C[neighbor] for neighbor in neighbors) >= C[index])
        m.addConstr(gp.quicksum(D[neighbor] for neighbor in neighbors) >= D[index])
        m.addConstr(gp.quicksum(E[neighbor] for neighbor in neighbors) >= E[index])   

for i in range(num_rows-1):
    for j in range(num_cols):
        index = i * num_cols + j
        neighbors = []
        if i > 0:
            neighbors.append((i-1)*num_cols+j)
        if i < num_rows-2:
            neighbors.append((i+2)*num_cols+j)
        if j > 0:
            
            neighbors.append(i*num_cols+(j-1))
            neighbors.append((i+1)*num_cols+(j-1))
        if j < num_cols-1:
            neighbors.append(i*num_cols+(j+1))
            neighbors.append((i+1)*num_cols+(j+1))

            
        m.addConstr(gp.quicksum(A[neighbor] for neighbor in neighbors) >= A[index])
        m.addConstr(gp.quicksum(B[neighbor] for neighbor in neighbors) >= B[index])
        m.addConstr(gp.quicksum(C[neighbor] for neighbor in neighbors) >= C[index])
        m.addConstr(gp.quicksum(D[neighbor] for neighbor in neighbors) >= D[index])
        m.addConstr(gp.quicksum(E[neighbor] for neighbor in neighbors) >= E[index])


m.addConstr(seat_count[0] == gp.quicksum(A[i] for i in ownedcities), name='A seat c')
m.addConstr(seat_count[1] == gp.quicksum(B[i] for i in ownedcities), name='B seat c')
m.addConstr(seat_count[2] == gp.quicksum(C[i] for i in ownedcities), name='C seat c')
m.addConstr(seat_count[3] == gp.quicksum(D[i] for i in ownedcities), name='D seat c')
m.addConstr(seat_count[4] == gp.quicksum(E[i] for i in ownedcities), name='E seat c')
m.addConstr(seat_count[5] == gp.quicksum(F[i] for i in ownedcities), name='F seat c')
m.addConstr(seat_count[6] == gp.quicksum(G[i] for i in ownedcities), name='G seat c')

m.addConstr(seats[0] == seat_count[0] - 2, name='A seat')
m.addConstr(seats[1] == seat_count[1] - 2, name='B seat')
m.addConstr(seats[2] == seat_count[2] - 2, name='C seat')
m.addConstr(seats[3] == seat_count[3] - 2, name='D seat')
m.addConstr(seats[4] == seat_count[4] - 2, name='E seat')
m.addConstr(seats[5] == seat_count[5] - 2, name='F seat')
m.addConstr(seats[6] == seat_count[6] - 2, name='G seat')


m.optimize()
print("A:")
a_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        a_matrix[i][j] = A[index].x
print(a_matrix)

print("B:")
b_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        b_matrix[i][j] = B[index].x
print(b_matrix)

print("C:")
c_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        c_matrix[i][j] = C[index].x
print(c_matrix)

print("D:")
d_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        d_matrix[i][j] = D[index].x
print(d_matrix)

print("E:")
e_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        e_matrix[i][j] = E[index].x
print(e_matrix)

print("F:")
f_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        f_matrix[i][j] = F[index].x
print(f_matrix)

print("G:")
g_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        g_matrix[i][j] = G[index].x
print(g_matrix)

print("seats boolean:")
s_matrix = np.zeros((num_cols, 1))
for i in range(num_cols):
    s_matrix[i] = seats[i].x
print(s_matrix)

print("vote count:")
s_matrix = np.zeros((num_cols, 1))
for i in range(num_cols):
    s_matrix[i] = seat_count[i].x
print(s_matrix)
