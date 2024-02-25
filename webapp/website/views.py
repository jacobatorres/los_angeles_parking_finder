from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 


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