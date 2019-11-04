# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:31:39 2019

@author: jerom
C'est une toute première version du plateau pour pouvoir vérifier l'IA
Celle-ci ne respecte pas les conventions mis en accord précédement

"""
#  import IAExpExpV1

from random import random

class IARandom : 
    def __init__(self,position_x,position_y,numero):
        #self.position = position_x,position_y
        # position inutile puisqu'elle se trouvera dans environnement
        
        # On suppose que il y ait le numéro 1 et 0
        self.numero = numero
        
    #IARandom jouera toujours en exploration sans retenir ses coups.
    def joueExploration(self,environnement):
        listeLibre = list()
        listePersonnelle = list()
        listeCasePossible = self.casesVoisines(environnement)
        for cellule in listeCasePossible :
            if environnement.appartient(cellule,self.numero):
                listePersonnelle.append(cellule)
            elif environnement.estLibre(cellule):
                listeLibre.append(cellule)
        if(len(listeLibre) != 0):
            caseDestination = listeLibre[(int)(random()*len(listeLibre))]
        else :
            caseDestination = listePersonnelle[(int)(random()*len(listePersonnelle))]
        return self.deplacement(environnement.joueurs[self.numero],caseDestination)
    #voisine à la position et ne sortant pas ou appartenant à l'adversaire    
    def casesVoisines(self,environnement):
        nouvelleListe = [(environnement.joueurs[self.numero][0]-1,environnement.joueurs[self.numero][1]),(environnement.joueurs[self.numero][0]+1,environnement.joueurs[self.numero][1]),(environnement.joueurs[self.numero][0],environnement.joueurs[self.numero][1]-1),(environnement.joueurs[self.numero][0],environnement.joueurs[self.numero][1]+1)]
        
        nouvelleListe = list(filter(lambda cellule :cellule[0]>=0 and cellule[1]>=0 and cellule[0]<8 and cellule[1]<8,nouvelleListe))
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

class PlateauCarton :
    def __init__(self):
        self.tableau=dict()
        for x in range(0,8,1):
            for y in range(0,8,1):
                self.tableau[(x,y)]=-8
        self.joueurs=dict();
        self.joueurs[0]=(0,0)
        self.tableau[(0,0)]=0
        self.joueurs[1]=(7,7)
        self.tableau[(7,7)]=1
        self.listeMouvement= [(1,0),(0,1),(-1,0),(0,-1)]
    
    def appartient(self,cellule,numero):
        return self.tableau[cellule]==numero
    def estLibre(self,cellule):
        return self.tableau[cellule]==-8
    def mouvement(self,deplacement,numero):
        self.joueurs[numero] = self.joueurs[numero][0]+self.listeMouvement[deplacement][0] , self.joueurs[numero][1]+self.listeMouvement[deplacement][1]  
        # maintenant, mouvement(1,0) permet de faire bouger le joueur 0 vers le bas.
        #Puis on 'colorie' la case pour le joueur
        self.tableau[self.joueurs[numero]]=numero
    def dessinePlateau(self):
        for y in range(0,8,1):
            resultat=""
            for x in range(0,8,1):
                if self.tableau[(x,y)]>=0:
                    resultat +=" "
                resultat +=str(self.tableau[(x,y)])
            print(resultat)
    #renvoie un tuple
    def nb_appartient_general(self):
        nb0=0
        nb1=0
        for valeur in self.tableau.values():
            if(valeur==0):
                nb0 +=1
            elif(valeur==1):
                nb1 +=1
        return (nb0,nb1)
            
        
    
class JeuEnCarton :
    def __init__(self):
        self.environnement=PlateauCarton()
        self.joueur0 =IARandom(0,0,0)
        self.joueur1 =IARandom(7,7,1)
        # self.numTour = 1
    #joueur0.joueExploration(environnement)
    
    #fait une partie ou les joueurs joueront exactement 50 fois chaqu'un
    def debutPartie50(self):
        for numTour in range(0,50,1):
            #joueur 0 choisit son action
            deplacement = self.joueur0.joueExploration(self.environnement)
            self.environnement.mouvement(deplacement,0)
            #joueur 1 choisit son action
            deplacement = self.joueur1.joueExploration(self.environnement)
            self.environnement.mouvement(deplacement,1)
            #♠On visualise la situation
            self.environnement.dessinePlateau()
            print(numTour)
        scores = self.environnement.nb_appartient_general()
        print( str(scores[0])+" et "+str(scores[1]))
        # reste à faire : le remplissage des cases quand elles sont entourées
        
        
            
        
    
"""
droite = 0
bas = 1
gauche = 2
haut = 3
((dirOpposée=(dir+2)%4))
"""