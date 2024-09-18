import plotly.graph_objects as go

# Canvas dimensions
canvas_width = 30
canvas_height = 30

# Poster information: (x, y, width, height, rotated)
posters = [
    (20, 25, 4, 5, False),  # Poster 1
    (20, 19, 4, 6, False),  # Poster 2
    (25, 0, 5, 21, False),  # Poster 3
    (24, 21, 6, 9, False),  # Poster 4
    (17, 0, 6, 8, False),  # Poster 5
    (8, 14, 6, 10, True),  # Poster 6
    (18, 8, 6, 11, False),  # Poster 7
    (10, 0, 7, 12, False),  # Poster 8
    (0, 11, 8, 9, False),  # Poster 9
    (0, 0, 10, 11, False),  # Poster 10
    (0, 20, 10, 20, True),  # Poster 11
]

# Vertical line position
vertical_line_x = 24

# List of soft colors for each poster
soft_colors = [
    "lightblue",
    "lightgreen",
    "lightpink",
    "lightcoral",
    "lightgoldenrodyellow",
    "lightcyan",
    "lightgray",
    "lightseagreen",
    "lightsalmon",
    "lightsteelblue",
    "lightyellow",
]

# Create figure
fig = go.Figure()

# Draw posters
for i, (x, y, width, height, rotated) in enumerate(posters, 1):
    if rotated:
        width, height = height, width  # Swap if rotated
    fig.add_shape(
        type="rect",
        x0=x,
        y0=y,
        x1=x + width,
        y1=y + height,
        line=dict(color="blue"),
        fillcolor=soft_colors[i - 1],  # Assign soft color to each rectangle
        opacity=0.5,  # Make the color slightly transparent for softness
    )
    # Add label to the poster
    fig.add_annotation(
        x=x + width / 2,
        y=y + height / 2,
        text=f"P{i}",
        showarrow=False,
        font=dict(size=10),
    )

# Draw the vertical line
fig.add_shape(
    type="line",
    x0=vertical_line_x,
    y0=0,
    x1=vertical_line_x,
    y1=canvas_height,
    line=dict(color="red", dash="dash"),
)


# Update layout for canvas
fig.update_layout(
    title=f"Canvas with Posters and Vertical Line at {vertical_line_x}",
    xaxis=dict(range=[0, canvas_width], showgrid=True),
    yaxis=dict(range=[0, canvas_height], scaleanchor="x", scaleratio=1, showgrid=True),
    showlegend=False,
    width=600,
    height=600,
)

# Show the figure
fig.show()
