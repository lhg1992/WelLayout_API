import numpy as np
from scipy.interpolate import griddata,RegularGridInterpolator
def surface2mesh3d(X, Y, Z, C=None, dense=1):
    """
    将规则网格数据 (X, Y, Z) 和颜色 C 转换为 go.Mesh3d 所需格式。
    x = np.arange(self.XRange[0], self.XRange[1], self.resolution)
    y = np.arange(self.YRange[0], self.YRange[1], self.resolution)
    X, Y = np.meshgrid(x, y)

    Z和C的np.nan值的位置对应

    参数:
        X, Y, Z: 2D numpy 数组，网格坐标 (由 meshgrid 生成)
        C: 2D numpy 数组，颜色数据 (可选，默认使用 Z)

    返回:
        dict，包括:
            x, y, z: 一维坐标列表
            i, j, k: 三角形索引列表
            intensity: 每个点的颜色值
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
