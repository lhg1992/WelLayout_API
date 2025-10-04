"""
plot cost contour(s)

Input:
X: (?,?), 2D array, X component of grid nodes location 
Y: (?,?), 2D array, Y component of grid nodes location
Contour_Val: (?,?), 2D array, cost values at the nodes of one well
Contour_ValM: (n, ?,?), 3D array, n wells' Contour_Val



show: if show==1, show the figure right now
      else, wait for futher plots
"""
import plotly.graph_objects as go
import numpy as np

def PlotContour_plotly(X,Y,Contour_Val, 
                fig=None,
                name= None,
                width=600, height=450, # fig size
                margin=[10,10,10,10], # [left, top, right, bottom]

                showscale=False, # True: show scale color bar
                showlegend=True, # True: show legend
                legendgroup=None, # legend group name

                cmin=None, cmax=None, # color scale min and max

                azim=-135, elev=20, # view angle
                show=1, # immediately show the plot

                plotz=50): # plot contour on the plane z=plotz
    if isinstance(X, list):
        X=np.array(X, dtype=np.float64)
    if isinstance(Y, list):
        Y=np.array(Y, dtype=np.float64)
    if isinstance(Contour_Val, list):
        Contour_Val=np.array(Contour_Val, dtype=np.float64)

    if X.ndim==1: # if X is 1D array, convert it to 2D array
        n2=np.sum(Y==Y[0])
        n1=Y.shape[0]//n2
        X=X.reshape(n1,n2)
        Y=Y.reshape(n1,n2)
        Contour_Val=Contour_Val.reshape(n1,n2)

    if not fig: # if it's a new figure
        fig = go.Figure()
        legend_groups_num=0
    else:
        # get existing legend groups
        legend_groups = set(trace.legendgroup for trace in fig.data if trace.legendgroup)
        legend_groups_num=len(legend_groups)
    
    if name is None:
        name=f'Cost Contour #{legend_groups_num+1}'
    if legendgroup is None:
        legendgroup = name
    # ==================================================================================
    # plot the surface(contour) using plotly
    if cmin is None:
        cmin=np.nanmin(Contour_Val.flatten().round(2))
    if cmax is None:
        cmax=np.nanmax(Contour_Val.flatten().round(2))
    # # print(f"cmin={cmin}, cmax={cmax}")
    # crange=cmax-cmin

    Z=np.full_like(Contour_Val, plotz)
    mask = np.isnan(Contour_Val) # mask for NaN values
    Z[mask]=np.nan  # apply mask to Z

    # %% go.Surface
    # # bugs：can't show irregular shape；hovertemplate no effect
    # fig.add_trace( go.Surface(
    #     x=X.round(2), 
    #     y=Y.round(2), 
    #     z=Z.round(2),# plot contour on the plane z=plotz
    #     surfacecolor=Contour_Val, # use Contour_Val as the surface color

    #     text=Contour_Val.round(2),
    #     name=name,
        
    #     colorscale='jet',
    #     cmin=cmin, # color scale minimum
    #     cmax=cmax, # color scale maximum
    #     # cmin=cmin-crange/50, #color scale precision 0.01?
    #     # cmax=cmax,
    #     # colorscale=[
    #     #         [0.00, 'rgba(0,0,0,0)'], # transparent
    #     #         [0.01, 'rgba(0,0,0,0)'], # transparent

    #     #         [0.01, 'rgb(0,0,255,1)'], # blue, non-transparent
    #     #         [0.5-0.49/3*2, 'rgb(0,127,255)'], 
    #     #         [0.5-0.49/3, 'rgb(0,255,255)'],

    #     #         [0.5, 'rgb(127,255,127)'],

    #     #         [0.5+0.5/3, 'rgb(255,255,0)'],   
    #     #         [0.5+0.5/3*2, 'rgb(255,127,0)'],    
    #     #         [1.0, 'rgb(255,0,0)'] # red, non-transparent
    #     #         ],

    #     showscale=showscale,
    #     opacity=0.8,  # <1 to make the contour plane semi-transparent

    #     hoverinfo='x+y+text+name', # works well
    #     # hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>cost: %{customdata:.2f}<br> <extra></extra>", # doesn't work

    #     legendgroup=legendgroup,
    #     showlegend=showlegend,
    #     )
    # )

    # %% go.Mesh3d
    mesh_data=surface2mesh3d(X, Y, Z, C=Contour_Val)
    fig.add_trace( go.Mesh3d(
            x=mesh_data['x'],
            y=mesh_data['y'],
            z=mesh_data['z'],
            i=mesh_data['i'],
            j=mesh_data['j'],
            k=mesh_data['k'],
            intensity=mesh_data['intensity'],
            colorscale='jet',

            text=Contour_Val.round(2),
            name=name,

            showscale=showscale,
            cmin=cmin, # color scale minimum
            cmax=cmax, # color scale maximum

            opacity=0.8,  # <1 to make the contour plane semi-transparent
            
            legendgroup=legendgroup,
            showlegend=showlegend,

            hovertemplate= name + "<br>x: %{x:.2f}<br>y: %{y:.2f}<br>cost: %{intensity:.2f}<br><extra></extra>",
            hoverlabel=dict(
                bgcolor="lightyellow",   
                font_size=14,            
                font_family="Arial",     
                font_color="black"       
            )
        )
    )
    # ==================================================================================
    # %%
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
    if fig.layout.scene.xaxis.range is None: # for new fig
        x_limits = [min(X.flatten()), max(X.flatten())]
    else: # for existing fig
        x_limits = [min(min(X.flatten()), min(fig.layout.scene.xaxis.range)), 
                    max(max(X.flatten()), max(fig.layout.scene.xaxis.range))]

    if fig.layout.scene.yaxis.range is None: # for new fig
        y_limits = [min(Y.flatten()), max(Y.flatten())]
    else: # for existing fig
        y_limits = [min(min(Y.flatten()), min(fig.layout.scene.yaxis.range)), 
                    max(max(Y.flatten()), max(fig.layout.scene.yaxis.range))]
        
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

