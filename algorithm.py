from urllib.request import urlopen
import json
import networkx as nx
import dbconnect
from datetime import timedelta
import timeit
import argparse
import tripdetails

input_for_max_match = nx.Graph()
total_trips = 0
total_lone_trips = 0
total_saved_trips = 0
total_trip_distance = 0
total_saved_distance = 0
total_running_time = 0
total_dg = 0
total_ss = 0
count = 0
merged_trips = []


# ===============================================================================
# Driver function to validate merging and invoke max match on the identified trips
# ===============================================================================

def merge_trips(passenger_constraint,trips,ss,ssw,walk):
    global total_saved_trips
    global total_lone_trips
    global total_trips
    global total_trip_distance
    global total_saved_distance
    global total_running_time
    global count
    global merged_trips
    global total_dg
    global total_ss
    input_for_max_match.clear()
    no_of_trips = 0
    trip_distance = 0

    if trips is not None:
        no_of_trips += len(trips)

    for trip in trips:
        trip_distance += trip.trip_distance

    # initialize the trip processing matrix to -1 to denote that the trips are yet to be processed
    # Merged trip pairs are set to 1 to avoid re-processing.
    start = timeit.default_timer()
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
                if passenger_count <= passenger_constraint and are_trips_mergeable(trip_1, trip_2,ss,ssw,walk):
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
    stop = timeit.default_timer()
    running_time = stop - start
    total_running_time += running_time
    pool_savings = 0
    ss = 0
    dg = 0
    for trip1,trip2 in matched:
        dg = input_for_max_match[trip1][trip2]["distance"]
        ss = input_for_max_match[trip1][trip2]["ss"]
        od = trip1.trip_distance + trip2.trip_distance
        td = dg * od
        sd = od - td
        pool_savings += sd
        merged_trips.append((trip1.trip_id,trip2.trip_id))

    lone_trips = no_of_trips - (len(matched) * 2)
    saved_trips = len(matched)
    total_trips += no_of_trips
    total_saved_trips += saved_trips
    total_lone_trips += lone_trips
    total_trip_distance += trip_distance
    total_saved_distance += pool_savings
    total_dg += dg
    total_ss += ss
    count += 1


# ===============================================================================
# Function to perform the max_matching algorithm by calling the networkx api
# ===============================================================================

def max_matching(input_for_max_match):
    matched = nx.max_weight_matching(input_for_max_match, maxcardinality=True)
    return matched

def are_trips_mergeable(trip_1, trip_2,ss,ssw,walk):
    if (trip_1.willing_to_walk or trip_2.willing_to_walk) and walk:
        return are_trips_mergeable_walk(trip_1,trip_2,ss,ssw)
    else:
        return are_trips_mergeable_no_walk(trip_1, trip_2,ss,ssw)


def are_trips_mergeable_walk(trip_1,trip_2,ss,ssw):
    if trip_1.trip_duration <= trip_2.trip_duration and trip_1.willing_to_walk and len(trip_1.ballparks)>0:
        new_dropoff_lat, new_dropoff_lon = find_best_dropoff(trip_1,trip_2)
        trip_1.dropoff_latitude = new_dropoff_lat
        trip_1.dropoff_longitude = new_dropoff_lon

    if trip_2.trip_duration < trip_1.trip_duration and trip_2.willing_to_walk and len(trip_2.ballparks)>0:
        new_dropoff_lat, new_dropoff_lon = find_best_dropoff(trip_2, trip_1)
        trip_2.dropoff_latitude = new_dropoff_lat
        trip_2.dropoff_longitude = new_dropoff_lon

    return are_trips_mergeable_no_walk(trip_1,trip_2,ss,ssw)


def find_best_dropoff(t1,t2):
    url = "http://localhost:5000/route/v1/driving/" + str(t1.dropoff_longitude) + "," + str(t1.dropoff_latitude) + ";" + str(t2.dropoff_longitude) + "," + str(t2.dropoff_latitude)
    try:
        response = urlopen(url)
        string = response.read().decode('utf-8')
        json_obj = json.loads(string)
        if json_obj is not None:
            min = json_obj['routes'][0]['distance'] * float(0.000621371)
            best_lat = t1.dropoff_longitude
            best_lon = t1.dropoff_longitude
        for l1,l2 in t1.ballparks:
            url = "http://localhost:5000/route/v1/driving/" + l2 + "," + l1 + ";" + str(t2.dropoff_longitude) + "," + str(t2.dropoff_latitude)
            try:
                response = urlopen(url)
                string = response.read().decode('utf-8')
                json_obj = json.loads(string)
                if json_obj is not None:
                    dist = json_obj['routes'][0]['distance'] * float(0.000621371)
                    if dist < min:
                        best_lat = l1
                        best_lon = l2
            except:
                continue
        return best_lat,best_lon
    except:
        return 0,0


def are_trips_mergeable_no_walk(trip_1, trip_2,ss,ssw):
    url = "http://localhost:5000/route/v1/driving/" + str(trip_1.dropoff_longitude) + "," + str(trip_1.dropoff_latitude) + ";" + str(trip_2.dropoff_longitude) + "," + str(trip_2.dropoff_latitude)
    try:
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
                if ss:
                    social_score = calculate_social_score(trip_1.professions,trip_2.professions)
                    sharing_gain = ((1-ssw) * distance_gain) + (ssw * social_score)
                else:
                    sharing_gain = distance_gain
                    social_score = 0
                input_for_max_match.add_nodes_from([trip_1,trip_2])
                input_for_max_match.add_edge(trip_1,trip_2,weight=sharing_gain,distance=distance_gain,ss=social_score)
            return result
        else:
            return False
    except:
        return False

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


