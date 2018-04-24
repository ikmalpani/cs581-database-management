from urllib.request import urlopen
import json
import geopy
from geopy.distance import VincentyDistance
import pandas as pd


def calculate_ball_parks(dropoff_latitude, dropoff_longitude, walking_threshold):
	origin = geopy.Point(dropoff_latitude, dropoff_longitude)
	b = 0
	destinations = []
	while b < 360:
		destination = VincentyDistance(miles=walking_threshold/2).destination(origin, b)
		b = b + 45
		lat2, lon2 = destination.latitude, destination.longitude
		destinations.append((round(lat2, 4), round(lon2, 4)))
	return destinations


def get_nearest_point(latitude, longitude, walking_threshold):
	url = 'http://localhost:5000/nearest/v1/foot/' + str(longitude) + ',' + str(latitude) + '?number=1'
	response = json.loads(urlopen(url).read().decode('utf-8'))
	distance = response['waypoints'][0]['distance'] * 0.000621371
	if distance <= (walking_threshold/2):
		return round(response['waypoints'][0]['location'][1], 4), round(response['waypoints'][0]['location'][0], 4)
	else:
		return 0,0


def all_nearest_points(dropoff_latitude, dropoff_longitude, walking_threshold):
	nearest_points = calculate_ball_parks(dropoff_latitude, dropoff_longitude, walking_threshold)

	new_nearest_points = []
	for each in nearest_points:
		new_point = get_nearest_point(each[0],each[1], walking_threshold)
		if new_point != (0,0):
			new_nearest_points.append(new_point)

	new_field = "|".join(str(i[0])+'#'+str(i[1]) for i in new_nearest_points)
	return new_field

df = pd.read_csv('dump_data.csv', index_col = [0], header=None)

new_col = []

for index, row in df.iterrows():
	dropoff_longitude, dropoff_latitude, walking_threshold = row[6], row[7], row[13]
	if walking_threshold > 0:
		final_points = all_nearest_points(dropoff_latitude, dropoff_longitude, walking_threshold)
		new_col.append(final_points)
	else:
		new_col.append(0)

df[15] = new_col

df.to_csv('dump_data_with_walking_d.csv', header=False)