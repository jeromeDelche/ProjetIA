from django.contrib import admin
from jeu.models import Profile,GameState, BoardLocationState
# Register your models here.

class GameStateAdmin(admin.ModelAdmin) : 
	list_display = ('player0', 'player1')


admin.site.register(Profile),
admin.site.register(GameState, GameStateAdmin),
admin.site.register(BoardLocationState),
