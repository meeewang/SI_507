#########################################
##### Name:     Meng Wang           #####
##### Uniqname:     meeewang        #####
#########################################

import requests
import json
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import random as random
from matplotlib.path import Path 
import numpy as np
import re

class DetroitDistrict:

    def __init__(self, data):
        self.Coordinates = self.extract_coordinates(data)
        self.Coordinates = self.Coordinates[0][0]
        self.HolcGrade = data['properties']['holc_grade']
        self.HolcColor = self.grade_to_color(self.HolcGrade)
        self.name = self.extract_name(data)  # Here we can define our extraction method
        self.QualitativeDescription = self.extract_section_8(data)
        self.RandomLat = None
        self.RandomLong = None
        self.MedianIncome = None
        self.CensusTract = None
    
    def extract_coordinates(self, data):
        # Extracting coordinates considering the fact that some districts can be non-contiguous
        return data['geometry']['coordinates']

    def grade_to_color(self, grade):
        color_map = {
            'A': 'darkgreen',
            'B': 'cornflowerblue',
            'C': 'gold',
            'D': 'maroon'
        }
        return color_map.get(grade, 'unknown') 

    def extract_name(self, data):
        # This is a placeholder. You can define the logic to extract the name or assign an iterator as required
        # For now, I'm returning the id of the district as its name
        return data['properties']['holc_id']

    def extract_section_8(self, data):
        return data['properties']["area_description_data"]['8']

  
def medianIncome(tract, data):
    for row in data:
        if row[3] == tract :
            return row[0]
    return None

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open("cache_redlining.json", 'w')
    fw.write(dumped_json_cache)
    fw.close()

