from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import JsonResponse, HttpResponse
from geopy.distance import geodesic
from website.models import BusinessLocation
import json, math

def home(request):
	# if log in, show data, else just the outside

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		# authenticate
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, "You're logged in!")
			return redirect("home")
		else:
			messages.success(request, "Error when logging in, please try again")
			return redirect("home")
	
	else:
		# just see the gomr
		return render(request, 'home.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You're logged out!")
	return redirect('home')


def nearest_station(request):

	latitude = request.GET.get('latitude')
	longitude = request.GET.get('longitude')
	input_location = latitude, longitude

	distances = {}

	list_to_return = []

	# get business locations 
	for datapoint in BusinessLocation.objects.all():
		data_lat_lng = datapoint.lat, datapoint.lng
		distance = geodesic(input_location, data_lat_lng).km
		# distances[distance] = data_lat_lng
		list_to_return.append([datapoint.lat, datapoint.lng, round(distance,2), 'Business'])
	# print(distances)
	# print(data_lat_lng)
	# print(json.dumps(distances))
	print(list_to_return)
	response = JsonResponse(list_to_return, safe=False)
	print(response)
	return response

	# print("asd")
	# stations = BusinessLocation.objects.values()
	# print(stations)
	# user_location = latitude, longitude
	# nearest_location_distances = {}

	# print(latitude, longitude)

	# return JsonResponse({})





