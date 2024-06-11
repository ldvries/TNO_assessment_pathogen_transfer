import csv
import math
import numpy as np
import os

from pathogentool_dataclasses import TagData
from pathogentool_dataclasses import MeasurementData
from pathogentool_dataclasses import Position
import pathogentool_utilities as ptu


# Settings
extension_of_datafiles = '.csv'
tagfilenames = ['TagA', 'TagB']     # Can be extended as new tags are added
tagnames = ['A', 'B']

default_datafolder = 'D:/TNO_assessment/data/'
radius_for_contact = 1.5    # [m]
measurement_error_tolerance = 0.1   # [m]

possible_user_input = ['a', 'b', 'c', 'd', 'e', 'f']


# main program
userWantsToExit = False
dataIsEntered = False
print("Welcome to the pathogen transfer experiment tool."
      " Please enter your datafolder (leave emtpy for default dataset): ")
while not dataIsEntered:
    datafolder = input()
    if datafolder == '':
        datafolder = default_datafolder
    try:
        open(os.path.join(datafolder, 'position' + extension_of_datafiles), mode = 'r')
        open(os.path.join(datafolder, 'position' + extension_of_datafiles), mode = 'r')
        dataIsEntered = True
    except:
        print("No positiondata and / or tagdata found. Try other folder, or leave emtpy for default dataset:")


DatasetOfInterest = MeasurementData(datafolder, tagfilenames, extension_of_datafiles, tagnames)

while not userWantsToExit:
    print("Enter what you want to do: \n"
          "a : Print summary \n"
          "b : Show contact hotspots \n"
          "c : Show invalid measurements \n"
          f"d : Change radius for contact (current is {radius_for_contact} [m])\n"
          f"e : Change error tolerance (current is {measurement_error_tolerance} [m])\n"
          "f : exit program")
    userinput = input()
    try:
        (userinput in possible_user_input)
    except:
        print("input not recognized")
    
    match userinput:
        case 'a':
            ptu.PrintSummary(DatasetOfInterest.m_alltagdata[0], radius_for_contact)
        case 'b':
            print(ptu.ShowContactHotspots(DatasetOfInterest.m_alltagdata[0], DatasetOfInterest.m_alltagdata[1], radius_for_contact))
        case 'c':
            print("Measurements of tag and beacon do not agree on the following data points, "
                  "where the first entry is the measurement time and the second entry the difference in meters between tag and beacon data:"
                  f" {ptu.CheckMeasurementValidity(DatasetOfInterest.m_alltagdata[0], DatasetOfInterest.m_alltagdata[1], measurement_error_tolerance)}")
        case 'd':
            print("Enter new radius for contact in [m] : ")
            radius_for_contact = float(input())
        case 'e':
            print("Enter new error tolerance in [m] : ")
            measurement_error_tolerance = float(input())           
        case 'f':
            userWantsToExit = True



