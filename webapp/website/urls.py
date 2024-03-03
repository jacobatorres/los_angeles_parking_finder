from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('get-nearest-station/', views.nearest_station, name="nearest_station")
]
