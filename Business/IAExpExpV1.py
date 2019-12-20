# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:21:42 2019

@author: jerome
"""
"""
Ceci est un premier essai pour le fonctionnement d'une IA
Celle ci fonctionne à partir d'une évolution Exploration/Exploitation
et évaluera les situations à partir d'une fonction d'évaluation
"""

import os.path
from os import path
import json
from random import random
# import pickle

# nom : eploration, exploitation, Version 1
class IAExpExpV1 :
    def __init__(self,numero):
        # On suppose que il y ait le numéro 1 et 0
        self.numero = numero 
        self.epsilon_greedy = 1
        #`documents à stocker !
        self.ListeSituationEvalue = None
        # retient les derniers mouvements effectués (clé : num du tour)
        self.dernieresSituations = dict()
        # Note, à 0.002 : on arrive à un epsilon_greedy de 20% qu'au bout de 800 parties
        # à 0.001 : on arrive à epsi-greedy de 20% au bout de 1600 parties
        self.tauxVersExploitation = 0.001
        self.learning_rate = 0.25
        # Se remettra à 1 après chaque fin de partie
        self.num_tour = 1
        self.nomFichier = "./fichierSauvegardeEtat8.txt"
        
        """
        pour lui demander de jouer, il y a deux versions : 
        joueEntrainement (avec apprentissage)
        joueSerieusement (uniquement en exploitation)
        """
    def joueEntrainement(self,environnement) :
        if random() < self.epsilon_greedy : 
            choix=self.joueExploration(environnement)
        else:
            choix=self.joueExploitation(environnement)
        # enregistre la situation avant que le choix ne soit fait.
        self.dernieresSituations[self.num_tour-1]=(environnement.situation())
        self.num_tour += 1
        return choix
            
    def joueSerieusement(self,environnement) :
        choix=self.joueExploitation(environnement)
        return choix
        
    def joueExploration(self,environnement):
        listeLibre = list()
        listePersonnelle = list()
        listeCasesPossibles = self.casesVoisinesValides(environnement)
        for cellule in listeCasesPossibles :
            if environnement.appartient(cellule,self.numero):
                listePersonnelle.append(cellule)
            elif environnement.estLibre(cellule):
                listeLibre.append(cellule)
        if(len(listeLibre) != 0):
            caseDestination = listeLibre[(int)(random()*len(listeLibre))]
        else :
            caseDestination = listePersonnelle[(int)(random()*len(listePersonnelle))]
        return self.deplacement(environnement.joueurs[self.numero],caseDestination)

    
    def joueExploitation(self,environnement):
        # A continuer : valeurDEtat
        listeCasesPossibles = self.casesVoisinesValides(environnement)
        situationActuelle = environnement.situation()
        # les valeurs seront comprise entre -64 et 64
        valeurMax = -100
        # On simule les différents cas possible
        for caseMouvement in listeCasesPossibles :
            #On deplace le joueur dans cette situation
            nouvellePositionJoueur = situationActuelle[1]
            nouvellePositionJoueur[self.numero]=caseMouvement 
            #On colorie la case
            nouveauPlateau = situationActuelle[0]
            nouveauPlateau[caseMouvement]=self.numero
            # Rechercher la valeur dans la BD
            valeurSituation = self.valeurDEtatTotale((nouveauPlateau,nouvellePositionJoueur))
            if(self.numero==0): # on essaye alors de maximiser
                if(valeurSituation>valeurMax):
                    valeurMax=valeurSituation
                    caseOptimal = caseMouvement
            else: # on essaye de minimiser
                if((-valeurSituation)>valeurMax):
                    valeurMax=(-valeurSituation)
                    caseOptimal = caseMouvement
        return self.deplacement(environnement.joueurs[self.numero],caseOptimal)
        
        
    #voisine à la position et ne sortant pas ou appartenant à l'adversaire    
    def casesVoisinesValides(self,environnement):
        nouvelleListe=environnement.casesVoisines(environnement.joueurs[self.numero])
        nouvelleListe = list(filter(lambda cellule : not(environnement.appartient(cellule,(self.numero+1)%2)),nouvelleListe))
        return nouvelleListe
        
    def deplacement(self,caseDepart,caseDestination):
        if (caseDepart[0]==caseDestination[0]):
            if (caseDestination[1]>caseDepart[1]):
                return 1 # vers le bas
            return 3 # vers le haut
        if (caseDestination[0]>caseDepart[0]):
            return 0 # vers la droite
        return 2 # vers la gauche
        
    #Une fois la partie fini, le jeu (classe jeu) envoie cette fonction à l'IA
    def fin_partie(self,environnement):
        # La récompense n'est attribuée qu'à la fin et ne compte que la différence des cases
        scores = environnement.obtenir_score()
        recompense= scores[self.numero]-scores[(self.numero+1)%2]
        #L'exploration se fait dans 20% des cas minimum ... On peut le changer
        self.epsilon_greedy= max(self.epsilon_greedy*(1-self.tauxVersExploitation), 0.2)
        # evaluer les différentes états par les quelles on est passé
        self.evaluationFinPartie(recompense)
        #A faire: Enregistre la partie et les différents mouvements
        
        
    def evaluationFinPartie(self,score) : 
        
        #Si il y a eu 3 tours, num_tour=4 et indice maximum=2 
        indiceSituation= self.num_tour-2
        
        #Modification du score pour cet état
        #Note : puisque les joueurs sont obligé de jouer à chaque tour,
        #  une situation ne peut corespondre qu'au debut d'un seul joueur
        #  via une preuve "par damier" en utilisant la récursivité.
        scorePrecedant=0
        if(self.numero==0):
            self.miseAJourEtatTotale(self.dernieresSituations[indiceSituation],score)
            scorePrecedant=score
        else:
            self.miseAJourEtatTotale(self.dernieresSituations[indiceSituation],-score)
            scorePrecedant=-score
        
        while indiceSituation >0 :
            indiceSituation -=1 
            ancienneValeur = self.valeurDEtatTotale(self.dernieresSituations[indiceSituation])
            nouvelleValeur = ancienneValeur + self.learning_rate*(scorePrecedant-ancienneValeur)
            self.miseAJourEtatTotale(self.dernieresSituations[indiceSituation],nouvelleValeur)
            scorePrecedant= nouvelleValeur
               
                
            
    def valeurDEtatTotale(self,situation):
        ligneEtat = self.plateauVersLigneEnregistrement(situation)
        valeur = self.valeurDEtat(ligneEtat)
        return valeur
    
    def miseAJourEtatTotale(self,situation,valeur):
        ligneEtat = self.plateauVersLigneEnregistrement(situation)
        self.miseAJourEtat(ligneEtat,valeur)
        
            
    def plateauVersLigneEnregistrement(self,situation):
        taillePlateau = 8
        valeurReturn = 0
        for x in range(taillePlateau):
            for y in range(taillePlateau):
                val = situation[0][(x,y)]
                if(val == -8):
                    val = 3
                valeurReturn = (valeurReturn+val)*4
        (valX,valY)=situation[1][0]
        valeurReturn = (valeurReturn+valX)*taillePlateau
        valeurReturn = (valeurReturn+valY)*taillePlateau
        (valX,valY)=situation[1][1]
        valeurReturn = (valeurReturn+valX)*taillePlateau
        valeurReturn = (valeurReturn+valY)*taillePlateau
        return valeurReturn
    
    def ligneEnregistrementVersPlateau(self,ligneLue):
        joueurs = dict()
        plateau = dict()
        taillePlateau = 8
        valY = ligneLue%taillePlateau
        ligneLue=(ligneLue-valY)/taillePlateau
        valX = ligneLue%taillePlateau
        ligneLue=(ligneLue-valX)/taillePlateau
        joueurs[1]=(valX,valY)
        valY = ligneLue%taillePlateau
        ligneLue=(ligneLue-valY)/taillePlateau
        valX = ligneLue%taillePlateau
        ligneLue=(ligneLue-valX)/taillePlateau
        joueurs[0]=(valX,valY)
        x=taillePlateau-1
        
        while(x>=0):
            y=taillePlateau-1
            while(y>=0):
                val = ligneLue%4
                ligneLue=(ligneLue-val)/4
                if(val==3):
                    val=-8
                plateau[(x,y)]=val
                y-=1
            x-=1
        
        return (plateau,joueurs)


    def valeurDEtat(self,situation):
        try :
            if not path.isfile(self.nomFichier) :
                return 0
            else :
                with open(self.nomFichier) as json_file :
                    data = json.load(json_file)
                return data[str(situation)]
        except KeyError :
            return 0
            
            
    def miseAJourEtat(self,situation,valeur):
        try :
            if not path.isfile(self.nomFichier) :
                with open (self.nomFichier,'w+'):
                    data = { }
            else :
                with open(self.nomFichier) as json_file:
                    data = json.load(json_file)
                data[str(situation)] = valeur
            with open(self.nomFichier, 'w') as outfile:
                json.dump(data, outfile)
        except EOFError :
            print("erreur lors de la modification de l'etat")
            
        
    