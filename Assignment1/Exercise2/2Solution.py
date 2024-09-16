from z3 import *

canvas_width = 30
canvas_height = 30

solver = Solver()

poster_sizes = [
    (4, 5),
    (4, 6),
    (5, 21),
    (6, 9),
    (6, 8),
    (6, 10),
    (6, 11),
    (7, 12),
    (8, 9),
    (10, 11),
    (10, 20),
]

num_posters = len(poster_sizes)

x = [
    Int(f"x_{i}") for i in range(num_posters)
]  # x coordinate of the bottom left corner
y = [
    Int(f"y_{i}") for i in range(num_posters)
]  # y coordinate of the bottom left corner
r = [Bool(f"r_{i}") for i in range(num_posters)]  # rotation of the poster

line_x = Int("line_x")
line_y = Int("line_y")
is_horizontal = Bool("is_horizontal")


# Constraint: line must be in the canvas
solver.add(And(line_x > 10, line_x < canvas_width - 10))
solver.add(And(line_y > 10, line_y < canvas_height - 10))

# Constraint: posters must be in the canvas taking into account the rotation
for i in range(num_posters):
    width_i, height_i = poster_sizes[i]

    rotated_width = If(r[i], height_i, width_i)
    rotated_height = If(r[i], width_i, height_i)

    solver.add(x[i] + rotated_width <= canvas_width)
    solver.add(y[i] + rotated_height <= canvas_height)
    solver.add(x[i] >= 0)
    solver.add(y[i] >= 0)


# Constraint: posters must not overlap, we check the position for each pair of them
for i in range(num_posters):
    for j in range(i + 1, num_posters):
        width_i, height_i = poster_sizes[i]
        width_j, height_j = poster_sizes[j]

        rotated_width_i = If(r[i], height_i, width_i)
        rotated_height_i = If(r[i], width_i, height_i)

        rotated_width_j = If(r[j], height_j, width_j)
        rotated_height_j = If(r[j], width_j, height_j)

        solver.add(
            Or(
                x[i] + rotated_width_i <= x[j],
                x[j] + rotated_width_j <= x[i],
                y[i] + rotated_height_i <= y[j],
                y[j] + rotated_height_j <= y[i],
            )
        )


# Constraint: the line can be covered by any poster (assume line is either vertical or horizontal)
for i in range(num_posters):
    width_i, height_i = poster_sizes[i]

    rotated_width = If(r[i], height_i, width_i)
    rotated_height = If(r[i], width_i, height_i)

    # If the line is vertical, posters must be fully to the left or right of the line_x
    vertical_constraint = Or(x[i] + rotated_width <= line_x, x[i] >= line_x)  #

    # If the line is horizontal, posters must be fully above or below the line_y
    horizontal_constraint = Or(y[i] + rotated_height <= line_y, y[i] >= line_y)

    # Only apply either the vertical or horizontal constraint depending on its position
    solver.add(If(is_horizontal, vertical_constraint, horizontal_constraint))


if solver.check() == sat:
    model = solver.model()

    for i in range(num_posters):
        print(
            f"Poster {i+1}: (x, y) = ({model[x[i]]}, {model[y[i]]}), Rotated: {model[r[i]]}"
        )

    if model[is_horizontal]:
        print("Horizontal line at y = ", model[line_y])
    else:
        print("Vertical line at x = ", model[line_x])
else:
    print("No solution found")
