"""
plot discretized trajectory.

Input:
survey: dict, solution dict of Dubins

fig: fig handle for the plot

show: if show==1, show the figure right now
      else, wait for futher plots
"""

import plotly.graph_objects as plt
import numpy as np
import pandas as pd

def PlotSurvey(survey, 
                    fig=None,
                    name= None, # name of the trajectory in the plot
                    style='k-', # line style for the trajectory
                    linewidth=1.5, 
                    width=600, height=450, # fig size
                    margin=[10,10,10,10], # [left, top, right, bottom]
                    showlegend=True, # True: show legend
                    legendgroup=None, # legend group name
                    azim=-135, elev=20, # view angle
                    show=1): # show fig immediately
    assert isinstance(survey, (pd.DataFrame, dict, np.ndarray)), \
        "survey must be a pandas DataFrame, a dictionary, or a numpy array."
    
    if not fig:
        fig = plt.Figure()
        legend_groups_num=0
    else:
        # get existing legend groups
        legend_groups = set(trace.legendgroup for trace in fig.data if trace.legendgroup)
        legend_groups_num=len(legend_groups)
    
    if name is None:
        name=f'Offset Well #{legend_groups_num+1}'
    if legendgroup is None:
        legendgroup = name

    # format survey data to numpy array [X, Y, Z, MD...]
    if isinstance(survey, pd.DataFrame) or isinstance(survey, dict):
        try:
            survey_array = np.array([survey['X'], survey['Y'], survey['Z'], survey['MD']]).T
        except:
            survey_array = np.array([survey['EAST'], survey['NORTH'], survey['TVD'], survey['MD']]).T
        assert survey_array.shape[1] == 4, "Survey data must contain at least X, Y, Z, and MD columns."

        inclination_keys = ['INCL', 'Inclination', 'Incl',  'Inc', 'incl']
        for key in inclination_keys:
            if key in survey:
                survey_array = np.column_stack((survey_array, survey[key]))
                break

        azimuth_keys = ['AZ', 'Azimuth', 'Az', 'AZIM', 'Azi', 'azi', 'AZIM_GN']
        for key in azimuth_keys:
            if key in survey:
                survey_array = np.column_stack((survey_array, survey[key]))
                break
        
        dls_keys = ['DLS', 'dls', 'Dls', 'dls_deg', 'DLS_deg']
        for key in dls_keys:
            if key in survey:
                survey_array = np.column_stack((survey_array, survey[key]))
        
        # re-assign survey
        if survey_array.shape[1] >= 4:
            survey=survey_array
        else:
            # Keep only X, Y, Z, MD if no Inclination, Azimuth, or DLS data
            survey=survey_array[:, :4]  

    # use survey np.ndarray to plot
    if type(survey) == np.ndarray:
        # define mouse hover interaction
        hovertemplate = name + "<br>East: %{x:.2f}<br>North: %{y:.2f}<br>Depth: %{z:.2f}" + \
            "<extra>MD: %{customdata[0]:.2f}"
        
        if survey.shape[1] >= 5: 
            hovertemplate += "<br>Inclination: %{customdata[1]:.2f}°" 
        if survey.shape[1] >= 6:
            hovertemplate += "<br>Azimuth: %{customdata[2]:.2f}°"
        if survey.shape[1] >= 7:
            hovertemplate +=  "<br>DLS: %{customdata[3]:.2f}°/30m "
        hovertemplate += "</extra>" 

        fig.add_trace(plt.Scatter3d(
            x=survey[:, 0],
            y=survey[:, 1],
            z=survey[:, 2],

            name=name,  # Name for the trace
            customdata= survey[:, 3:],  # Add MD, Inc, Az, F1_v, F2_v, F3_v values as customdataext
            mode='lines',
            line=style_map(style, linewidth),
            hovertemplate=hovertemplate,
            showlegend=bool(showlegend),
            legendgroup=f'{name}'  # Assign a legend group
            )
        )

    # ========================================================================================
    # ========================================================================================
    # Basic layout
    fig.update_layout(
        scene = dict( xaxis=dict(title='X (East, m)',),
                    yaxis=dict(title='Y (North, m)',),
                    zaxis=dict(title='Z (Depth, m)',),
                    # aspectmode='cube'  #
                    # aspectmode='auto', 
                    # aspectmode='data',
                    aspectratio=dict(x=1, y=1, z=1)
                ),
        width=width,
        height=height,
        margin=dict(l=margin[0],  t=margin[1], r=margin[-2], b=margin[-1]),
        )
    
    # Ensure equal aspect ratio for X and Y axes
    F_x = survey[:, 0]
    F_y = survey[:, 1]
    if fig.layout.scene.xaxis.range is None: # for new fig
        x_limits = [min(F_x), max(F_x)]
    else: # for existing fig
        x_limits = [min(min(F_x), min(fig.layout.scene.xaxis.range)), 
                    max(max(F_x), max(fig.layout.scene.xaxis.range))]

    if fig.layout.scene.yaxis.range is None: # for new fig
        y_limits = [min(F_y), max(F_y)]
    else: # for existing fig
        y_limits = [min(min(F_y), min(fig.layout.scene.yaxis.range)), 
                    max(max(F_y), max(fig.layout.scene.yaxis.range))]
        
    max_range = max(x_limits[1] - x_limits[0], y_limits[1] - y_limits[0])
    mid_x = (x_limits[0] + x_limits[1]) / 2
    mid_y = (y_limits[0] + y_limits[1]) / 2
    x_range= [mid_x - max_range / 2, mid_x + max_range / 2]
    y_range= [mid_y - max_range / 2, mid_y + max_range / 2]
    fig.update_layout(
        scene = dict(xaxis=dict(range=x_range,), # Set range for X axis
                    yaxis=dict(range=y_range,), # Set range for Y axis
                ),
        )

    # customize legend
    fig.update_layout(
        legend=dict(
            # title="Legend Title",  # Add a title to the legend
            x=0.9,  # Horizontal position (0 = left, 1 = right)
            y=0.9,  # Vertical position (0 = bottom, 1 = top)
            xanchor="left",  # Anchor the legend's left side to the x position
            yanchor="top",  # Anchor the legend's top to the y position
            bgcolor="rgba(255,255,255,0.1)",  # Background color with transparency
            # bordercolor="black",  # Border color
            # borderwidth=2,  # Border width
            font=dict(
                size=12,  # Font size
                color="black"  # Font color
                ),
            orientation="v"  # Orientation: "v" for vertical, "h" for horizontal
            )
        )

    # adjust view angle
    fig.update_layout(
        scene=dict(
            camera=dict(
                eye=dict(x=np.cos(azim/180*np.pi)*2.2, #*np.cos(elev/180*np.pi)
                        y=np.sin(azim/180*np.pi)*2.2, #*np.cos(elev/180*np.pi)
                        z=np.sin(elev/180*np.pi)*2.2) 
                )
            )
        )


    # show fig or preserve it for further modification
    if show == 1:
        fig.show()

    return fig

# ###############################################################
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