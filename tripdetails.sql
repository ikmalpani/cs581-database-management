create table trip_details
(
  trip_id                bigint unsigned auto_increment
  primary key,
  pickup_datetime        datetime    null,
  dropoff_datetime       datetime    null,
  passenger_count        int(2)      null,
  pickup_longitude       float       null,
  pickup_latitude        float       null,
  dropoff_longitude      varchar(15) null,
  dropoff_latitude       varchar(15) null,
  original_trip_distance float       null,
  trip_distance          float       null,
  trip_duration          float       null,
  delay_threshold        float       null,
  willing_to_walk        int(1)      null,
  walking_threshold      float       null,
  constraint trip_details_trip_id_uindex
  unique (trip_id),
  constraint trip_id
  unique (trip_id)
);

create index trip_details_idx_2
on trip_details (pickup_datetime);
