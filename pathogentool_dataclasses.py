import os
import csv
import math

class MeasurementData:
    """class to read and store all measurement data"""
    def __init__(self, datafolder_to_read, tagfilenames_in_dataset, extension, tagnames_in_dataset):
        self.m_alltagdata = []
        self.LoadData(datafolder_to_read, tagfilenames_in_dataset, extension, tagnames_in_dataset)

    def LoadData(self, datafolder_to_read, tagfilenames_in_dataset, extension, tagnames_in_dataset):

        # read position data
        with open(os.path.join(datafolder_to_read, 'position' + extension), mode = 'r', encoding="utf-8") as positionData:
            next(positionData)      # skip first row containing field names
            datareader = csv.reader(positionData, delimiter=',')
            tagpositions = [ [] for _ in range(len(tagnames_in_dataset)) ]     # create list of n lists, where n is the number of tagnames
            for row in datareader:
                self.AddPositionTotagpositions(tagnames_in_dataset, row, tagpositions)

        # read tag data
        for index, filename in enumerate(tagfilenames_in_dataset):
            try:
                with open(os.path.join(datafolder_to_read+filename+extension), mode = 'r', encoding="utf-8") as tagData:
                    next(tagData)      # skip first row containing field names
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
    
    def AddTagData(self, new_tagdata):
        self.m_alltagdata.append(new_tagdata)

    def AddPositionTotagpositions(self, tagnames_to_add, row, tagpositions_to_add):
        #used in the LoadData function
        for index, tagname in enumerate(tagnames_to_add):
            if row[1] == tagname:
                tagpositions_to_add[index].append(Position(row[2], row[3]))

class TagData:
    """Stores all data for a single tag"""
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
                endofcontact = self.m_measurementtimes[-1]
                contacttimes.append([startofcontact, endofcontact])
        return contacttimes     

    def GetPositionsForMeasurementTimes(self, times):
        contactpositions = []
        for timeintervals in times:
            for index, time in enumerate(self.m_measurementtimes):
                if time >= timeintervals[0] and time <= timeintervals[1]:
                    contactpositions.append(self.m_tagpositions[index])
        return contactpositions


class Position:
    def __init__(self, xposition, yposition):
        self.m_x = float(xposition)
        self.m_y = float(yposition)
    
    def ComputeDistance(self, other_position):
    # Should be a member of Position class? Or not as it is random which position is position1 or 2, see reasoning CheckMeasurementValidity function
        return math.sqrt((self.m_x - other_position.m_x)**2 + (self.m_y - other_position.m_y)**2)    
