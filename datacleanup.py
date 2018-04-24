import pandas as pd
import numpy as np

df = pd.read_csv("yellow_tripdata_2016-01.csv")
df = df.drop(df[(df.passenger_count <= 0) | (df.passenger_count >= 4) | (df.dropoff_longitude == 0) | (df.dropoff_latitude == 0) | (df.pickup_longitude == 0) | (df.pickup_latitude == 0) | (df.RatecodeID != 2) | (df.trip_distance < 0.1)].index)
df.drop(df.columns[[0,7,8,11,12,13,14,15,16,17,18]],axis=1,inplace=True)
df['pickup_latitude'] = df['pickup_latitude'].apply(lambda x: round(x,4))
df['dropoff_latitude'] = df['dropoff_latitude'].apply(lambda x: round(x,4))
df['pickup_longitude'] = df['pickup_longitude'].apply(lambda x: round(x,4))
df['dropoff_longitude'] = df['dropoff_longitude'].apply(lambda x: round(x,4))
df.index = np.arange(1, len(df) + 1)
df.to_csv("final_input_data.csv",index_label='Trip_Id')
