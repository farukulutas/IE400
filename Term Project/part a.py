import gurobipy as gp
from gurobipy import *
import numpy as np

num_rows = 5
num_cols = 7

expectations = [
    9, 19, 26, 6, 28, 18, 25, 22, 29, 26, 27, 10, 23, 25, 9, 30, 16, 
    29, 23, 13, 10, 28, 9, 28, 22, 6, 29, 26, 21, 30, 25, 24, 12, 6, 16
]
T = 15

min_votes = 18

m = Model()

x = {}
y = {}
investment = {}
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        x[index] = m.addVar(vtype=GRB.BINARY, name="x_%d" % index)
        y[index] = m.addVar(vtype=GRB.BINARY, name="y_%d" % index)
        investment[index] = m.addVar(vtype=GRB.INTEGER,
                                     name="invest_%d" % index)
m.setObjective(gp.quicksum(investment[i] for i in range(35)), GRB.MINIMIZE)

for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        m.addConstr(x[index] >= y[index])

m.addConstr(quicksum(y[i] for i in range(num_rows * num_cols)) >= min_votes)

M = 1000000
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

        m.addConstr((investment[index] >= expectations[index] * y[index]))
        m.addConstr(
            quicksum(investment[index]
                     for index in neighbors) / len(neighbors) >= T * y[index])
        m.addConstr(quicksum(y[n] for n in neighbors) >= y[index])

        m.addConstr(x[index] * M >= investment[index])
        m.addConstr(x[index] <= investment[index])

m.optimize()
print("invested")
x_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        x_matrix[i][j] = x[index].x
print(x_matrix)

print("investment")
inv_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        inv_matrix[i][j] = investment[index].x
print(inv_matrix)

print("votes")
y_matrix = np.zeros((num_rows, num_cols))
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        y_matrix[i][j] = y[index].x
print(y_matrix)