def processballparks(points):
    ballparks = []
    if points != '0' and len(points) > 1:
        points = points.split('|')
        for p in points:
            x,y = p.split('#')
            ballparks.append((x,y))
    return ballparks


def check(d1, d2, duration_between, delay_threshold):
    increased_duration = ((d1 + duration_between) - d2) / d2
    if increased_duration <= delay_threshold:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p",default=3,type=int,choices=[3,5,7],help="Pool window in minutes")
    parser.add_argument("-s",default=1,type=int,choices=[0,1],help="Include social scoring?")
    parser.add_argument("-ss",default=0.15,type=float,help="Social scoring weight")
    parser.add_argument("-walk",default=1,type=int,choices=[0,1],help="Include walking?")
    parser.add_argument("-w",default=5,type=int,choices=[0,1,2,3,4,5],help="Run for how many weeks?")
    parser.add_argument("-d",default=10,type=int,choices=range(1,32),help="Enter day for January!")
    parser.add_argument("-hr",default=8,type=int,choices=range(0,24),help="Enter begin hour")
    parser.add_argument("-hd", default=1, type=int, choices=range(1,24), help="Enter hour delta")
    parser.add_argument("-o",required=True,help="Output File")
    args = parser.parse_args()
    pw = args.p
    ss = args.s
    ssw = args.ss
    walk = args.walk
    weeks = args.w
    outfile = args.o
    connection_object = dbconnect.open_db_connection()
    cursor = connection_object.cursor()
    if weeks > 0:
        q = "select * from trip_details where pickup_datetime order by pickup_datetime"
    else:
        day = args.d
        hour = args.hr
        hd = args.hd
        if hour < 10:
            beginhour = str(0) + str(hour)
        else:
            beginhour = str(hour)
        begindate = '2016-01-' + str(day) + ' ' + beginhour + ':00:00'
        q = "select * from trip_details where pickup_datetime >= ('%s') order by pickup_datetime" % (begindate)

    cursor.execute(q)
    first_record = cursor.fetchone()
    if weeks > 0:
        startdate = first_record[1]  # pickup_datetime
        enddate = first_record[1] + timedelta(minutes=pw)  # pool window - 3 minute
        stopdate = startdate + timedelta(weeks=weeks)
    else:
        startdate = first_record[1]  # pickup_datetime
        enddate = startdate + timedelta(minutes=pw)  # pool window - 3 minute
        stopdate = startdate + timedelta(hours=hd)

    while (enddate <= stopdate):
        query = "select * from trip_details where pickup_datetime between ('%s') and ('%s')" % (startdate, enddate)
        cursor.execute(query)
        if cursor == None:
            break
        else:
            trips = []
            for record in cursor:
                trip = tripdetails.TripDetails(record[0], record[1], record[3], record[6], record[7], record[9],
                                                       record[10], record[11], record[12],record[13],record[14],processballparks(record[15]))
                trips.append(trip)
            merge_trips(4,trips,ss,ssw,walk)

            #poll database here, per pool window
            startdate = enddate + timedelta(seconds=1)
            enddate = startdate + timedelta(minutes=pw)

    avg_trips = int(total_trips/count)
    avg_lone_trips = int(total_lone_trips/count)
    avg_saved_trips = int(total_saved_trips/count)
    avg_original_distance = total_trip_distance/count
    avg_saved_distance = total_saved_distance/count
    avg_running_time = total_running_time/count
    avg_ss = total_ss/count
    avg_dg = total_dg/count

    with open(outfile,'w') as f:
        if weeks > 0:
            print("****** Pool window - {} minute - Statistics, Time Period - {} week ******".format(pw,weeks),file = f)
        else:
            print("****** Pool window - {} minute - Statistics, Time Period - 01/{}/2016, Hours Between {}:00:00 and {}:00:00 ******".format(pw, day, hour, hour + hd), file=f)

        print("Merged Trips - {}".format(merged_trips),file = f)
        print("Total Trips - {}".format(total_trips),file = f)
        print("Total Lone Trips - {}".format(total_lone_trips),file = f)
        print("Total Saved Trips - {}".format(total_saved_trips),file = f)
        print("Total Original Distance - {} miles".format(total_trip_distance),file = f)
        print("Total Distance Saved - {} miles".format(total_saved_distance),file = f)
        print("Total Distance Gain - {} ".format(total_dg), file=f)
        print("Total Social score - {} ".format(total_ss), file=f)
        print("Percentage Savings - {}%".format(round((total_saved_distance / total_trip_distance) * 100), 0), file=f)
        print("Total run time to compute matches - {} minutes".format(total_running_time / 60), file=f)
        print("***************************************************************************", file=f)
        print("Average Trips - {}".format(avg_trips), file = f)
        print("Average Lone Trips- {}".format(avg_lone_trips),file = f)
        print("Average Saved Trips - {}".format(avg_saved_trips), file = f)
        print("Average Original Distance in a pool window - {} miles".format(avg_original_distance), file = f)
        print("Average Distance Saved - {} miles".format(avg_saved_distance), file = f)
        print("Average Distance Gain - {}".format(avg_dg), file=f)
        print("Average Social Score - {} ".format(avg_ss), file=f)
        print("Average Running Time - {} seconds".format(avg_running_time), file = f)
        print("***************************************************************************", file = f)
    f.close()

if __name__ == "__main__":
    main()
