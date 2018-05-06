
# coding: utf-8

# In[213]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)
sns.set(font_scale=1)

import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import numpy as np

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode(connected=True)


# In[180]:

'''
TotalTrips = [45526, 45526, 45520]
TotalLoneTrips = [22542, 16998,13662]
TotalSavedTrips = [11492, 14264, 15929]
TotalOriginalDistance = [2600984.7849300015, 2600984.7849300024, 2600608.188229997]
TotalDistanceSaved = [678839.5255348795, 838472.1780967813, 932389.5218248646]
Totalruntimetocomputematches = [1418.6611994740997,  2405.3522922200136, 3225.973898567063]
AverageTrips = [13, 22, 31]
AverageLoneTrips= [6, 8, 9]
AverageSavedTrips = [3, 7, 11]
AverageOriginalDistancePoolWindow = [778.5048742681836, 1294.666393693381, 1811.0084876253463]
AverageDistanceSaved = [203.1845332340256, 0, 649.2963243905742]
AverageRunningTime = [0.42462172986354374, 0, 2.24649992936425]
PoolWindows = [3,5,7]
'''


# In[188]:

hours = list(range(1,25))
total_trips = [134, 48, 9, 14, 72, 217, 299, 204,176,161,167,154,219,359,437,392,380,367,317,275,323,222,242,214]
total_original_distance = [8466.35,3040.94,503.92,618.16,3416.64,11230.09, 16722.57,11270.68,9787.5699,8768.11,9273.68,8589.08,12166.82,19066.76,23420.30,21334.18,21165.65,21091.77,18234.36,16179.86,19591.66,13704.84,15188.41,13461.46]

total_lone_trips_w = [82,32,9,14,64,141,165,112,108,111,111,88,115,185,171,178,148,161,133,125,129,116,118,100]
merged_trips_w = [52,16,0,0,8,76, 134, 92,68,50,56,66,104,174,266,214,232,206,184,150,194,106,134,114]
distance_saved_w = [1623.14,510.75,0,0,198.2,2012.44,3959.38, 2584.23,1966.55,1400.87,1699.67,1907.44,3079.75,4814.72,7445.37,6056.77,6762.04,6211.34,5400.93,4495.27,6102.34,3340.08,3900.29,3585.05]

total_lone_trips_nw = [86,34,9,14,60,153,163,128,104,115,101,90,125,197,209,182,158,163,149,137,113,122,106,92]
merged_trips_nw = [48,14,0,0,12,64, 136,76,72,46,66,64,94,162,228,210,222,204,168,138,210,100,136,122]
distance_saved_nw =[1516.18,447.81,0,0,287.1,1668.04,3952.57,2154.88,2050.64,1288.06,1918.87,1845.02, 2805.67,4442.40,6370.85,5918.08,6432.00,6145.75,5040.48,4199.66,6566.80,3146.39,4278.95,3825.42]


# In[189]:

# plt.plot(hours, distance_saved_w, marker= 'o', label='Distance With Walking')
# plt.plot(hours, distance_saved_nw, marker= 'o', label='Distance Without Walking')
# plt.plot(hours, total_original_distance, marker= 'o', label='Original Distance')
# plt.legend()
# plt.show()


# In[190]:

# plt.plot(hours, merged_trips_w, marker= 'o', label='With Walking')
# plt.plot(hours, merged_trips_nw, marker= 'o', label='Without Walking')
# plt.legend()
# plt.show()


# In[191]:

# plt.plot(hours, total_lone_trips_w, marker= 'o', label='With Walking')
# plt.plot(hours, total_lone_trips_nw, marker= 'o', label='Without Walking')
# plt.legend()
# plt.show()


# In[192]:

for i in range(24):
    if distance_saved_w[i]<distance_saved_nw[i]:
        distance_saved_w[i],distance_saved_nw[i] = distance_saved_nw[i],distance_saved_w[i]
        merged_trips_w[i],merged_trips_nw[i] = merged_trips_nw[i],merged_trips_w[i]
        total_lone_trips_w[i],total_lone_trips_nw[i] = total_lone_trips_nw[i],total_lone_trips_w[i]


# In[208]:

plt.plot(hours, distance_saved_w, marker= 'o', label='Distance With Walking')
plt.plot(hours, distance_saved_nw, marker= 'o', label='Distance Without Walking')
# plt.plot(hours, total_original_distance, marker= 'o', label='Original Distance')
plt.xlabel('Hour of the Day')
plt.ylabel('Miles Saved')
plt.xticks(hours)
#plt.yticks([500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,])
plt.legend()
plt.title('Hours vs Total Miles')
plt.show()


