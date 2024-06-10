import csv
import math
import matplotlib.pyplot as plt
import numpy as np

class MeasurementData:
    def __init__(self, datafolder, tagfilenames, extension, tagnames):
        self.m_alltagdata = []
        self.LoadData(datafolder, tagfilenames, extension, tagnames)

    def LoadData(self, datafolder, tagfilenames, extension, tagnames):
    #    for tagname in tagnames:
        # TODO: add something smart to make sure this goes OK when we have distances to different tags

        # read position data
        with open(datafolder+'position'+extension, mode = 'r') as positionData:
            positionData.__next__()      # skip first row containing field names
            datareader = csv.reader(positionData, delimiter=',')
            tagpositions = [ [] for _ in range(len(tagnames)) ]     # create list of n lists, where n is the number of tagnames
            for row in datareader:
                self.AddPositionTotagpositions(tagnames, row, tagpositions)

        # read tag data
        for index, filename in enumerate(tagfilenames):
            try:
                with open(datafolder+filename+extension, mode = 'r') as tagData:
                    tagData.__next__()      # skip first row containing field names
                    datareader = csv.reader(tagData, delimiter=',')
                    measurementtimes = []
                    distances = []
                    tagname = filename[-1]
                    for row in datareader:
                        measurementtimes.append(float(row[0]))
                        distances.append(float(row[2]))
                    self.AddTagData(TagData(tagname, measurementtimes, distances, tagpositions[index]))

            except FileNotFoundError:
                print(f"File does not exist for: {filename}. Skipping...")
    
    def AddTagData(self, NewTagData):
        self.m_alltagdata.append(NewTagData)

    def AddPositionTotagpositions(self, tagnames, row, tagpositions):
        #used in the LoadData function
        for index, tagname in enumerate(tagnames):
            if row[1] == tagname:
                tagpositions[index].append(Position(row[2], row[3]))          

class TagData:
    def __init__(self, tagID, measurementtimes, distances_to_other_tags, tagpositions):
        self.m_tagID = tagID
        self.m_measurementtimes = measurementtimes
        self.m_distances_to_other_tags = distances_to_other_tags
        self.m_tagpositions = tagpositions

    def ComputeContactTimes(self, radius):
        # input is of type TagData
        # output is list of intervals in contact
        contacttimes = []
        incontact = False
        for index, distance in enumerate(self.m_distances_to_other_tags):
            if distance < radius and incontact == False:
                incontact = True
                startofcontact = self.m_measurementtimes[index]
            elif distance >= radius and incontact == True:
                incontact = False
                endofcontact = self.m_measurementtimes[index-1]
                contacttimes.append([startofcontact, endofcontact])
        # Ensure that contact is registered if persons are still in contact at end of test period
        if incontact == True:
                endofcontact = self.m_measurementtimes[index]
                contacttimes.append([startofcontact, endofcontact])
        return contacttimes        

    def AddDistances(distanceToWhichTag, distances):
        pass    
    #TODO: do stuff so we can add distances to other tags

class Position:
    def __init__(self, xposition, yposition):
        self.m_x = float(xposition)
        self.m_y = float(yposition)



def ComputeDistance(position1, position2):
    # Should be a member of Position class? Or not as it is random which position is position1 or 2, see reasoning CheckMeasurementValidity function
    return math.sqrt((position1.m_x - position2.m_x)**2 + (position1.m_y - position2.m_y)**2)  

def GetTotalTimeAndOccurences(contacttimes):
    occurences = len(contacttimes)
    totaltime = 0
    for occurence in contacttimes:
        totaltime += (occurence[1] - occurence[0])
    return[occurences, totaltime]

def PrintSummary(tagdata, radius):
    contacttimes = tagdata.ComputeContactTimes(radius)
    [occurences, totaltime] = GetTotalTimeAndOccurences(contacttimes)
    print(f"The subjects were in contact for a total of {totaltime} seconds, divided over {occurences} separate occurences. \n"
          f"contact occurred during the following time intervals: {tagdata.ComputeContactTimes(radiusforcontact)}")

def CheckMeasurementValidity(tagdata1, tagdata2, tolerance):
    # input: two objects of type TagData
    # maybe make this a member of TagData, and pass 1 other TagData object? Or does that not make sense as it is random which of the data is tagdata1 and which is tagdata2?
    corrupted_measurement_times = []
    for index, distance_to_other_tag in enumerate(tagdata1.m_distances_to_other_tags):
        distance_from_position = ComputeDistance(tagdata1.m_tagpositions[index], tagdata2.m_tagpositions[index])
        if abs(distance_from_position-distance_to_other_tag) > tolerance:
            corrupted_measurement_times.append([tagdata1.m_measurementtimes[index], abs(distance_from_position-distance_to_other_tag)])
    return corrupted_measurement_times

#def ShowContactHotspots():
    # get contact times
    # get positions from times
    # draw positions


extension = '.csv'
tagfilenames = ['TagA', 'TagB', 'TagC']     # Can be extended as new tags are added
tagnames = ['A', 'B']

defaultdatafolder = 'D:/TNO_assessment/data/'    # TODO: should be entered by user in terminal
radiusforcontact = 5
measurement_error_tolerance = 0.1

possibleUserInput = ['a', 'b', 'c']

# main program

# x = np.linspace(0, 2 * np.pi, 200)
# y = np.sin(x)

# fig, ax = plt.subplots()
# ax.plot(x, y)
# plt.show()

userWantsToExit = False
dataIsEntered = False
print("Welcome to the pathogen transfer experiment tool. Please enter your datafolder (leave emtpy for default dataset): ")
while not dataIsEntered:
    datafolder = input()
    if datafolder == '':
        datafolder = defaultdatafolder
    try:
        open(datafolder+'position'+extension, mode = 'r')
    except:
        print("No position data found. Try other folder, or leave emtpy for default dataset:")
    try:
        open(datafolder+tagfilenames[0]+extension, mode = 'r')
        dataIsEntered = True
    except:
        print("No tagdata found. Try other folder, or leave emtpy for default dataset:")


DatasetOfInterest = MeasurementData(datafolder, tagfilenames, extension, tagnames)

while not userWantsToExit:
    print("Enter what you want to do: \n"
          "a : Print summary \n"
          "b : Show contact hotspots \n"
          "c : exit program")
    userinput = input()
    try:
        (userinput in possibleUserInput)
    except:
        print("input not recognized")
    
    match userinput:
        case 'a':
            PrintSummary(DatasetOfInterest.m_alltagdata[0], radiusforcontact)
        case 'b':
            pass
        case 'c':
            userWantsToExit = True




# print(CheckMeasurementValidity(DatasetOfInterest.m_alltagdata[0], DatasetOfInterest.m_alltagdata[1], measurement_error_tolerance))




