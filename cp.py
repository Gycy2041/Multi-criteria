from ortools.sat.python import cp_model

def distance(a, b):
    a=a-1
    b=b-1
    x_dist = model.NewIntVar(0, 9999, f"x_d{a}{b}")
    y_dist = model.NewIntVar(0, 9999, f"x_d{a}{b}")
    ah_width = int(objects[a][0] /2)
    bh_width = int(objects[b][0] /2)
    ah_height = int(objects[a][1]/2)
    bh_height = int(objects[b][1]/2)

    # model.AddAbsEquality(x_dist, (position_x[b] + objects[b][0] / 2 - position_x[a] - objects[a][0] / 2)).OnlyEnforceIf((position_x[b] + objects[b][0] / 2 - position_x[a] - objects[a][0] / 2) >=0)
    model.AddAbsEquality(x_dist, (position_x[b] + bh_width - position_x[a] - ah_width))
    model.AddAbsEquality(y_dist, (position_y[b] + int(objects[b][1] / 2) - position_y[a] - int(objects[a][1] / 2)))
    # model.Add(y_dist == (position_y[b] + objects[b][1] / 2 - position_y[a] - objects[a][1] / 2)).OnlyEnforceIf((position_y[b] + objects[b][1] / 2 - position_y[a] - objects[a][1] / 2) >=0)
    # model.Add(x_dist == -(position_x[b] + objects[b][0] / 2 - position_x[a] - objects[a][0] / 2)).OnlyEnforceIf((position_x[b] + objects[b][0] / 2 - position_x[a] - objects[a][0] / 2) <=0)
    # model.Add(y_dist == -(position_y[b] + objects[b][1] / 2 - position_y[a] - objects[a][1] / 2)).OnlyEnforceIf((position_y[b] + objects[b][1] / 2 - position_y[a] - objects[a][1] / 2) <=0)
    # x_dist = (position_x[b] + objects[b][0] / 2 - position_x[a] - objects[a][0] / 2)
    # y_dist = (position_y[b] + objects[b][1] / 2 - position_y[a] - objects[a][1] / 2)
    # dist = (position_x[b] + 1 - position_x[a] - 1) + (position_y[b] + 1 - position_y[a] - 1)
    print((a,b))
    return x_dist + y_dist


model = cp_model.CpModel()

# 示例物体
objects = [30, 30], [20, 20], [20, 20], [20, 10], [10, 10]

position_x = {}
position_y = {}


# 物体位置变量 --bottom left
for i in range(0, 5):
    position_x[i] = model.NewIntVar(0, 100 - objects[i][0], f"x_{i}")
    position_y[i] = model.NewIntVar(0, 100 - objects[i][1], f"y_{i}")

# 非重叠约束条件
ql = {}
qr = {}
qb = {}
qt = {}
z=0
for i in range(0,5):
    for j in range(i + 1, 5):

        ql[z] = model.NewBoolVar(f"left{i}{j}")
        qr[z] = model.NewBoolVar(f"right{i}{j}")
        qb[z] = model.NewBoolVar(f"bottom{i}{j}")
        qt[z] = model.NewBoolVar(f"top{i}{j}")

        model.Add(position_x[i] + objects[i][0] + 2 <= position_x[j]).OnlyEnforceIf(ql[z])
        model.Add(position_x[j] + objects[j][0] + 2 <= position_x[i]).OnlyEnforceIf(qr[z])
        model.Add(position_y[i] + objects[i][1] + 2 <= position_y[j]).OnlyEnforceIf(qb[z])
        model.Add(position_y[j] + objects[j][1] + 2 <= position_y[i]).OnlyEnforceIf(qt[z])
        model.Add(ql[z] + qr[z] + qt[z] + qb[z] == 1)
        z = z + 1


wire_length = model.NewIntVar(0, 99999, "wire_length")
model.Add(wire_length == (distance(1,2) + distance(1,3) + distance(1,4) + distance(1,5) + distance(2,5) + distance(3,5) + distance(4,5)))
objective = model.Minimize(wire_length)
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Solution:')
    print('Objective value =', solver.Value(wire_length))
    for i in range(0, 5):
        print(f"q_{i}{0} = ", solver.Value(ql[i]))
        print(f"q_{i}{1} = ", solver.Value(qr[i]))
        print(f"q_{i}{2} = ", solver.Value(qb[i]))
        print(f"q_{i}{3} = ", solver.Value(qt[i]))
        print(f"x_{i} = ", solver.Value(position_x[i]))
        print(f"y_{i} = ", solver.Value(position_y[i]))

else:
    print("No solution")
