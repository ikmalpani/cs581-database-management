# CS581 Database Management Systems
# Team 3 - Keshav Malpani, Prateek Shekhar Akhauri, Kruneet Patel, Maithreyi Rajagopalan
This project evaluates ride-sharing algorithms on spatio-temporal data. 
The raw data in this case represents nearly 10 million trips in New York City, which cuts down to 188.6 thousand after cleaning the dataset.
A maximum of 4 passengers would be allowed per trip and a maximum of two trips will be combined. Only the static trips are considered. 

The ojective of this project is to compare the merged trips with the individual trips to:
1. determine the total distance or time saved by ridesharing 
2. estimate the total number of trips saved

Initial Data Set-up
1. Data Clean-up
A clean up script datacleanup.py is run on the original data to filter out trips originating around JFK
This is the first script to be run.

2. OSRM
OSRM is set up on a linux machine using the docker machine and is up and running, accepting requests.

3. Data Preprocessing
datapreprocess.py finds distances from a single point source (A possible terminal at JFK) to the original
destinations. OSRM is used to find the trip distance and duration taken to reach the destination.
This is the second script to be run on the cleaned data. This creates a dump csv file to load the database with the
needed data. 

4. Database - MySQL
tripdetails.sql - Creates the tripdetails table and needed indexes to hold data.
dumpdata.sql - This script loads the table with data created from step 3. 
These scripts are executed in the order mentioned below. 

Please ensure that all the data files are on the same directory containing the script.

To use the 'algorithm.py' file, use the following parameters:

> algorithm.py -walk 1 -w 0 -d 8 -hr 0 -hd 23 -o 5_1.txt

> -walk 1 or 0 to control walking - default 1
> -w 0 - 5 . 0 if you want hourly; 1 if u want for 1st week; 2 if you want first 2 weeks...
> -s - 1 or 0 to control social score - default 1
> -p 3 5 7 default 3
> -d - if you choose hourly by giving week as 0, then 1 - 31 corresponding to the day.
> -hr - begin hour (0-23)
> -hd - delta hours (1-23). So you can give 0 1 for 12-1; 8 2 for 8-10 and 0 23 for the whole day.
> -o output file to dump results
You can use -h to see usage.
