import matplotlib.pyplot as plt

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
          f"contact occurred during the following time intervals: {tagdata.ComputeContactTimes(radius)}")

def CheckMeasurementValidity(tagdata1, tagdata2, tolerance):
    # input: two objects of type TagData
    corrupted_measurement_times = []
    for index, distance_to_other_tag in enumerate(tagdata1.m_distances_to_other_tags):
        distance_from_position = tagdata1.m_tagpositions[index].ComputeDistance(tagdata2.m_tagpositions[index])
        if abs(distance_from_position-distance_to_other_tag) > tolerance:
            corrupted_measurement_times.append([tagdata1.m_measurementtimes[index], abs(distance_from_position-distance_to_other_tag)])
    return corrupted_measurement_times

def ShowContactHotspots(tagdata1, tagdata2, radiusforcontact):
    contacttimes = tagdata1.ComputeContactTimes(radiusforcontact)
    contacttimes = tagdata2.ComputeContactTimes(radiusforcontact)

    # get positions from times
    positions1 = tagdata1.GetPositionsForMeasurementTimes(contacttimes)
    positions2 = tagdata2.GetPositionsForMeasurementTimes(contacttimes)
    x1, y1 = SeparatePositionInXandY(positions1)
    x2, y2 = SeparatePositionInXandY(positions2)

    # draw positions
    fig, ax = plt.subplots()
    ax.plot(x1, y1, 'bo')
    ax.plot(x2, y2, 'r+')
    plt.show()
        
def SeparatePositionInXandY(position_to_separate):
    x = []
    y = []
    for position in position_to_separate:
        x.append(position.m_x)
        y.append(position.m_y)
    return x, y