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

from random import random

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
        self.tauxVersExploitation = 0.002
        self.learning_rate = 0.25
        # Se remettra à 1 après chaque fin de partie
        self.num_tour = 1
        
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
        valeurMax = -100
        for caseMouvement in listeCasesPossibles :
            #On deplace le joueur dans cette situation
            nouvellePositionJoueur = situationActuelle[1]
            nouvellePositionJoueur[self.numero]=caseMouvement 
            #On colorie la case
            nouveauPlateau = situationActuelle[0]
            nouveauPlateau[caseMouvement]=self.numero
            # A faire: rechercher la valeur dans la BD
            valeurSituation=0
            #valeurSituation = self.valeurDEtat((nouveauPlateau,nouvellePositionJoueur))
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
        # A continuer: miseAJourEtat
        
        #Si il y a eu 3 tours, num_tour=4 et indice maximum=2 
        indiceSituation= self.num_tour-2
        
        #Modification du score pour cet état
        #Note : puisque les joueurs sont obligé de jouer à chaque tour,
        #  une situation ne peut corespondre qu'au debut d'un seul joueur
        #  via une preuve "par damier" en utilisant la récursivité.
        scorePrecedant=0
        if(self.numero==0):
            #self.miseAJourEtat(self.dernieresSituations[indiceSituation],score)
            scorePrecedant=score
        else:
            #self.miseAJourEtat(self.dernieresSituations[indiceSituation],-score)
            scorePrecedant=-score
        
        while indiceSituation >0 :
            indiceSituation -=1 
            # ancienneValeur = self.valeurDEtat(self.dernieresSituations[indiceSituation])
            nouvelleValeur = ancienneValeur + self.learning_rate*(scorePrecedant-ancienneValeur)
            #self.miseAJourEtat(self.dernieresSituations[indiceSituation],nouvelleValeur)
            scorePrecedant= nouvelleValeur
               
