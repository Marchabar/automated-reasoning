import plotly.graph_objects as go

# Canvas dimensions
canvas_width = 30
canvas_height = 30

# Poster information: (x, y, width, height, rotated)
posters = [
    (6, 19, 4, 5, False),  # Poster 1
    (6, 24, 4, 6, False),  # Poster 2
    (0, 1, 5, 21, False),  # Poster 3
    (15, 1, 6, 9, False),  # Poster 4
    (0, 22, 6, 8, False),  # Poster 5
    (5, 1, 6, 10, True),   # Poster 6
    (24, 9, 6, 11, False), # Poster 7
    (5, 7, 7, 12, False),  # Poster 8
    (21, 1, 8, 9, True),   # Poster 9
    (12, 10, 10, 11, True),# Poster 10
    (10, 20, 10, 20, True) # Poster 11
]

# Vertical line position
vertical_line_x = 13

# List of soft colors for each poster
soft_colors = [
    "lightblue", "lightgreen", "lightpink", "lightcoral", "lightgoldenrodyellow", 
    "lightcyan", "lightgray", "lightseagreen", "lightsalmon", "lightsteelblue", "lightyellow"
]

# Create figure
fig = go.Figure()

# Draw posters
for i, (x, y, width, height, rotated) in enumerate(posters, 1):
    if rotated:
        width, height = height, width  # Swap if rotated
    fig.add_shape(
        type="rect",
        x0=x, y0=y, x1=x + width, y1=y + height,
        line=dict(color="blue"),
        fillcolor=soft_colors[i-1],  # Assign soft color to each rectangle
        opacity=0.5  # Make the color slightly transparent for softness
    )
    # Add label to the poster
    fig.add_annotation(
        x=x + width / 2, y=y + height / 2,
        text=f'P{i}', showarrow=False, font=dict(size=10),
    )

# Draw the vertical line
fig.add_shape(
    type="line",
    x0=vertical_line_x, y0=0, x1=vertical_line_x, y1=canvas_height,
    line=dict(color="red", dash="dash"),
)


# Update layout for canvas
fig.update_layout(
    title="Canvas with Posters and Vertical Line at x=13",
    xaxis=dict(range=[0, canvas_width], showgrid=True),
    yaxis=dict(range=[0, canvas_height], scaleanchor="x", scaleratio=1, showgrid=True),
    showlegend=False,
    width=600, height=600,
)

# Show the figure
fig.show()