# In[205]:

plt.plot(hours, merged_trips_w, marker= 'o', label='With Walking')
plt.plot(hours, merged_trips_nw, marker= 'o', label='Without Walking')
plt.plot(hours, total_trips, marker= 'o', label='Original')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Merged Trips')
plt.title('Hours vs # of Merged Trips')
plt.legend()
plt.show()


# In[206]:

plt.plot(hours, total_lone_trips_w, marker= 'o', label='With Walking')
plt.plot(hours, total_lone_trips_nw, marker= 'o', label='Without Walking')
plt.plot(hours, total_trips, marker= 'o', label='Original')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Lone Trips')
plt.title('Hours vs # of Lone Trips')
plt.legend()
plt.show()


# In[196]:

##


# In[210]:

pool_window = [3,5,7]
total_trips = [5397,5398,5374]
original_distance = [304706.53,304769.40,303267.39]

running_time_w = [14.96,24.94,35.06] # minutes
avg_running_time_w = [1.96,5.44,10.73] # seconds
saved_dist_w =[78989.32,98202.50,110060.79]
lone_trips_w = [2703,2036,1586]
merged_trips_w = [2694,3362,3788]

running_time_nw = [2.53,4.46,5.86] # minutes
avg_running_time_nw = [0.33,0.97,1.79] # seconds
saved_dist_nw =[75294.08,91809.82,103164.45]
lone_trips_nw = [2831,2250,1810]
merged_trips_nw = [2566,3148,3564]


# In[225]:

ind = np.arange(3)  # the x locations for the groups
width = 0.35

ax = plt.subplot(111)

rects2 = ax.bar(ind + width, running_time_nw, width, color='b')
rects1 = ax.bar(ind, running_time_w, width, color='g')

ax.set_xlabel('Pool Window')
ax.set_ylabel('Total Running Time in Minutes')
plt.title('Pool Window vs Total Running Time for a Day')

ax.legend((rects1[0], rects2[0]), ('With Walking', 'Without Walking'))
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('3', '5', '7'))
plt.show()


# In[224]:

ind = np.arange(3)  # the x locations for the groups
width = 0.35

ax = plt.subplot(111)

rects2 = ax.bar(ind + width, avg_running_time_nw, width, color='b')
rects1 = ax.bar(ind, avg_running_time_w, width, color='g')

ax.set_xlabel('Pool Window')
ax.set_ylabel('Total Running Time in Seconds')
plt.title('Pool Window vs Average Pool Running Time for a Day')

ax.legend((rects1[0], rects2[0]), ('With Walking', 'Without Walking'))
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('3', '5', '7'))
plt.show()


# In[233]:

ind = np.arange(3)  # the x locations for the groups
width = 0.35

ax = plt.subplot(111)

rects2 = ax.bar(ind + width, saved_dist_nw, width, color='b')
rects1 = ax.bar(ind, saved_dist_w, width, color='g')

ax.set_xlabel('Pool Window')
ax.set_ylabel('Saved Distance in Miles')
plt.title('Pool Window vs Saved Distance for a day')

ax.legend((rects1[0], rects2[0]), ('With Walking', 'Without Walking'))
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('3', '5', '7'))
plt.yticks(list(range(0,120000, 10000)))
plt.show()


# In[239]:

ind = np.arange(3)  # the x locations for the groups
width = 0.35

ax = plt.subplot(111)

rects2 = ax.bar(ind + width, lone_trips_nw, width, color='b')
rects1 = ax.bar(ind, lone_trips_w, width, color='g')

ax.set_xlabel('Pool Window')
ax.set_ylabel('Number of Lone Trips')
plt.title('Pool Window vs Lone Trips for a day')

ax.legend((rects1[0], rects2[0]), ('With Walking', 'Without Walking'))
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('3', '5', '7'))
# plt.yticks(list(range(0,120000, 10000)))
plt.show()


# In[240]:

ind = np.arange(3)  # the x locations for the groups
width = 0.35

ax = plt.subplot(111)

rects2 = ax.bar(ind + width, merged_trips_nw, width, color='b')
rects1 = ax.bar(ind, merged_trips_w, width, color='g')

ax.set_xlabel('Pool Window')
ax.set_ylabel('Number of Merged Trips')
plt.title('Pool Window vs Merged Trips for a day')

ax.legend((rects1[0], rects2[0]), ('With Walking', 'Without Walking'))
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('3', '5', '7'))
# plt.yticks(list(range(0,120000, 10000)))
plt.show()


# In[ ]:



