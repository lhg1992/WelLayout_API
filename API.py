import requests
import json
import sys
import os

url_1well = "https://home-test.make234.com/api/v1/get_1well"
url_1site = "https://home-test.make234.com/api/v1/get_1site"
url_ksites = "https://home-test.make234.com/api/v1/get_ksites"



# %%
# =======================================================================
# =======================================================================
# =======================================================================
def get_1well(input_data, # formatted json data
            index=None,
            getContour=0,

            filepath='output.json', # filepath to save response content
            show=0, # show full response
            
            timeout=300,
            url=url_1well, # API server url
            ):
     return APIhandler(url, # API server url
                input_data, # formatted json data
                index=index,
                getContour=getContour,

                filepath=filepath, # filepath to save response content
                show=show, # show full response
                timeout=timeout,
                )

# %%
# *********************************************************************
def get_1site(input_data, # formatted json data
              indices=None, # indices of wells to be extracted from response
              getContours=0,
              
            filepath='output.json', # filepath to save response content
            show=0, # show full response

            timeout=300,
            url=url_1site, # API server url
            ):
    
    return APIhandler(url, # API server url
                input_data, # formatted json data
                indices=indices,
                getContours=getContours,

                filepath=filepath, # filepath to save response content
                show=show, # show full response
                timeout=timeout,
                )
# %%
# ***********************************************************************
def get_ksites(input_data, # formatted json data
              indices=None, # indices of wells to be extracted from response
              getContours=0,

            filepath='output.json', # filepath to save response content
            show=0, # show full response

            timeout=300,
            url=url_ksites, # API server url
            ):
    
    return APIhandler(url, # API server url
                input_data, # formatted json data
                indices=indices,
                getContours=getContours,

                filepath=filepath, # filepath to save response content
                show=show, # show full response
                timeout=timeout,
                )


# %%
# =======================================================================
# =======================================================================
# =======================================================================
def APIhandler(url, # API server url
            input_data, # formatted json data
            index=None, # index of well for 1well
            getContour=0, # whether to get the cost contour of the well

            indices=None, # indices of wells for 1site & ksites
            getContours=0, # whether to get the cost contours of each well

            filepath='output.json', # filepath to save response content
            show=0, # show full response

            timeout=300,
            ):
    # Set request headers
    headers = {
        'Content-Type': 'application/json'
    }

    print(f"requesting from {url}")
    try:
        # if the last word of url is "get_1well"
        if url.split("/")[-1]=="get_1well":
            if index is None: # automatically computes the 1st well (index=0)
                input_data["other"]={"getContour":getContour}
                pass 
            elif isinstance(index, int):
                if (index<0) or index>=input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']:
                    print(f"index out of range [0, {input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']}]")
                    return None
                # add parameters for computing the specified well
                input_data["other"]={"index":index, "getContour":getContour}
            else:
                print("index must be an integer or unspecified(None)")
                return None
            response = requests.post(url, json=input_data, headers=headers, timeout=timeout)

        elif url.split("/")[-1]=="get_1site":
            if indices is None: # automatically computes all well as 1-site problem
                input_data["other"]={"getContours":getContours}
                pass 
            elif isinstance(indices, list):
                for ind in indices:
                    if not isinstance(ind, int):
                        print(f"index must be an integer")
                        return None
                    if (ind<0) or ind>=input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']:
                        print(f"index out of range [0, {input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']}]")
                        return None
                # add parameters for computing the specified wells
                input_data["other"]={"indices":indices, "getContours":getContours}
            else:
                print("indices must be a list of integers or unspecified(None)")
                return None
            response = requests.post(url, json=input_data, headers=headers, timeout=timeout)

        elif url.split("/")[-1]=="get_ksites":
            if indices is None: # automatically computes all well as k-sites problem
                input_data["other"]={"getContours":getContours}
                pass 
            elif isinstance(indices, list):
                for ind in indices:
                    if not isinstance(ind, int):
                        print(f"index must be an integer")
                        return None
                    if (ind<0) or ind>=input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']:
                        print(f"index out of range [0, {input_data['FIELDOPT INPUT BLOCK']['n']['VALUE']}]")
                        return None
                # add parameters for computing the specified wells
                input_data["other"]={"indices":indices, "getContours":getContours}
            else:
                print("indices must be a list of integers or unspecified(None)")
                return None
            response = requests.post(url, json=input_data, headers=headers, timeout=timeout)
        
        # Check response status
        response.raise_for_status()
        print("Status code:", response.status_code)

        # format response content to JSON format
        output=json.dumps(response.json(), indent=2)

        # Print response results
        if show==1:
            print("Response content:")
            print(output)

        # Save response content to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
        print(f"Response content has been saved to \"{filepath}\"")

        # return response content
        return json.loads(output)
    except requests.exceptions.Timeout:
        print("Request timeout (exceeded 5 minutes)")
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except json.JSONDecodeError:
        print("Response is not valid JSON format")
        print("Raw response:", response.text)