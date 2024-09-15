from z3 import *

square = Int("square")
triangle = Int("triangle")
circle = Int("circle")

solver = Solver()

solver.add(square * square + circle == 16)
solver.add(triangle * triangle * triangle == 27)
solver.add(triangle * square == 6)

if solver.check() == sat:
    model = solver.model()

    circle_value = model.eval(circle).as_long()
    square_value = model.eval(square).as_long()
    triangle_value = model.eval(triangle).as_long()

    result = circle_value * square_value * triangle_value
    print("The solution is: " + str(result))
else:
    print("No solution found")
