from django.urls import path
from . import views

urlpatterns = [
	path('', views.ConnexionView, name = "connexion"),
	path('register/', views.RegisterView, name = "register"),
	path('logout/', views.LogoutView, name = "logout"),
	path('game/', views.GameView, name="game"),
	path('game/<int:direction>', views.GameView, name="gameWithArgument")
]