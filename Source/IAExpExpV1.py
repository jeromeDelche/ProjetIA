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
    def __init__(self,position_x,position_y,numero):
        # dépent de la classe joueur
        self.position = position_x,position_y
        # On suppose que il y ait le numéro 1 et 0
        self.numero = numero
        # dépent de la classe joueur        
        self.epsilon_greedy = 1
        self.ListeSituationEvalue = None
        self.dernieresSituations = dict()
        # Note, à 0.002 : on arrive à un epsilon_greedy de 20% qu'au bout de 800 parties
        self.tauxVersExploitation = 0.002
        self.learning_rate = 0.1
        # Se remettra à 1 après chaque fin de partie
        self.num_tour = 1
        
        """
        pour lui demander de jouer, il y a deux versions : 
        joueEntrainement (avec apprentissage)
        joueSerieusement (uniquement en exploitation)
        """
    def joueEntrainement(environnement) :
        if random() < self.epsilon_greedy : 
            choix=joueExploration(environnement)
        else:
            choix=joueExploitation(environnement)
        self.dernieresSituations[num_tour]=(environnement.situation)
        num_tour += 1
        return choix
            
    def joueSerieusement(environnement) :
        choix=joueExploitation(environnement)
        return choix
        
    def joueExploration(environnement):
        listeLibre = list()
        listePersonnelle = list()
        listeCasePossible = casesVoisines()
        for cellule in listeCasePossible :
            if environnement.appartient(cellule,numero):
                listePersonnelle.append(cellule)
            elif environnement.estLibre(cellule):
                listeLibre.append(cellule)
        if(len(listeLibre) != 0):
            caseDestination = listeLibre[(int)(random()*len(listeLibre))]
        else :
            caseDestination = listePersonnelle[(int)(random()*len(listePersonnelle))]
        return deplacement(position,caseDestination)

    
    def joueExploitation(environnement):
        # A continuer
        
    def deplacement(caseDepart,caseDestination):
        deltaX = caseDestination[0]-caseDepart[0]
        deltaY = caseDestination[1]-caseDepart[1]
        if(deltaX == 0):
            if(deltaY > 0):
                return "uparrow"
            return "downarrow"
        if(deltaX > 0):
            return "rightarrow"
        return "leftarrow"
        
    def fin_partie(environnement):
        # La récompense n'est attribuée qu'à la fin et ne compte que la différence des cases
        score = environnement.nb_appartient(numero)-environnement.nb_appartient(numero+1%2)
        #L'exploration se fait dans 20% des cas minimum ... On peut le changer
        self.epsilon_greedy= max(self.epsilon_greedy*(1-self.tauxVersExploitation), 0.2)
        # evaluer les différentes états par les quelles on est passé
        evaluationFinPartie(score)
        # A faire : enregistre la partie et les différents mouvements
        
    def evaluationFinPartie(score) : 
        
    #voisine à la position et ne sortant pas ou appartenant à l'adversaire    
    def casesVoisines():
        nouvelleListe = [(position[0]-1,position[1]),(position[0]+1,position[1]),(position[0],position[1]-1),(position[0],position[1]+1)]
        # Contient une erreur !!!
        nouvelleListe = list(filter((lambda cellule :cellule[0]>=0 and cellule[1]>=0 and cellule[0]<8 and cellule[1]<8,nouvelleListe))
        nouvelleListe = list(filter((lambda cellule : environnement.appartient(cellule,(numero+1)%2),nouvelleListe))
        return nouvelleListe