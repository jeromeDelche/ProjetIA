from django.shortcuts import render, redirect
from .forms import ConnexionForm, RegisterForm
from .models import Profile, GameState, BoardLocation, BoardLocationState
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from Business.JeuEnCarton import PlateauCarton
from Business.IAExpExpV1 import IAExpExpV1
import copy
# Create your views here.
def ConnexionView(request) :
	form = ConnexionForm(request.POST or None)

	if request.user.is_authenticated :
		return redirect('game') 
	if form.is_valid() :
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if user :
			error = False
			login(request, user)
			return redirect('game') #redirect to game
		else :
			error = True
	return render(request, 'jeu/connexion.html', locals())

def RegisterView(request) : 
	form = RegisterForm(request.POST or None)

	if form.is_valid() : 
		profile = Profile()
		profile.user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
		profile.pseudo = form.cleaned_data['nickname']
		profile.save()
		user = authenticate(username = form.cleaned_data['username'],  password = form.cleaned_data['password'])
		login(request, user)
		return redirect('game') 
	
	return render(request, 'jeu/register.html', locals())

def LogoutView(request) : 
	logout(request)
	return redirect('connexion')


@login_required
def GameView(request, direction = "") :
	size = 8
	board = PlateauCarton(size)
	if request.user.profile.gameState : #si le joueur à déjà une partie en cours, crée un plateau et lui fournit l'environement enregistrer dans les models
		state = dict()
		players = dict()

		for location in request.user.profile.gameState.locations.all() :
			state[location.xPos, location.yPos] = BoardLocationState.objects.get(gameState = request.user.profile.gameState, location = BoardLocation.objects.get(xPos = location.xPos, yPos = location.yPos)).playerState

		board.setEnvironement(state)

		players[0] = (request.user.profile.gameState.player0.xPos, request.user.profile.gameState.player0.yPos)
		players[1] = (request.user.profile.gameState.player1.xPos, request.user.profile.gameState.player1.yPos)

		board.setJoueurs(players)

		modelsState = request.user.profile.gameState
		nbDemiTour = modelsState.nbDemiTour
		playerNum = modelsState.playerNum

	else : #sinon, crée un plateau vide
		state = board.getEnvironement()
		players = board.getJoueurs()
		modelsState = GameState.objects.create()
		playerNum = 0
		nbDemiTour = 0
		request.user.profile.gameState = modelsState
		request.user.profile.save()
		#crée les case et l'état des cases si nécessaire 
		for row in range(size) :
			for column in range(size) :
				modelsLocation, isCreate = BoardLocation.objects.get_or_create(xPos = column, yPos = row)
				modelsLocationState = BoardLocationState.objects.get_or_create(playerState = state[column, row], location = modelsLocation, gameState = modelsState)



	if not board.jeuFini() :
		if nbDemiTour%2 != playerNum : #si c'est au tour de l'ia de jouer
			numAI =( 1 if playerNum == 0 else 0)
			ai = IAExpExpV1(numAI)
			direction = ai.joueSerieusement(copy.deepcopy(board))
			while not board.deplacementValide(direction, numAI) :
				direction = ai.joueSerieusement(copy.deepcopy(board))
			board.mouvement(direction, numAI)
			nbDemiTour +=1

		elif nbDemiTour%2 == playerNum and direction in range(4) and board.deplacementValide(direction, playerNum): #si c'est au tour du joueur et que l'argument de direction est valide
			board.mouvement(direction, playerNum)
			nbDemiTour += 1
	elif direction == 4 :
		modelsState.delete()
		return redirect('game')


	score = board.obtenir_score()#récupère les info pour le template
	isFinish = board.jeuFini()

	#mets à jours les models des action effectuées
	state = board.getEnvironement()
	players = board.getJoueurs()
	modelsState.player0 = BoardLocation.objects.get(xPos = players[0][0], yPos = players[0][1])
	modelsState.player1 = BoardLocation.objects.get(xPos = players[1][0], yPos = players[1][1])
	for row in range(size) :
		for column in range(size) :
			location = BoardLocationState.objects.get(location = BoardLocation.objects.get(xPos = column, yPos = row), gameState = modelsState)
			location.playerState = state[column, row]
			location.save()
	modelsState.playerNum = playerNum
	modelsState.nbDemiTour = nbDemiTour 
	modelsState.save();

	autoRefreshNeeded = nbDemiTour%2 != playerNum and not isFinish #si le joueur vient de jouer il faudra rafraichir automatiquement la page pour que l'ia joue

	return render(request, 'jeu/game.html', locals())
