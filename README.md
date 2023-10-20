The idea is that you go to a website, and it shows los angeles classified to hexbins. The hexbins have color, more green = more walkable, more red = less walkable.
Walkability is based off of these things:
	
1. Number of Active Businesses  
	-  https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju
	- Will only pick restaurants, parks, groceries, and related items. Exhaustive list to follow.
	- more businesses => more walkable.
	- some restaurants close, this counts to that.


2. Number of Parking
	- https://data.lacity.org/Transportation/LADOT-Metered-Parking-Inventory-Policies/s49e-q6j2 (has SpaceID, LatLong)
	- https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry (has SpaceID, Time, OccupancyState) (merge with #1)
	- https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e (has SpaceID, Time, OccupancyState) (merge with #1)
	- less parking = more walkable.


3. Crime
	- https://data.lacity.org/Public-Safety/Arrest-Data-from-2020-to-Present/amvf-fr72
	- less crime => more walkable. 
	- you can filter by last week, last month, last year, last three years



On Processing the Data

Will only get data from 2020 onwards, since that's the year where all three metrics are more complete.

The links/data above can be split into two: the archived data and the real-time data. Archived data is only:
https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry 

Real-time data is:
https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju
https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e
https://data.lacity.org/Public-Safety/Arrest-Data-from-2020-to-Present/amvf-fr72

For archived data, it's already finished data so I'll made an adhoc script to put them in the database. For the real-time data, I'll use Airflow to get data given a specific interval.




