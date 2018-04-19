from urllib.request import urlopen
import json
import networkx as nx
import dbconnect
from datetime import timedelta
from sys import argv
import tripdetails

input_for_max_match = nx.Graph()
# ===============================================================================
# Driver function to validate merging and invoke max match on the identified trips
# ===============================================================================
def merge_trips(passenger_constraint,trips):
    input_for_max_match.clear()
    no_of_trips = 0
    total_trip_distance = 0

    if trips is not None:
        no_of_trips += len(trips)

    for trip in trips:
        total_trip_distance += trip.trip_distance

    # initialize the trip processing matrix to -1 to denote that the trips are yet to be processed
    # Merged trip pairs are set to 1 to avoid re-processing.
    trips_processed = [[-1 for x in range(no_of_trips)] for y in range(no_of_trips)]
    i = 0
    while i < len(trips):
        j = i + 1
        trip_1 = trips[i]
        while j < len(trips):
            trip_2 = trips[j]
            #Processing un-processed trips alone!
            if (trip_1.trip_id != trip_2.trip_id) and (trips_processed[i][j] == -1):
                passenger_count = trip_1.passenger_count + trip_2.passenger_count
                if passenger_count <= passenger_constraint and are_trips_mergeable(trip_1, trip_2):
                    trips_processed[i][j] = 1
                    trips_processed[j][i] = 1
                else:
                    trips_processed[i][j] = 0
                    trips_processed[j][i] = 0
            else:
                trips_processed[i][j] = 0
                trips_processed[j][i] = 0
            j = j + 1
        i = i + 1
    matched = max_matching(input_for_max_match)
    lone_trips = no_of_trips - (len(matched) * 2)
    saved_trips = len(matched)
    print("The merged trips are {}".format(matched))
    print("Total number of trips in this pool window is {}".format(no_of_trips))
    print("Number of Lone trips in this pool window is {}".format(lone_trips))
    print("Total number of trips saved in this pool window is {}".format(saved_trips))


# ===============================================================================
# Function to perform the max_matching algorithm by calling the networkx api
# ===============================================================================

def max_matching(input_for_max_match):
    matched = nx.max_weight_matching(input_for_max_match, maxcardinality=True)
    return matched

def are_trips_mergeable(trip_1, trip_2):
    #if trip_1.willing_to_walk or trip_2.willing_to_walk:
    #    print("Walking to be coded")
    #else:
    return are_trips_mergeable_no_walk(trip_1, trip_2)


def are_trips_mergeable_no_walk(trip_1, trip_2):
    url = "http://localhost:5000/route/v1/driving/" + trip_1.dropoff_longitude + "," + trip_1.dropoff_lattitude + ";" + trip_2.dropoff_longitude + "," + trip_2.dropoff_lattitude
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    if json_obj is not None:
        duration_between_two_trips = json_obj['routes'][0]['duration']
        distance_between_two_trips = json_obj['routes'][0]['distance'] * float(0.000621371)
        if trip_1.trip_duration <= trip_2.trip_duration:
            edge_one = trip_1.trip_duration
            edge_two = trip_2.trip_duration
            delay_threshold = trip_2.delay_threshold
            distance_one = trip_1.trip_distance
            distance_two = trip_2.trip_distance
        else:
            edge_one = trip_2.trip_duration
            edge_two = trip_1.trip_duration
            delay_threshold = trip_1.delay_threshold
            distance_one = trip_2.trip_distance
            distance_two = trip_1.trip_distance
        result = check(edge_one, edge_two, duration_between_two_trips,delay_threshold)
        if result:
            distance_gain = calculate_distance_gain(distance_one,distance_two,distance_between_two_trips)
            social_score = calculate_social_score(trip_1.professions,trip_2.professions)
            sharing_gain = (0.85 * distance_gain) + (0.15 * social_score)
            input_for_max_match.add_nodes_from([trip_1.trip_id,trip_2.trip_id])
            input_for_max_match.add_edge(trip_1.trip_id,trip_2.trip_id,weight=sharing_gain)
    return result

def calculate_distance_gain(d1,d2,distance_between):
    return float((d1 + distance_between) / (d1 + d2))

def calculate_social_score(p1,p2):
    professions_1 = p1.split('-')
    professions_2 = p2.split('-')
    professions = professions_1 + professions_2
    if any(professions.count(x) > 3 for x in professions):
        return 1
    elif any(professions.count(x) > 2 for x in professions):
        return 0.6667
    elif any(professions.count(x) > 1 for x in professions):
        return 0.3333
    else:
        return 0

def check(d1, d2, duration_between, delay_threshold):
    increased_duration = ((d1 + duration_between) - d2) / d2
    if increased_duration <= delay_threshold:
        return True
    else:
        return False

def main():
    connection_object = dbconnect.open_db_connection()
    cursor = connection_object.cursor()
    cursor.execute("select * from trip_details order by pickup_datetime")
    first_record = cursor.fetchone()
    startdate = first_record[1] #pickup_datetime
    enddate = first_record[1] + timedelta(minutes=3) #pool window - 3 minutes
    while (True):
        query = "select * from trip_details where pickup_datetime between ('%s') and ('%s')" % (startdate, enddate)
        cursor.execute(query)
        if cursor == None:
            break
        else:
            trips = []
            for record in cursor:
                trip = tripdetails.TripDetails(record[0], record[1], record[3], record[6], record[7], record[9],
                                                       record[10], record[11], record[12],record[13],record[14])
                trips.append(trip)
            merge_trips(4,trips)

            #poll database here, per pool window
            startdate = enddate + timedelta(seconds=1)
            enddate = startdate + timedelta(minutes=3)

if __name__ == "__main__":
    main()
