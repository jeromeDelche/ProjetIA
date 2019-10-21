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
    def __init__(self,position,numero):
        # dépent de la classe joueur
        self.position = position
        # On suppose que il y ait le numéro 1 et 0
        self.numero = numero
        # dépent de la classe joueur        
        self.epsilon_greedy = 1
        self.ListeSituationEvalue = None
        # Note, à 0.002 : on arrive à un epsilon_greedy de 20% qu'au bout de 800 parties
        self.tauxVersExploitation = 0.002
        self.dernieresSituations = dict()
        self.learning_rate = 0.1
        self.num_tour = 1
        
    def joueEntrainement(environnement) :
        if random() < self.epsilon_greedy : 
            choix=joueExploration(environnement)
        else:
            choix=joueExploitation(environnement)
        #L'exploration se fait dans 20% des cas minimum ... On peut le changer
        self.epsilon_greedy= max(self.epsilon_greedy*(1-self.tauxVersExploitation), 0.2)
        self.dernieresSituations[num_tour]=(environnement.situation)
        num_tour += 1
        return choix
            
    def joueSerieusement(environnement) :
        choix=joueExploitation(environnement)
        return choix
        
    def joueExploration(environnement):
        listeLibre = list()
        listePersonnelle = list()
        for cellule in environement.caseVoisine(self.position):
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
        # A continuer
    
        
    def fin_partie(environnement):
        score = environnement.nb_appartient(numero)-environnement.nb_appartient(numero%2)
        # A continuer : evaluer les différentes états par les quelles on est passé