def open_cache():
    try:
        cache_file = open("cache_redlining.json", 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = []
    return cache_dict

def mean_in(incomeList):
    if len(incomeList) != 0:
        return sum(incomeList) / len(incomeList)
    else:
        return "Not available now. Try again."

def median_in(incomeList):
    incomeList = sorted(incomeList)
    n = len(incomeList)
    if len(incomeList) != 0:
        if n % 2 == 1:
            return incomeList[int((n-1)/2)]
        else:
            left = incomeList[int(n/2 - 1)]
            right = incomeList[int(n/2 + 1)]
        return (left + right) / 2
    else:
        return "Not available now. Try again."

def ten_Most_Common(strList):
    if len(strList) != 0:
        strList = " ".join(strList)
        words = re.findall(r'\b\w+\b', strList, re.IGNORECASE)
        words = [word.lower() for word in words] # convert to lower cases
        filler_words = ["the", "and", "of", "a", "is", "are", "in", "to", "for", "with", "but", "by", "this", "that",
                        "on", "at", "not", "as", "there", "very", "000", "all", "area", "2", "from"]
        most_10 = []
        common = {}
        for word in words:
            if word not in filler_words:
                if word not in common:
                    common[word] = 1
                else:
                    common[word] = common[word] + 1           
            
        #print(common)
        sorted_words = sorted(common.items(), key = lambda x: x[1], reverse = True)
        #print(sorted_words)
        for i in range(10):
            most_10.append(sorted_words[i][0])
        
        return most_10
    else:
        return "Not available now. Try again." 


if __name__ == "__main__":

    base_url = "https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson"
    response = requests.get(base_url)

    if response.status_code == 200:
        RedliningData = json.loads(response.text)
        # to access the features:
        features = RedliningData['features']    
    else:
        print("Failed to fetch the GeoJSON data. Status code:", response.status_code)


    Districts = [DetroitDistrict(feature) for feature in features]

    fig, ax = plt.subplots()
    for district in Districts: # what kind of for loop makes sense? 
        ax.add_patch(
        plt.Polygon(district.Coordinates, color =district.HolcColor,) 
        ) # add arguments here 
        ax.autoscale()
        plt.rcParams["figure.figsize"] = (15,15)
    plt.show()


    random.seed(17)
    xgrid = np.arange(-83.5,-82.8,.004) 
    ygrid = np.arange(42.1, 42.6, .004) 
    xmesh, ymesh = np.meshgrid(xgrid,ygrid)
    points = np.vstack((xmesh.flatten(),ymesh.flatten())).T
    for j in Districts:
        p = Path(j.Coordinates, codes=None)
        grid = p.contains_points(points)
        print(j," : ", points[random.choice(list(np.where(grid)[0]))]) 
        point = points[random.choice(list(np.where(grid)[0]))] 
        j.RandomLong = point[0]
        j.RandomLat = point[1]


    api_key = "84e5b35447fb5fd886aecc07d8325b7bb285eaf6"

    latitude = 42.33
    longitude = -83.04

    # Construct the API request URL
    api_url = f"https://geo.fcc.gov/api/census/block/find?latitude={latitude}&longitude={longitude}&format=json&showall=true"

    headers = {"apikey": api_key}
    response = requests.get(api_url, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        data = response.json()
        block_fips = data.get("Block", {}).get("FIPS", {})
        census_tract = block_fips[5:11]
        county_code = block_fips[2:5]
        print(f"Census Tract Code: {census_tract}, County Code: {county_code}")
    else:
        print("API request failed")


    # Construct the API request URL

    api_url = f"https://api.census.gov/data/2018/acs/acs5?get=B19013_001E&for=tract:*&in=state:26&in=county:*"
    # Make the API request
    response = requests.get(api_url)
    # Check for a successful response
    if response.status_code == 200:
        income_data  = response.json()
        print(income_data)
 
    else:
        print("API request failed")

    
    CACHE_redlining = open_cache()

    
    iii = 0
    Alist = []
    Blist = []
    Clist = []
    Dlist = []

    AStringList = []
    BStringList = []
    CStringList = []
    DStringList = []
    
    incomeRank = []

    census_tracts = [
        {"census_tract_code": "TRACT_CODE_1", "state_code": "STATE_CODE_1", "county_code": "COUNTY_CODE_1"},
        {"census_tract_code": "TRACT_CODE_2", "state_code": "STATE_CODE_2", "county_code": "COUNTY_CODE_2"},
        # Add more census tracts as needed
    ]

    # Initialize an empty dictionary to store the data
    data_cache = {}

    # Loop through each census tract and fetch median income data
    for tract_data in census_tracts:
        census_tract_code = tract_data["census_tract_code"]
        county_code = tract_data["county_code"]

        # Construct the API request URL
        api_url = f"https://api.census.gov/data/2018/acs/acs5?key={api_key}&get=B19013_001E&for=tract:{census_tract_code}&in=state:26+county:{county_code}"

        # Make the API request
        response = requests.get(api_url)

        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            median_income = data[1][0]  # Extract the median household income value

            # Store the data in the cache
            data_cache[census_tract_code] = {
                "county_code": county_code,
                "median_income": median_income,
                
            }
        else:
            print(f"API request for {census_tract_code} failed")

    # Save the data cache as a JSON file
    with open("income_data_cache.json", "w") as json_file:
        json.dump(data_cache, json_file, indent=2)

    print("Data cache saved as income_data_cache.json")


    A_mean_income = mean_in(Alist)
    A_median_income = median_in(Alist)
    print(f"A: mean income: {A_mean_income}, median income: {A_median_income}")

    B_mean_income = mean_in(Blist)
    B_median_income = median_in(Blist)
    print(f"A: mean income: {B_mean_income}, median income: {B_median_income}")


    C_mean_income = mean_in(Clist)
    C_median_income = median_in(Alist)
    print(f"C: mean income: {C_mean_income}, median income: {C_median_income}")

    D_mean_income = mean_in(Dlist)
    D_median_income = median_in(Dlist)
    print(f"D: mean income: {D_mean_income}, median income: {D_median_income}")

    A_10_Most_Common = ten_Most_Common(AStringList)
    print(f"A_10_Most_Common: {A_10_Most_Common}")
    B_10_Most_Common = ten_Most_Common(BStringList)
    print(f"B_10_Most_Common: {B_10_Most_Common}")
    C_10_Most_Common = ten_Most_Common(CStringList)
    print(f"C_10_Most_Common: {C_10_Most_Common}")
    D_10_Most_Common = ten_Most_Common(DStringList)
    print(f"D_10_Most_Common: {D_10_Most_Common}")


        




