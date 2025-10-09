import numpy as np
import plotly.graph_objects as go


def PlotArrow(start, vector, style='r-', 
              fig=None, 
              shaft_width=3, 
              head_size=0.2,
              name=None):
    """
    Draw a 3D arrow defined by a start point and a direction vector using Plotly.

    Parameters:
        start: shape (3,)
            Arrow starting point(s) [x0, y0, z0].
        vector: shape (3,)
            Direction vector(s) [u, v, w].
        style: str
            e.g., 'k--', 'b:', 'r-'.
        fig: go.Figure or None
            Existing figure to draw on. If None, a new figure will be created.
        shaft_width: int
            Line width of the arrow shaft.
        head_size: float
            Size of the arrowhead relative to vector length.

    Returns:
        fig : plotly.graph_objects.Figure
    """

    # Create a new figure if not provided
    if fig is None:
        fig = go.Figure()
    
    if name is None:
        name = "Direction"

    x0, y0, z0 = start
    u, v, w = vector

    # Compute arrow endpoint
    x1, y1, z1 = x0 + u, y0 + v, z0 + w
    
    line_style=style_map(style, shaft_width)
    # Arrow shaft (as a 3D line)
    fig.add_trace(go.Scatter3d(
        x=[x0, x1],
        y=[y0, y1],
        z=[z0, z1],
        mode='lines',
        line=line_style,

        name=name,
        legendgroup=name,
        showlegend=False,
    ))

    # Skip zero-length vectors
    vec_len = np.linalg.norm(vector)
    if vec_len == 0:
        return fig

    # Normalize direction
    u_n, v_n, w_n = np.array([u, v, w]) / vec_len

    # Arrowhead (as a cone)
    head_pos = np.array([x1, y1, z1])
    fig.add_trace(go.Cone(
        x=[head_pos[0]],
        y=[head_pos[1]],
        z=[head_pos[2]],
        u=[u_n],
        v=[v_n],
        w=[w_n],
        colorscale=[[0, line_style['color']], 
                    [1, line_style['color']]],
        sizemode="absolute",
        sizeref=vec_len * head_size,
        showscale=False,

        name=name,
        legendgroup=name,
        showlegend=True,
    ))

    # Make x-y axes scale equally
    # Ensure equal aspect ratio for X and Y axes
    F_x = [x0, x1]
    F_y = [y0, y1]
    x_range = max(F_x)-min(F_x)
    y_range = max(F_y)-min(F_y)
    if fig.layout.scene.xaxis.range is None: # for new fig
        x_limits = [min(F_x), max(F_x)]
    else: # for existing fig
        x_limits = [min(min(F_x)-0.1*x_range, min(fig.layout.scene.xaxis.range)), 
                    max(max(F_x)+0.1*x_range, max(fig.layout.scene.xaxis.range))]

    if fig.layout.scene.yaxis.range is None: # for new fig
        y_limits = [min(F_y), max(F_y)]
    else: # for existing fig
        y_limits = [min(min(F_y)-0.1*y_range, min(fig.layout.scene.yaxis.range)), 
                    max(max(F_y)+0.1*y_range, max(fig.layout.scene.yaxis.range))]
        
    
    x_ratio=float((x_limits[1]-x_limits[0])/(y_limits[1]-y_limits[0]))
    fig.update_layout(
        scene = dict(
                xaxis=dict(range=x_limits), # Set range for X axis
                yaxis=dict(range=y_limits), # Set range for Y axis
                aspectmode="manual",
                aspectratio=dict(x=x_ratio, y=1)  # X:Y:Z = 1:1:?
                # aspectmode='data'
                ),
        margin=dict(l=5, r=5, b=5, t=10)
    )
    return fig



def style_map(style, linewidth):
    """
    Maps Matplotlib-style line styles to Plotly line properties.

    Args:
        style (str): Matplotlib-style shorthand (e.g., 'k--', 'b:', 'r-').

    Returns:
        dict: Plotly line properties (color and dash).
    """
    color_map = {
        'k': 'black',
        'b': 'blue',
        'r': 'red',
        'g': 'green',
        'y': 'yellow',
        'm': 'magenta',
        'c': 'cyan',
        'w': 'white'
    }

    dash_map = {
        '-': 'solid',
        '--': 'dash',
        '- -': 'longdash',
        ':': 'dot',
        '-.': 'dashdot',
        '--.': 'longdashdot'
    }

    color = color_map.get(style[0], 'black')  # Default to black if color not found
    dash = dash_map.get(style[1:], 'solid')  # Default to solid if dash not found

    return {'color': color, 'dash': dash, 'width': linewidth}