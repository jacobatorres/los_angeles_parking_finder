The app will ask for these parameters: the general location of where you want to park, when you want to park, and the radius of parking (setting this to either 1 mile or 0.5 mile for simplicity). Then it will use data from the Lacity website to provide you the top parking areas that most likely has parking, and the top business areas that might have parking.


Datasets used:
	
1. Active Businesses  
	- https://data.lacity.org/Administration-Finance/Listing-of-All-Businesses/r4uk-afju
	- Will only pick restaurants, parks, groceries, and related items. This dataset has a column called "NAICS" which shows the type of business a record is. I will only filter these columns: 44-45 (Retail Trade), 71 (Arts, Entertainment, and Recreation), 72 (Accommodation and Food Services). Might improve on this later.


2. Parking
	- https://data.lacity.org/Transportation/LADOT-Metered-Parking-Inventory-Policies/s49e-q6j2 (has SpaceID, LatLong)
	- https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e (has SpaceID, Time, OccupancyState) (merge with #1)
