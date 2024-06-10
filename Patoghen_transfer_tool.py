import csv
import math
import matplotlib.pyplot as plt
import numpy as np

# data classes
class MeasurementData:
    def __init__(self):
        self.m_alltagdata = []
    def AddTagData(self, NewTagData):
        self.m_alltagdata.append(NewTagData)

class TagData:
    def __init__(self, tagID, measurementtimes, distances_to_other_tags, tagpositions):
        self.m_tagID = tagID
        self.m_measurementtimes = measurementtimes
        self.m_distances_to_other_tags = distances_to_other_tags
        self.m_tagpositions = tagpositions

    def AddDistances(distanceToWhichTag, distances):
        pass    
    #TODO: do stuff so we can add distances to other tags

class Position:
    def __init__(self, xposition, yposition):
        self.m_x = float(xposition)
        self.m_y = float(yposition)



def ComputeDistance(position1, position2):
    return math.sqrt((position1.m_x - position2.m_x)**2 + (position1.m_y - position2.m_y)**2)


def AddPositionTotagpositions(tagnames, row, tagpositions):
    #used in the LoadData function
    for index, tagname in enumerate(tagnames):
        if row[1] == tagname:
            tagpositions[index].append(Position(row[2], row[3]))    

def LoadData(datafolder, tagfilenames, extension, tagnames):
    # TODO: make part of MeasurementData class.

    Mydataset = MeasurementData()

#    for tagname in tagnames:
    # TODO: add something smart to make sure this goes OK when we have distances to different tags

    # get positions for tags

    # read position data
    with open(datafolder+'position'+extension) as positionData:
        positionData.__next__()      # skip first row containing field names
        datareader = csv.reader(positionData, delimiter=',')
        tagpositions = [ [] for _ in range(len(tagnames)) ]     # create list of m lists, where n is the number of tagnames
        for row in datareader:
            AddPositionTotagpositions(tagnames, row, tagpositions)

    # read tag data
    for index, filename in enumerate(tagfilenames):
        try:
            with open(datafolder+filename+extension, mode = 'r', newline='') as csvData:
                csvData.__next__()      # skip first row containing field names
                datareader = csv.reader(csvData, delimiter=',')
                measurementtimes = []
                distances = []
                tagname = filename[-1]
                for row in datareader:
                    measurementtimes.append(float(row[0]))
                    distances.append(float(row[2]))
                Mydataset.AddTagData(TagData(tagname, measurementtimes, distances, tagpositions[index]))

        except FileNotFoundError:
            print(f"File does not exist for: {filename}. Skipping...")

    return Mydataset

def ComputeContactTimes(tagdata, radius):
    # input is of type TagData
    # output is list of intervals in contact
    # TODO: make part of TagData class?
    contacttimes = []
    incontact = False
    for index, distance in enumerate(tagdata.m_distances_to_other_tags):
        # TODO: extract methods here?
        if distance < radius and incontact == False:
            incontact = True
            startofcontact = tagdata.m_measurementtimes[index]
        elif distance >= radius and incontact == True:
            incontact = False
            endofcontact = tagdata.m_measurementtimes[index-1]
            contacttimes.append([startofcontact, endofcontact])
    return contacttimes

def GetTotalTimeAndOccurences(contacttimes):
    occurences = len(contacttimes)
    totaltime = 0
    for occurence in contacttimes:
        totaltime += (occurence[1] - occurence[0])
    return[occurences, totaltime]

def PrintSummary(tagdata, radius):
    contacttimes = ComputeContactTimes(tagdata, radius)
    [occurences, totaltime] = GetTotalTimeAndOccurences(contacttimes)
    print(f"The subjects were in contact for a total of {totaltime} seconds, divided over {occurences} separate occurences.")

def CheckMeasurementValidity(tagdata1, tagdata2, tolerance):
    # input: two objects of type TagData
    # maybe make this a member of TagData, and pass 1 other TagData object?
    corrupted_measurement_times = []
    for index, distance_to_other_tag in enumerate(tagdata1.m_distances_to_other_tags):
        distance_from_position = ComputeDistance(tagdata1.m_tagpositions[index], tagdata2.m_tagpositions[index])
        if abs(distance_from_position-distance_to_other_tag) > tolerance:
            corrupted_measurement_times.append([tagdata1.m_measurementtimes[index], abs(distance_from_position-distance_to_other_tag)])
    return corrupted_measurement_times


extension = '.csv'
tagfilenames = ['TagA', 'TagB', 'TagC']     # Can be extended as new tags are added
tagnames = ['A', 'B']

datafolder = 'D:/TNO_assessment/data/'    # TODO: should be entered by user in terminal
radiusforcontact = 5
measurement_error_tolerance = 0.1

# main program

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()


DatasetOfInterest = LoadData(datafolder, tagfilenames, extension, tagnames)
PrintSummary(DatasetOfInterest.m_alltagdata[0], radiusforcontact)

print(CheckMeasurementValidity(DatasetOfInterest.m_alltagdata[0], DatasetOfInterest.m_alltagdata[1], measurement_error_tolerance))

mycontacttimesA = ComputeContactTimes(DatasetOfInterest.m_alltagdata[0], radiusforcontact)
print(mycontacttimesA)



