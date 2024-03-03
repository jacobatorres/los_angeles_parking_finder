from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import JsonResponse
from geopy.distance import geodesic
from website.models import BusinessLocation

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
	print("asd")
	stations = BusinessLocation.objects.values()
	print(stations)
	latitude = request.GET.get('latitude')
	longitude = request.GET.get('longitude')
	user_location = latitude, longitude
	nearest_location_distances = {}



	print(latitude, longitude)

	return JsonResponse({})