#################################################################
#################################################################
# %%
def PlotContours_plotly(X, Y, Contour_ValM,
                        fig=None,
                        name_list= None,

                        width=600, height=450, # fig size
                        margin=[10,10,10,10], # [left, top, right, bottom]

                        showscale=False, # True: show scale color bar
                        showlegend=True, # True: show legend
                        separate=True, # True: plot each contour separately

                        azim=-135, elev=20, # view angle
                        show=1, # immediately show the plot

                        plotz=50): # plot contour on the plane z=plotz
    
    num_contour = Contour_ValM.shape[0]

    if name_list is None:
        name_list = [f'contour #{i+1}' for i in range(num_contour)]
    elif len(name_list) < num_contour:
        name_list.extend([f'contour #{i+1}' for i in range(len(name_list), num_contour)])

    if separate:
        cmin = None
        cmax = None
    else:
        cmin = np.nanmin(Contour_ValM)
        cmax = np.nanmax(Contour_ValM)

    for i in range(num_contour):
        fig=PlotContour_plotly(X,Y,Contour_ValM[i,:,:], 
                fig=fig,
                name= name_list[i],

                width=width, height=height, # fig size
                margin=margin, # [left, top, right, bottom]

                showscale=showscale, # True: show scale color bar
                showlegend=showlegend, # True: show legend
                cmin=cmin, cmax=cmax, # color scale min and max

                azim=azim, elev=elev, # view angle
                show=0, # immediately show the plot

                plotz=plotz+i*0.1, # plot on different planes
                ) 
    
    if show == 1 and fig is not None:
        fig.show()

    return fig


#################################################################
#################################################################
# %%
def PlotDangerArea(X,Y,Z,        
                fig=None,
                Color='red'):
    """
    X, Y: 2D meshgrid 
    x = np.arange(0, 3000, 50)
    y = np.arange(0, 3000, 50)
    X, Y = np.meshgrid(x, y)

    """
    if fig is None:
        fig = go.Figure()
   
   # format to Mesh3d
    mesh_data=surface2mesh3d(X, Y, Z, C=Z, dense=4)

    # 创建 Mesh3d 图形
    fig.add_trace(go.Mesh3d(
            x=mesh_data['x'],
            y=mesh_data['y'],
            z=mesh_data['z'],
            i=mesh_data['i'],
            j=mesh_data['j'],
            k=mesh_data['k'],
            name="danger zone",
            color=Color, # 固定颜色
            showlegend=True,
            opacity=0.8,
            hovertemplate= "danger zone" + "<br>x: %{x:.2f}<br>y: %{y:.2f}<br><extra></extra>", 
            )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
        ),
        # title='Mesh3d from Surface Grid',
        width=600,
        height=500,
    )

    fig.show()

    return fig




