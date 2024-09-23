from z3 import *

solver = Optimize()

num_trucks = 6

truck_capacity = 8000
max_pallets_per_truck = 10

nuzzles = 6
prittles = 12
skipples = 15
crottles = 8

nuzzle_weight = 800
prittle_weight = 405
skipple_weight = 500
crottle_weight = 2500
dupple_weight = 600

# Variables for number of pallets of each type on each truck
nuzzles_t = [Int(f"nuzzles_{t}") for t in range(num_trucks)]
prittles_t = [Int(f"prittles_{t}") for t in range(num_trucks)]
skipples_t = [Int(f"skipples_{t}") for t in range(num_trucks)]
crottles_t = [Int(f"crottles_{t}") for t in range(num_trucks)]
dupples_t = [Int(f"dupples_{t}") for t in range(num_trucks)]

# Constraint: We can't overload the trucks capacity
for i in range(num_trucks):
    solver.add(
        nuzzles_t[i] * nuzzle_weight
        + prittles_t[i] * prittle_weight
        + skipples_t[i] * skipple_weight
        + crottles_t[i] * crottle_weight
        + dupples_t[i] * dupple_weight
        <= truck_capacity
    )

# Constraint: Each truck can only carry a maximum of 10 pallets
for i in range(num_trucks):
    solver.add(
        nuzzles_t[i] + prittles_t[i] + skipples_t[i] + crottles_t[i] + dupples_t[i]
        <= max_pallets_per_truck
    )

# Constraint: At most two trucks can carry skipples
skipple_trucks = [Bool(f"skipple_truck_{t}") for t in range(num_trucks)]
for t in range(num_trucks):
    solver.add(
        If(skipples_t[t] > 0, skipple_trucks[t] == True, skipple_trucks[t] == False)
    )

solver.add(Sum([If(skipple_trucks[t], 1, 0) for t in range(num_trucks)]) <= 2)

# Constraint: The quantity for each pallet has to be positive
for i in range(num_trucks):
    solver.add(nuzzles_t[i] >= 0)
    solver.add(prittles_t[i] >= 0)
    solver.add(skipples_t[i] >= 0)
    solver.add(crottles_t[i] >= 0)
    solver.add(dupples_t[i] >= 0)

# Constraint: Prittles must be distributed over at least five trucks
prittle_truck_count = Sum([If(prittles_t[t] > 0, 1, 0) for t in range(num_trucks)])
solver.add(prittle_truck_count >= 5)

# We have to distribute all the pallets
solver.add(Sum(nuzzles_t) == nuzzles)
solver.add(Sum(prittles_t) == prittles)
solver.add(Sum(skipples_t) == skipples)
solver.add(Sum(crottles_t) == crottles)

# Constraint: if there are crottles in a truck, then in that truck there are at least 2 dupples
for i in range(num_trucks):
    solver.add(Implies(crottles_t[i] > 0, dupples_t[i] >= 2))

# Maximize the number of dupples
dupple_num = Int("dupple_num")
solver.add(dupple_num == Sum(dupples_t))
solver.maximize(dupple_num)


if solver.check() == sat:
    model = solver.model()
    print(
        f"2. Do the same, with the extra information that crottles get too cold if there are less than two dupples in the same truck."
    )
    print(
        "Maximum number of dupple pallets",
        model.eval(dupple_num).as_long(),
    )
    for i in range(num_trucks):
        print(f"Truck {i + 1}:")
        print(f"  Nuzzles: {model[nuzzles_t[i]]}")
        print(f"  Prittles: {model[prittles_t[i]]}")
        print(f"  Skipples: {model[skipples_t[i]]}")
        print(f"  Crottles: {model[crottles_t[i]]}")
        print(f"  Dupples: {model[dupples_t[i]]}")
else:
    print("No solution found")
