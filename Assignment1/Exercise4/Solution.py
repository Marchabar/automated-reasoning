from z3 import *

# Define variables
a = Int('a')
b = Int('b')

# Initialize values
s = Solver()
a_init = 1
b_init = 1

# Loop through values of n from 1 to 10
for n in range(1, 11):
    a_val = a_init
    b_val = b_init
    
    # Iterate the loop from 1 to 10
    for i in range(1, 11):
        a_next = Int(f'a_{i}')
        b_next = Int(f'b_{i}')
        
        # Define the two branches of the unknown condition ?
        branch1 = And(a_next == a_val + 2 * b_val, b_next == b_val + 3)
        branch2 = And(a_next == a_val + i, b_next == b_val - a_next)
        
        # Add constraints that one of the branches must be true
        s.add(Xor(branch1, branch2))
        
        # Update a_val and b_val for the next iteration
        a_val = a_next
        b_val = b_next
    
    # Check crash condition after the loop
    s.push()  # Save the state before testing this n
    s.add(b_val == 210 + n)
    
    # Check if the solver can find a model (crash state)
    if s.check() == sat:
        print(f"Program crashes for n = {n}")
        
        # Get the model (i.e., values of variables)
        m = s.model()
        print('--------------------------------------------------------')
        print(f'a = {m[a_val]}')
        print(f'b = {m[b_val]}')
        
        # Show path to crash state
        print('Path to crash state:')
        print(f'Initial values: a = {a_init}, b = {b_init}')
        for i in range(1, 11):
            a_i = m[Int(f'a_{i}')]
            b_i = m[Int(f'b_{i}')]
            print(f'Step {i}: a = {a_i}, b = {b_i}')
        
        print('--------------------------------------------------------')
    else:
        print(f"Program safe for n = {n}")
    
    s.pop()  # Restore the state to test the next value of n