#################################################################
#################################################################
# %%
import numpy as np
from scipy.interpolate import griddata
def surface2mesh3d(X, Y, Z, C=None, dense=1):
    """
    Convert regular (X, Y, Z) and color C -> go.Mesh3d format
    x = np.arange(self.XRange[0], self.XRange[1], self.resolution)
    y = np.arange(self.YRange[0], self.YRange[1], self.resolution)
    X, Y = np.meshgrid(x, y)

    np.nan in Z and C are corresponding

    parameter:
        X, Y, Z: 2D numpy array, generated by meshgrid 
        C: 2D numpy array, default =Z

    return:
        dict:
            x, y, z: coordinate location
            i, j, k: triangle indices
            intensity: color at each node
    """
    import numpy as np
    if C is None:
        C = Z

    if dense>1: #加密效果不好，最好不用
        # 恢复原始x, y
        x = np.unique(X)
        y = np.unique(Y)

        # 加密
        x_dense = np.linspace(x.min(), x.max(), int(len(x)*dense))
        y_dense = np.linspace(y.min(), y.max(), int(len(y)*dense))

        # 新网格
        X_dense, Y_dense = np.meshgrid(x_dense, y_dense)

        # valid = ~np.isnan(Z.flatten())
        # Z_dense = griddata(
        #         (X.flatten()[valid], Y.flatten()[valid]),
        #         Z.flatten()[valid],
        #         (X_dense, Y_dense),
        #         method='nearest'
        #     )
        # C_Dense = griddata(
        #         (X.flatten()[valid], Y.flatten()[valid]),
        #         C.flatten()[valid],
        #         (X_dense, Y_dense),
        #         method='nearest'
        #     )
        
        Z_dense = griddata(
                (X.flatten(), Y.flatten()),
                Z.flatten(),
                (X_dense, Y_dense),
                method='nearest'
            )
        C_Dense = griddata(
                (X.flatten(), Y.flatten()),
                C.flatten(),
                (X_dense, Y_dense),
                method='nearest'
            )
    else:
        X_dense, Y_dense, Z_dense, C_Dense = X, Y, Z, C


    rows, cols = X_dense.shape
    x = X_dense.ravel()
    y = Y_dense.ravel()
    z = Z_dense.ravel()


    # rows, cols = X.shape
    # x = X.ravel()
    # y = Y.ravel()
    # z = Z.ravel()



    # 默认颜色使用 Z 值
    intensity = C_Dense.ravel() if C_Dense is not None else z

    # 构造三角形索引
    i, j, k = [], [], []
    for r in range(rows - 1):
        for c in range(cols - 1):
            p0 = r * cols + c
            p1 = p0 + 1
            p2 = p0 + cols
            p3 = p2 + 1

            """
            p0rc - - p0c - - p1c - - p1rc
             |        |       |       |
             |        |       |       |
            p0r - - - 0 - - - 1 - - - p1r  
             |        |       |       |
             |        |       |       |
            p2r - - - 2 - - - 3 - - - p3r
             |        |       |       |
             |        |       |       |
            p2rc - - p2c - - p3c - - p3rc
            """
            # 非np.nan个数
            count = np.count_nonzero(~np.isnan(z[[p0,p1,p2,p3]]))
            if count>=3:
                # 注意3个点的顺逆时针顺序要统一，否则三角块颜色突兀
                # 均采用顺时针
                if not np.isnan(z[p0]) and not np.isnan(z[p3]):
                    # 以 0--3 为分割线
                    # 构造两个三角形 (p0, p1, p3), (p0, p3, p2)
                    i += [p0, p0]
                    j += [p1, p3]
                    k += [p3, p2]
                else: 
                    # 以 1--2 为分割线
                    # 构造两个三角形 (p1, p3，p2), (p0, p1, p2)
                    i += [p1, p0]
                    j += [p3, p1]
                    k += [p2, p2]
            elif count == 2:
                # 尝试拓展为钝角三角形？
                pass

    return {
        'x': x,
        'y': y,
        'z': z,
        'i': i,
        'j': j,
        'k': k,
        'intensity': intensity
    }
