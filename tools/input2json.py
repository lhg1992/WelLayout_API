import json 
import numpy as np
import os
    
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            # deal with np.nan in Numpy
            return self.handle_nan(obj.tolist())
        
        if isinstance(obj, list):
            # deal with np.nan in List
            return self.handle_nan(obj)
        
        # convert np.nan to None
        if np.isnan(obj):
            return None
        
        return json.JSONEncoder.default(self, obj)
    
    def handle_nan(self, obj):
        if isinstance(obj, list):
            return [self.handle_nan(item) for item in obj]
        if isinstance(obj, float) and np.isnan(obj):
            return None
        return obj

def input2json (n, # number of wells
                
                PTM, # shape:(n, 3)
                VTM, # shape:(n, 3)
                PKM, # shape:(n, 3)
                VKM, # shape:(n, 3)
                DLSM, # shape:(n, 2) or (n, 3), dogleg for [KOP, Control(optional), Target] 
                rM= None, # curvature radius, corresponding to dogleg, overwrites DLSM if provided.
                ObjM=None, # objective(cost) function, default is the length of well trajectory
                        # shape (n, 1) string objects.

                tag= None, # a list of strings for well names

                MD_intervalM= None, # shape (n, )
                XRange= None, # shape (2, )
                YRange= None, # shape (2, )
                resolution= None, # scalar
                cst_radiusM= None, # shape (n, )
                
                # other constraints
                neconM= None,
                lay_conM= None,

                

                # K-sites parameters
                cst_Site= None,
                slot= None,
                cst_WH= None,
                cluster_min= None,
                cluster_max= None,

                filepath = "input.json",
               ):
    
    json_dict = \
        {"FIELDOPT INPUT BLOCK":
            {
                "n":
                {
                    "DESCRIPTION": "number of wells",
                    "UNIT":"",
                    "VALUE": int(n)

                },

                "tag":
                {
                    "DESCRIPTION": "well tag",
                    "UNIT":"",
                    "VALUE": tag 
                    # "VALUE":np.where(np.isnan(tag), None, tag)

                },

                "PTM":
                {
                    "DESCRIPTION": "target location, i.e., the 1st point of completion interval. 3D, [EAST,NORTH,Depth]",
                    "UNIT":"m",
                    "VALUE": PTM
                    # {
                    #     int(WellNo[i]): PTM[i,:] for i in range(PTM.shape[0])
                    #     }
                },
                
                "VTM":
                {
                    "DESCRIPTION": "driling direction at the target, 3D, [EAST,NORTH,Depth]",
                    "UNIT":"m",
                    "VALUE":VTM
                    # {
                    #     int(WellNo[i]): VTM[i,:] for i in range(VTM.shape[0])
                    #     }
                },

                "PKM":
                {
                    "DESCRIPTION": "kickoff point, [East, North, Depth]",
                    "UNIT":"m",
                    "VALUE":PKM
                    # {
                    #     int(WellNo[i]): PKM[i,:] for i in range(n)
                    #     }
                },

                "VKM":
                {
                    "DESCRIPTION": "driling direction at the KOP, 3D, [EAST,NORTH,Depth]",
                    "UNIT":"m",
                    "VALUE":VKM
                    # {
                    #     int(WellNo[i]): VKM[i,:] for i in range(VKM.shape[0])
                    #     }
                },

                "DLSM":
                {
                    "DESCRIPTION": "dogleg severity",
                    "UNIT":"°/30m",
                    "VALUE":DLSM
                    # {
                    #     int(WellNo[i]): DLSM[i,:] for i in range(n)
                    #     }
                },

                "rM":
                {
                    "DESCRIPTION": "turning radius",
                    "UNIT":"m",
                    "VALUE":rM
                    # {
                    #     int(WellNo[i]): rM[i,:] for i in range(n)
                    #     }
                },

                "ObjM":
                {
                    "DESCRIPTION": "objective(cost) function, default is the length of well trajectory",
                    "UNIT": "",
                    "VALUE": ObjM
                },

                "MD_intervalM":
                {   
                    "DESCRIPTION": "measured depth interval in output data of well trajectory",
                    "UNIT":"m",
                    "VALUE":MD_intervalM
                    # "VALUE":np.where(np.isnan(MD_intervalM), None, MD_intervalM)
                    # {
                    #     int(WellNo[i]): MD_intervalM[i,:] for i in range(n)
                    #     }
                },

                "XRange":
                {
                    "DESCRIPTION": "X(East) range for computing",
                    "UNIT":"m",
                    "VALUE":XRange

                },

                "YRange":
                {
                    "DESCRIPTION": "Y(North) range for computing",
                    "UNIT":"m",
                    "VALUE":YRange
                },

                "resolution":
                {
                    "DESCRIPTION": "resolution for computing nodes",
                    "UNIT":"m",
                    "VALUE":resolution
                },

                "cst_radiusM":
                {
                    "DESCRIPTION": "radius for computing cost contour",
                    "UNIT":"",
                    "VALUE":cst_radiusM
                    # {
                    #     int(WellNo[i]): cst_radiusM[i,:] for i in range(n)
                    #     }
                },

                "neconM":
                {
                    "DESCRIPTION": "non-equal constraints",
                    "UNIT":"",
                    "VALUE": neconM

                },

                "lay_conM":
                {
                    "DESCRIPTION": "formation constraints in special layer(s)",
                    "UNIT":"",
                    "VALUE": lay_conM
                },

                "cst_Site":
                {
                    "DESCRIPTION": "drill site preparation cost",
                    "UNIT":"",
                    "VALUE": cst_Site
                },

                "slot":
                {
                    "DESCRIPTION": "available slot numbers in one cluster",
                    "UNIT":"",
                    "VALUE": slot
                },

                "cst_WH":
                {
                    "DESCRIPTION": "cost of subsea wellhead equipment of different slots, corresponding with slot",
                    "UNIT":"",
                    "VALUE": cst_WH
                },

                "cluster_min":
                {
                    "DESCRIPTION": "minimum number of clusters(drill sites)",
                    "UNIT":"",
                    "VALUE": cluster_min
                    # "VALUE":np.where(np.isnan(cluster_min), None, cluster_min)
                },

                "cluster_max":
                {
                    "DESCRIPTION": "maximum number of clusters(drill sites)",
                    "UNIT":"",
                    "VALUE": cluster_max
                    # "VALUE":np.where(np.isnan(cluster_max), None, cluster_max)
                },

            }
        }
    
    out_json=json.dumps(json_dict, cls=NumpyEncoder)


    try:
        try:
            # if path doesn't exist, create it
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        except Exception as e: # filepath is a single file name
            pass

        with open(filepath, "w") as outfile:
            outfile.write(out_json)
        print(f"=====file {str(filepath)} written successfully=====")
        print("===================================")
    except Exception as e:
        print("======Error in opening file========")
        print(str(e))

    return out_json