# Class definition to store trip details.

class TripDetails:
    def __init__(self, trip_id,pickup_datetime,passenger_count,dropoff_longitude,dropoff_latitude,
                 trip_duration,trip_distance,delay_threshold,willing_to_walk,walking_threshold,professions,ballparks):
        self.trip_id = trip_id
        self.pickup_datetime = pickup_datetime
        self.passenger_count = passenger_count
        self.dropoff_longitude = dropoff_longitude
        self.dropoff_latitude = dropoff_latitude
        self.trip_duration = trip_duration
        self.trip_distance = trip_distance
        self.delay_threshold = delay_threshold
        self.willing_to_walk = willing_to_walk
        self.walking_threshold = walking_threshold
        self.professions = professions
        self.ballparks = ballparks
