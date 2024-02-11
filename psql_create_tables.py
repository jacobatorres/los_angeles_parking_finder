# create the tables: parking_location, parking_real_time, business_location



"""
--- parking_location ---
* a list all parking spots (long, lat)
* derived from https://data.lacity.org/Transportation/LADOT-Metered-Parking-Inventory-Policies/s49e-q6j2/about_data
spaceid   latlng
VW546  	  {'latitude': '34.062615', 'longitude': '-118.2...


columns:
space_id - varchar
lat - float
lng - float


sample row:
space_id		lat 			lng
VW546			34.062615		-118.223453


--- parking_real_time --- 
* given a parking spot, tell me the time it is OCCUPIED or VACANT
* derived from https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e/about_data
spaceid     eventtime 				occupancystate
CB1181  	2024-01-18T05:23:58.000 VACANT


columns of parking_data are:
space_id - varchar
event_time - datetime (UTC)
occupancy_state - varchar

sample row:
space_id		event_time				occupancy_state
CB1181			2024-01-18T05:23:58.000 VACANT


--- business_location ---
* list of businesses
* Only getting businesses with these naics codes, because I think they're the ones with more public parking:
42* Wholesale Trade
44*-45* Retail Trade
71* Arts Entertainment Recrration
* derived from https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju
location_account   naics   location
0003217523-0001-2  444130  {'latitude': '33.9581', 'longitude': '-118.292...
* will get only those businesses with relevent naics code (those with public parking, etc.). Full list of codes to follow.

columns of business_location are:
location_id - varchar
naics_code - int
lat - float
lng - float




"""


create_parking_location_table = """
CREATE TABLE IF NOT EXISTS parking_location (
	space_id VARCHAR ( 20 ) PRIMARY KEY,
	lat float,
	lng float
)
"""


create_parking_rt_table = """
CREATE TABLE IF NOT EXISTS parking_real_time (
	space_id VARCHAR ( 20 ) PRIMARY KEY,
	event_time timestamptz,
	occupancy_state VARCHAR ( 10 )
)
"""


business_location_table = """
CREATE TABLE IF NOT EXISTS business_location (
	location_id VARCHAR ( 20 ) PRIMARY KEY,
	naics_code int, 
	lat float, 
	lng float
);
"""
