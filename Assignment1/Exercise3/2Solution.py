from z3 import *

'''
THINGS WE ASSUME:
1) the truck can either leave food supply to a village or not
2) if the truck leave food supply it can either leave only one package or its full load
3) When the truck goes in S it fully loads
'''

# Number of steps
N = 59

# Truck location variables for each step
T_a = [Bool(f'T_a_{i}') for i in range(N)]  # Truck at village A at step i
T_b = [Bool(f'T_b_{i}') for i in range(N)]  # Truck at village B at step i
T_c = [Bool(f'T_c_{i}') for i in range(N)]  # Truck at village C at step i
T_s = [Bool(f'T_s_{i}') for i in range(N)]  # Truck at village S at step i

# Capacity of the villages for each step
capacity_A = [Int(f'capacity_A_{i}') for i in range(N)]
capacity_B = [Int(f'capacity_B_{i}') for i in range(N)]
capacity_C = [Int(f'capacity_C_{i}') for i in range(N)]

# Truck's capacity for each step
truck_capacity = [Int(f'truck_capacity_{i}') for i in range(N)]

# Solver
s = Solver()

# Maximum capacities of the villages
max_capacity_A = 90
max_capacity_B = 120
max_capacity_C = 90
max_truck_capacity = 150

# Initial conditions at step 0
s.add(capacity_A[0] == 60)
s.add(capacity_B[0] == 60)
s.add(capacity_C[0] == 60)
s.add(truck_capacity[0] == 150)

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

# Declare a variable k for each transition
k_SA = [Int(f'k_SA_{i}') for i in range(N)]
k_SC = [Int(f'k_SC_{i}') for i in range(N)]
k_AS = [Int(f'k_AS_{i}') for i in range(N)]
k_AC = [Int(f'k_AC_{i}') for i in range(N)]
k_AB = [Int(f'k_AB_{i}') for i in range(N)]
k_CS = [Int(f'k_CS_{i}') for i in range(N)]
k_CA = [Int(f'k_CA_{i}') for i in range(N)]
k_CB = [Int(f'k_CB_{i}') for i in range(N)]
k_BC = [Int(f'k_BC_{i}') for i in range(N)]
k_BA = [Int(f'k_BA_{i}') for i in range(N)]

# Add constraints for all k_ variables
for k in (k_SA, k_SC, k_AS, k_AC, k_AB, k_CS, k_CA, k_CB, k_BC, k_BA):
    for i in range(N):
        s.add(And(k[i] >= 0, k[i] <= max_truck_capacity))

# Truck starts at village S
s.add(T_s[0] == True)
s.add(T_a[0] == False)
s.add(T_b[0] == False)
s.add(T_c[0] == False)

for i in range(N):
    s.add(capacity_A[i] >= 0)
    s.add(capacity_B[i] >= 0)
    s.add(capacity_C[i] >= 0)
    s.add(truck_capacity[i] >= 0)
    s.add(capacity_A[i] <= 90)
    s.add(capacity_B[i] <= 120)
    s.add(capacity_C[i] <= 90)
    s.add(truck_capacity[i] <= 150)

