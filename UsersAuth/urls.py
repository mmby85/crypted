from django.urls import path
from . import views


urlpatterns = [
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('adminpage/', views.adminpage, name="adminpage"),
	path('reception/', views.reception, name="reception"),
    path('', views.home, name="home"),
	path('download/', views.dload, name="download"),
]