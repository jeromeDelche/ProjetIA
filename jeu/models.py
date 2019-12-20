from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BoardLocation(models.Model) :
	xPos = models.IntegerField()
	yPos = models.IntegerField()

	def __str__(self) :
		return "(" + str(self.xPos) + ":" + str(self.yPos) +")"


class GameState(models.Model) :
	playerNum = models.IntegerField(null = True)
	nbDemiTour = models.IntegerField(null = True)
	locations = models.ManyToManyField(BoardLocation, through='BoardLocationState' )
	player0 = models.ForeignKey(BoardLocation, on_delete=models.CASCADE, null = True, related_name="+")
	player1 = models.ForeignKey(BoardLocation, on_delete=models.CASCADE, null = True, related_name ="+")
	def __str__(self) :
		return "demi-tour n°" + str(self.nbDemiTour)


class BoardLocationState(models.Model) :
	playerState = models.IntegerField(default = -8)
	location = models.ForeignKey(BoardLocation, on_delete = models.CASCADE)
	gameState = models.ForeignKey(GameState, on_delete = models.CASCADE)

	def __str__(self) :
		return str(self.location) +" : " + str(self.playerState)


class Profile(models.Model) :
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	pseudo = models.CharField(max_length = 30)
	gameState = models.OneToOneField(GameState, on_delete = models.SET_NULL, null=True)

	def __str__(self) :
		return str(self.user) + " as " + str(self.pseudo) 