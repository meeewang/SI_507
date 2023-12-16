import requests
import pandas as pd
import numpy as np
from zipfile import ZipFile
from time import sleep
import io

rows = 0
cols = 0   

def initialize(url):
    '''
    Get institiutional data from IPEDS
    '''
    file_content = requests.get(url)
    if file_content.status_code == 200:
        print("File downloaded successfully.")
        content = io.BytesIO(file_content.content)
        content.seek(0)
        compile_text = []
        with ZipFile(content, mode="a") as archive:
            with archive.open("hd2022_data_stata.csv", mode="r") as hello:
                for line in io.TextIOWrapper(hello, encoding='ISO-8859-1'):
                    lst = line.split(",")
                    compile_text.append(lst)
        return compile_text
    else: 
        print("API request failed")


def printData(array):
    '''
    Print data
    '''
    with open('output.txt', 'w') as file:
        for row in array:
            print("\t".join(str(value) for value in row), file=file)


def create_nodes(array, keywords):   
    '''
    Find five parameters from data
    '''
    institution_clean = {}
    inst = array[0].index("INSTNM")
    n = len(array)
    for keyword in keywords:
        institution_raw = {}
        index = array[0].index(keyword)     
        for i in range(1, n - 1):
            if array[i][index] not in institution_raw.keys():
                institution_raw[array[i][index]]= []
                institution_raw[array[i][index]].append(array[i][inst])
            else:
                institution_raw[array[i][index]].append(array[i][inst])
        if keyword == "ICLEVEL":
            institution_clean["Four or more years"] = institution_raw['1']
            institution_clean["At least 2 but less than 4 years"] = institution_raw['2']
            institution_clean["Less than 2 years (below associate)"] = institution_raw['3']
            institution_clean["Unknown"] = institution_raw['-3']
        if keyword == "CONTROL":
            institution_clean["Public"] = institution_raw['1']
            institution_clean["Private not-for-profit"] = institution_raw['2']
            institution_clean["Private for-profit"] = institution_raw['3']
            institution_clean["Unknown"] = institution_raw['-3']
        if keyword == "INSTSIZE":
            institution_clean["Under 1,000"] = institution_raw['1']
            institution_clean["1,000 - 4,999"] = institution_raw['2']
            institution_clean["5,000 - 9,999"] = institution_raw['3']
            institution_clean["10,000 - 19,999"] = institution_raw['4']
            institution_clean["20,000 and above"] = institution_raw['5']
            institution_clean["Not reported"] = institution_raw['-1']
            institution_clean["Not applicable"] = institution_raw['-2']
        if keyword == "OBEREG":
            institution_clean["U.S. Service schools"] = institution_raw[' 0']
            institution_clean["New England (CT, ME, MA, NH, RI, VT)"] = institution_raw[' 1']
            institution_clean["Mid East (DE, DC, MD, NJ, NY, PA)"] = institution_raw[' 2']
            institution_clean["Great Lakes (IL, IN, MI, OH, WI)"] = institution_raw[' 3']
            institution_clean["Plains (IA, KS, MN, MO, NE, ND, SD)"] = institution_raw[' 4']
            institution_clean["Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)"] = institution_raw[' 5']
            institution_clean["Southwest (AZ, NM, OK, TX)"] = institution_raw[' 6']
            institution_clean["Rocky Mountains (CO, ID, MT, UT, WY)"] = institution_raw[' 7']
            institution_clean["Far West (AK, CA, HI, NV, OR, WA)"] = institution_raw[' 8']
            institution_clean["Other U.S. jurisdictions (AS, FM, GU, MH, MP, PR, PW, VI)"] = institution_raw[' 9']
        if keyword == "HBCU":
            institution_clean["HBCU"] = institution_raw['1']
            institution_clean["Non-HBCU"] = institution_raw['2']
    return institution_clean


def getInst(node):
    global inst_raw
    return inst_raw[node]

def getList(inst):
    global inst_raw
    s = []
    for node, colleges in inst_raw.items():
        if inst in colleges:
            s.append(node)
    return s

def init_global_data():
    global instList
    global adjacencyMatrix
    global cache

    instSet = set()
    for colleges in inst_raw.values():
        instSet.update(colleges)
    instList = list(instSet)
    N = len(instList)

    # Initialize the adjacency matrix as an N by N matrix of zeroes.
    adjacencyMatrix = np.array([0] * (N * N)).reshape(N, N)

    # Now populate it.
    for i, inst in enumerate(instList):
        for node in getList(inst):
            for lst in getInst(node):
                j = instList.index(lst)
                adjacencyMatrix[i,j] += 1

    # Initialize the cache.
    cache = [None, adjacencyMatrix]

def get_power(N):
    """
        Get the Nth power of the adjacency matrix.
        Cache the result to minimize the number of
        matrix multiplications we have to perform.
    """
    global adjacencyMatrix
    global cache

    while len(cache) < N + 1:
        # Get a reference to the highest power we have calculated so far.
        # Calculate the next power and add the matrix to the cache.
        cache.append(np.dot(cache[-1], adjacencyMatrix))

    # Return a reference to a matrix in the cache.
    return cache[N]

def instNumber(inst, referenceInst):
    """
        List the similar instititutons
    """
    global instList
    i = instList.index(referenceInst)
    j = instList.index(inst)
    if i == j:
        return 0
    power = 1
    A = get_power(power)
    while A[i,j] <= 0:
        power += 1
        if power > 10:
            # Quick and dirty check against hanging.
            raise Exception("Infinite loop")
        A = get_power(power)
    return A

def prompt():
    response1 = input("Please list your top choice of institution: ")
    response2 = input("please list your second choice of institution: ")
    response3 = '\'\"' + response1 + '\"\''
    response4 = '\'\"' + response2 + '\"\''
    nodes = []
    recommend = []
    try:
        for node in getList(response3):
            if node in getList(response4):
                nodes.append(node)
                for i in getInst(node):
                    recommend.append(i)
        print ("Instititutions you probably would like to consider: ", recommend)
    except:
        print("Sorry, ", response1, "or ", response2, " cannot be found. Please check your name or change institutions")
        prompt()
      


if __name__ == "__main__":

    url = "https://nces.ed.gov/ipeds/datacenter/data/HD2022_Data_Stata.zip"

    max_retries = 3
    base_retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except requests.HTTPError as err:
            if response.status_code == 503 and attempt < max_retries - 1:
                retry_delay = base_retry_delay * 2 ** attempt
                print(f"Retrying in {retry_delay} seconds...")
                sleep(retry_delay)
            else:
                print(f"Failed with status code {response.status_code}: {err}")
                break
    data = initialize(url)
    printData(data)
    # create five parameters
    inst_raw = create_nodes(data, ["ICLEVEL", "CONTROL", "INSTSIZE", "OBEREG", "HBCU"])
    init_global_data()
    prompt()







