from general_functions import *

data_code_dictionary = {

	"business": ["r4uk-afju", ["location_account", "naics", "primary_naics_description", "location"]],

	"parking_spot_loc": ["s49e-q6j2", ["spaceid", "latlng"]],

	"parking_spot_archived": ["cj8s-ivry", ["SpaceID", "EventTime_Local", "EventTime_UTC", "OccupancyState"]], # will scrape separately

	"parking_spot_realtime": ["e7h6-4a3e", ["spaceid", "eventtime", "occupancystate"]],

	"crime": ["amvf-fr72", ["rpt_id", "lat", "lon", "arst_date"]]

}

# Create a DataFrame
data = {"Name": ["John", "Jane", "Mary", "Adam"],
        "City": ["New York", "Los Angeles", "Chicago", "Houston"]}
df = pd.DataFrame(data)

# Filter the DataFrame by multiple string values in the "City" column
filtered_df = df[df["City"].str.contains("Chi|Hou")]
print(df)
print(filtered_df)



app_val_token = get_secret("app_token_value", "us-east-1")
lacity_password = get_secret("data_lacity_password_value", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)

business_results = get_data_from_la_city(client, data_code_dictionary['business'][0], 0)

results_df = pd.DataFrame.from_records(business_results)
print(results_df)
