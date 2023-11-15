import requests
import json
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import random as random
from matplotlib.path import Path 
import numpy as np


class DetroitDistrict:
    def __init__(self, coordinates, holc_grade, qualitative_description, name, random_lat=None, random_long=None, median_income=None, census_tract=None):
        self.Coordinates = coordinates
        self.HolcGrade = holc_grade
        self.QualitativeDescription = qualitative_description
        self.name = name
        self.RandomLat = random_lat
        self.RandomLong = random_long
        self.MedianIncome = median_income
        self.CensusTract = census_tract
    class DetroitDistrict: