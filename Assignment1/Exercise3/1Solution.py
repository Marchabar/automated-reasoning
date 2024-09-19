from z3 import *

# Define truck's location as an integer (0 for S, 1 for A, 2 for B, 3 for C)
truck_location = Int('truck_location')

# Declare the capacities of each village
capacity_A = Int('capacity_A')
capacity_B = Int('capacity_B')
capacity_C = Int('capacity_C')
capacity_S = Int('capacity_S')  # S is self-supporting, but we track it

# Declare the truck's capacity
truck_capacity = Int('truck_capacity')

# Step counter for tracking the number of moves
steps = Int('steps')

# Solver
s = Solver()

# Maximum capacities of the villages
max_capacity_A = 90
max_capacity_B = 120
max_capacity_C = 90
max_truck_capacity = 130

# Initial conditions
s.add(capacity_A == 60)
s.add(capacity_B == 60)
s.add(capacity_C == 60)
s.add(truck_capacity == 130)
s.add(steps == 0)

# Ensure that the truck can only be in one of the four villages
s.add(Or(truck_location == 0, truck_location == 1, truck_location == 2, truck_location == 3))  # 0=S, 1=A, 2=B, 3=C

# Declare the time costs for each path
time_SA = 15
time_SC = 15
time_AS = 15
time_AC = 12
time_AB = 17
time_CS = 15
time_CA = 12
time_CB = 9
time_BC = 13
time_BA = 17

# Transitions
# If truck moves from S (0) to A (1)
s.add(Implies(truck_location == 0, And(
    capacity_A == max_capacity_A,
    capacity_B == capacity_B - time_SA,
    capacity_C == capacity_C - time_SA,
    capacity_S == capacity_S + time_SA,
    truck_capacity == truck_capacity - (max_capacity_A - capacity_A),
    truck_location == 1)))

# If truck moves from S (0) to C (3)
s.add(Implies(truck_location == 0, And(
    capacity_A == capacity_A - time_SC,
    capacity_B == capacity_B - time_SC,
    capacity_C == max_capacity_C,
    capacity_S == capacity_S + time_SC,    
    truck_capacity == truck_capacity - (max_capacity_C - capacity_C),
    truck_location == 3)))

# CHESK
# If truck moves from A (1) to S (0) (refill only)
s.add(Implies(truck_location == 1, And(
    capacity_A == capacity_A - time_AS,
    capacity_B == capacity_B - time_AS,
    capacity_C == capacity_C - time_AS,
    capacity_S == capacity_S + time_AS, 
    truck_capacity == truck_capacity + (max_truck_capacity - truck_capacity),
    capacity_S == capacity_S - (max_truck_capacity - truck_capacity),
    truck_location == 0)))

# If truck moves from A (1) to C (3)
s.add(Implies(truck_location == 1, And(
    capacity_A == capacity_A - time_AC,
    capacity_B == capacity_B - time_AC,
    capacity_C == max_capacity_C,
    capacity_S == capacity_S + time_AC,    
    truck_capacity == truck_capacity - (max_capacity_C - capacity_C),
    truck_location == 3)))

# If truck moves from A (1) to B (2)
s.add(Implies(truck_location == 1, And(
    capacity_A == capacity_A - time_AB,
    capacity_B == max_capacity_B,
    capacity_C == capacity_C - time_AB,
    capacity_S == capacity_S + time_AB,
    truck_capacity == truck_capacity - (max_capacity_B - capacity_B),
    truck_location == 2)))

# If truck moves from C (3) to A (1)
s.add(Implies(truck_location == 3, And(
    capacity_A == max_capacity_A,
    capacity_B == capacity_B - time_CA,
    capacity_C == capacity_C - time_CA,
    capacity_S == capacity_S + time_CA,
    truck_capacity == truck_capacity - (max_capacity_A - capacity_A),
    truck_location == 1)))

# If truck moves from C (3) to B (2)
s.add(Implies(truck_location == 3, And(
    capacity_A == capacity_A - time_CB,
    capacity_B == max_capacity_B,
    capacity_C == capacity_C - time_CB,
    capacity_S == capacity_S + time_CB,
    truck_capacity == truck_capacity - (max_capacity_B - capacity_B),
    truck_location == 2)))

# If truck moves from B (2) to C (3)
s.add(Implies(truck_location == 2, And(
    capacity_A == capacity_A - time_BC,
    capacity_B == capacity_B - time_BC,
    capacity_C == max_capacity_C,
    capacity_S == capacity_S + time_BC,
    truck_capacity == truck_capacity - (max_capacity_C - capacity_C),
    truck_location == 3)))

# If truck moves from B (2) to A (1)
s.add(Implies(truck_location == 2, And(
    capacity_A == max_capacity_A,
    capacity_B == capacity_B - time_BA,
    capacity_C == capacity_C - time_BA,
    capacity_S == capacity_S + time_BA,    
    truck_capacity == truck_capacity - (max_capacity_A - capacity_A),
    truck_location == 1)))

#CHECK IT
# If truck moves from C (3) to S (0)
s.add(Implies(truck_location == 3, And(
    capacity_A == capacity_A - time_CS,
    capacity_B == capacity_B - time_CS,
    capacity_C == capacity_C - time_CS,
    capacity_S == capacity_S + time_CS, 
    truck_capacity == truck_capacity + (max_truck_capacity - truck_capacity),
    capacity_S == capacity_S - (max_truck_capacity - truck_capacity),
    truck_location == 0)))





# Condition to check if all villages A, B, and C run out of supplies
s.add(And(capacity_A <= 0, capacity_B <= 0, capacity_C <= 0))

# Check the satisfiability of the model
if s.check() == sat:
    model = s.model()
    print("Solution found:")
    print(model)
else:
    print("No solution found")