# Constraints for each step
for i in range(N-1):  # Loop over each step
    # Ensure truck is in exactly one village at each step
    s.add(Or(T_a[i], T_b[i], T_c[i], T_s[i]))  # Truck must be somewhere

    s.add(And(
        Implies(T_a[i], And(Not(T_b[i]), Not(T_c[i]), Not(T_s[i]))),  # If T_a is true, others are false
        Implies(T_b[i], And(Not(T_a[i]), Not(T_c[i]), Not(T_s[i]))),  # If T_b is true, others are false
        Implies(T_c[i], And(Not(T_a[i]), Not(T_b[i]), Not(T_s[i]))),  # If T_c is true, others are false
        Implies(T_s[i], And(Not(T_a[i]), Not(T_b[i]), Not(T_c[i])))   # If T_s is true, others are false
    ))

    s.add(Implies(T_s[i], Or(
        And(T_a[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_SA, 
            Or(And(capacity_A[i+1] == capacity_A[i] - time_SA + k_SA[i], truck_capacity[i+1] == truck_capacity[i] - k_SA[i])),
            capacity_C[i+1] == capacity_C[i] - time_SA),
        And(T_c[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_SC, 
            capacity_A[i+1] == capacity_A[i] - time_SC, 
            Or(And(capacity_C[i+1] == capacity_C[i] - time_SC + k_SC[i], truck_capacity[i+1] == truck_capacity[i] - k_SC[i])),
            ))))
    
    s.add(Implies(T_a[i], Or(
        And(T_b[i+1], 
            Or(And(capacity_B[i+1] == capacity_B[i] - time_AB + k_AB[i], truck_capacity[i+1] == truck_capacity[i] - k_AB[i])),
            capacity_A[i+1] == capacity_A[i] - time_AB, 
            capacity_C[i+1] == capacity_C[i] - time_AB),
        And(T_s[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_AS, 
            capacity_A[i+1] == capacity_A[i] - time_AS, 
            capacity_C[i+1] == capacity_C[i] - time_AS),
        And(T_c[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_AC, 
            capacity_A[i+1] == capacity_A[i] - time_AC, 
            Or(And(capacity_C[i+1] == capacity_C[i] - time_AC + k_AC[i], truck_capacity[i+1] == truck_capacity[i] - k_AC[i])),
            ))))

    s.add(Implies(T_b[i], Or(
        And(T_c[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_BC, 
            capacity_A[i+1] == capacity_A[i] - time_BC, 
            Or(And(capacity_C[i+1] == capacity_C[i] - time_BC + k_BC[i], truck_capacity[i+1] == truck_capacity[i] - k_BC[i]))
            ),
        And(T_a[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_BA, 
            Or(And(capacity_A[i+1] == capacity_A[i] - time_BA + k_BA[i], truck_capacity[i+1] == truck_capacity[i] - k_BA[i])),
            capacity_C[i+1] == capacity_C[i] - time_BA))))

    s.add(Implies(T_c[i], Or(
        And(T_b[i+1], 
            Or(And(capacity_B[i+1] == capacity_B[i] - time_CB + k_CB[i], truck_capacity[i+1] == truck_capacity[i] - k_CB[i])),
            capacity_A[i+1] == capacity_A[i] - time_CB, 
            capacity_C[i+1] == capacity_C[i] - time_CB),
        And(T_s[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_CS, 
            capacity_A[i+1] == capacity_A[i] - time_CS, 
            capacity_C[i+1] == capacity_C[i] - time_CS),
        And(T_a[i+1], 
            capacity_B[i+1] == capacity_B[i] - time_CA, 
            Or(And(capacity_A[i+1] == capacity_A[i] - time_CA + k_CA[i], truck_capacity[i+1] == truck_capacity[i] - k_CA[i])), 
            capacity_C[i+1] == capacity_C[i] - time_CA))))
    

    s.add(And(capacity_A[i+1] != 0, capacity_B[i+1] != 0, capacity_C[i+1] != 0))



# Check if it's possible to have valid transitions
if s.check() == sat:
    print("Satisfiable:")
    
    model = s.model()
    
    # Organize and print the results by steps
    for i in range(N-1):
        print(f"Step {i}:")
        # Check where the truck is at step i
        if model.evaluate(T_a[i]):
            print("Truck is at village A")
        elif model.evaluate(T_b[i]):
            print("Truck is at village B")
        elif model.evaluate(T_c[i]):
            print("Truck is at village C")
        elif model.evaluate(T_s[i]):
            print("Truck is at village S")
        # Print capacities at this step
        print(f"Capacity A: {model[capacity_A[i]]}")
        print(f"Capacity B: {model[capacity_B[i]]}")
        print(f"Capacity C: {model[capacity_C[i]]}")
        print(f"Truck capacity: {model[truck_capacity[i]]}\n")
else:
    print("Unsatisfiable")

