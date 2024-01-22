# create the tables: business_data, parking_data, crime_data


"""
--- business_data ---
* list of businesses
* the data here is derived from one table.
* 1. from https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju
location_account   naics   location
0003217523-0001-2  444130  {'latitude': '33.9581', 'longitude': '-118.292...


columns of business_data are:
location_id - varchar
naics_code - int
lat - float
lng - float


--- parking_data --- 
* parking spot locations
* when the parking spot was occupied
* the table here is derived from three tables.

* 1. from https://data.lacity.org/Transportation/LADOT-Metered-Parking-Inventory-Policies/s49e-q6j2/about_data
spaceid   latlng
VW546  	  {'latitude': '34.062615', 'longitude': '-118.2...


* 2. archived data  https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry/about_data
SpaceID 	EventTime_Local 		EventTime_UTC			OccupancyState
CB2536 		2021-02-01 00:00:05.000 2021-02-01 08:00:05.000 OCCUPIED


* 3. more real time data https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e/about_data
spaceid     eventtime 				occupancystate
CB1181  	2024-01-18T05:23:58.000 VACANT


columns of parking_data are:
space_id - varchar
lat - float
lng - float
event_time - datetime
occupancy_state - varchar


--- crime_data ---
* listing the crimes and where they happened
* the table here is derived from one table.
* 1. from https://data.lacity.org/Public-Safety/Arrest-Data-from-2020-to-Present/amvf-fr72/about_data
rpt_id     lat      lon        arst_date
231413977  33.9908  -118.4765  2023-07-13T00:00:00.000


crime_id - int
arrest_date - datetime
lat - float
lng - float
"""


create_business_data_table_txt = """
CREATE TABLE IF NOT EXISTS business_data (
	location_id VARCHAR ( 20 ) PRIMARY KEY,
	naics_code int, 
	lat float, 
	lng float
);
"""


create_parking_data_table_txt = """
CREATE TABLE IF NOT EXISTS parking_data (
	event_id int not null generated always as identity (increment by 1),
	space_id VARCHAR ( 7 ), 
	lat float, 
	lng float,
	event_time timestamptz,
	occupancy_state VARCHAR ( 10 ),
	PRIMARY KEY (space_id,event_time)
);
"""


create_crime_data_table_txt = """
CREATE TABLE IF NOT EXISTS crime_data (
	crime_id int PRIMARY KEY,
	arrest_date timestamptz, 
	lat float, 
	lng float
);
"""

