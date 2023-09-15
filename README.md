README

- idea is that you go to a website, and it shows los angeles but classified to hexbins
- the hexbins have color. more green = more walkable, more red = less walkable.
- walkability is based off of these things:
	
	- number of restaurants
		- https://data.lacity.org/A-Prosperous-City/Map-of-Restaurants/ycz4-j47g
		- https://data.lacity.org/A-Prosperous-City/Restaurants-in-LA/ieer-tbdq
		- more restaurants => more walkable.
		- weight: 40%


	- number of parking
		- https://data.lacity.org/Transportation/LADOT-Metered-Parking-Inventory-Policies/s49e-q6j2
		- https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry
		- https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy/e7h6-4a3e
		- more parking = more walkable. My argument here is that if an area has a lot of street parking then that area would have more businesses and places to visit, so it's more walkable. This is not a perfect indicator of walkability (a counter example is that downtown LA has less parking but it's subjectively a walkable area), so I'm giving it a weight of 20%.
		- weight: 20%


	- crime
		- https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8
		- https://data.lacity.org/Public-Safety/Arrest-Data-from-2020-to-Present/amvf-fr72
		- less crime => more walkable. 
		- weight: 40%


	- you can filter by last week, last month, last year, last three years
