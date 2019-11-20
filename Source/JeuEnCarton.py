# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:31:39 2019

@author: jerom
C'est une toute première version du plateau pour pouvoir vérifier l'IA
Celle-ci ne respecte pas les conventions mis en accord précédement

"""
#  import IAExpExpV1

"""

colorama : pour permettre d'avoir des couleurs
"""

import time
from random import random

def decoTemps(fonction):
    def nouvelleFonction(*args,**key_args):
        debut=time.time()
        fonction(*args,**key_args)
        fin=time.time()
        print(str(fin-debut)+" secondes")
    return nouvelleFonction

class IARandom : 
    def __init__(self,numero):
        #self.position = position_x,position_y
        # position inutile puisqu'elle se trouvera dans environnement
        
        # On suppose que il y ait le numéro 1 et 0
        self.numero = numero
        
    #IARandom jouera toujours en exploration sans retenir ses coups.
    def joueSerieusement(self,environnement):
        listeLibre = list()
        listePersonnelle = list()
        listeCasePossible = self.casesVoisinesValides(environnement)
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

class PlateauCarton :
    def __init__(self,taille):
        self.taille = taille
        self.tableau=dict()
        self.joueurs=dict()
        #mets à 0 tout le tableau : initialisation!
        self.nettoyePlateau()

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
        #On vérifie si on a pas bloquer des cases...
        
        #Voir la documentation (pour le moment : une feuille de Jérome)
        caseEnFace = self.joueurs[numero][0]+self.listeMouvement[deplacement][0] , self.joueurs[numero][1]+self.listeMouvement[deplacement][1]
        caseCote1 = self.joueurs[numero][0]+self.listeMouvement[(deplacement+1)%4][0] , self.joueurs[numero][1]+self.listeMouvement[(deplacement+1)%4][1]
        caseCote2 = self.joueurs[numero][0]+self.listeMouvement[(deplacement+3)%4][0] , self.joueurs[numero][1]+self.listeMouvement[(deplacement+3)%4][1]
        if (not self.libreRemplissage(caseEnFace,numero)):
            if(self.libreRemplissage(caseCote1,numero) and self.libreRemplissage(caseCote2,numero)):
                self.remplissage([caseCote1,caseCote2],numero)
        else:
            remplissageUtile=False
            listeATester = list()
            caseCote1a = caseCote1[0]+self.listeMouvement[deplacement][0] , caseCote1[1]+self.listeMouvement[deplacement][1]
            caseCote2a = caseCote2[0]+self.listeMouvement[deplacement][0] , caseCote2[1]+self.listeMouvement[deplacement][1]
            if(self.libreRemplissage(caseCote1,numero) and not self.libreRemplissage(caseCote1a,numero)):
                remplissageUtile = True
                listeATester = listeATester+[caseCote1]
            if(self.libreRemplissage(caseCote2,numero) and not self.libreRemplissage(caseCote2a,numero)):
                remplissageUtile = True
                listeATester = listeATester+[caseCote2]
            if remplissageUtile :
                self.remplissage(listeATester+[caseEnFace],numero)

        
    #renvoie true si n'appartient pas à ce joueur et est dans le tableau
    def libreRemplissage(self,case,numJoueur):
        return (case[0]>=0 and case[1]>=0 and case[0]<self.taille and case[1]<self.taille and (not self.appartient(case,numJoueur)))
        
    def casesVoisines(self,case):
        nouvelleListe = [(case[0]-1,case[1]),(case[0]+1,case[1]),(case[0],case[1]-1),(case[0],case[1]+1)]
        
        nouvelleListe = list(filter(lambda cellule :cellule[0]>=0 and cellule[1]>=0 and cellule[0]<self.taille and cellule[1]<self.taille,nouvelleListe))
        return nouvelleListe
    def dessinePlateau(self):
        for y in range(self.taille):
            resultat=""
            for x in range(self.taille):
                if self.tableau[(x,y)]>=0:
                    if self.joueurs[0]==(x,y) or self.joueurs[1]==(x,y):
                        resultat +="J"
                    else:
                        resultat +=" "
                resultat +=str(self.tableau[(x,y)])
            print(resultat)
    
    
    #renvoie un tuple : (score du premier , score du second)
    def obtenir_score(self):
        nb0=0
        nb1=0
        for valeur in self.tableau.values():
            if(valeur==0):
                nb0 +=1
            elif(valeur==1):
                nb1 +=1
        return (nb0,nb1)
    
    def jeuFini(self):
        score0,score1 = self.obtenir_score()
        return (score0+score1)>= self.taille*self.taille
    
    def testRemplissageRecursif(self,ensembleCaseAValide,ensembleCaseValide,numJoueur):
        if not ensembleCaseAValide :
            return True,list(ensembleCaseValide)
        else :
            # trie tableau par distance grace au min
            # pas élégant et plutot complexe 
            
            nouvellesCases = self.casesVoisines(min(ensembleCaseAValide)[1])
            ensembleCaseValide = ensembleCaseValide | set([min(ensembleCaseAValide)])
            ensembleCaseAValide= ensembleCaseAValide-set([min(ensembleCaseAValide)])
            
            for nouvCase in nouvellesCases:
                nouvellesCasesDist =self.distanceMana(nouvCase,self.joueurs[(numJoueur+1)%2])
                if not( self.appartient(nouvCase,numJoueur) or set([(nouvellesCasesDist,nouvCase)])<= (ensembleCaseAValide|ensembleCaseValide) ):
                    # sinon :on n'enregistre pas cette case !
                    if(self.appartient(nouvCase,(numJoueur+1)%2)):
                        return False,list( (ensembleCaseAValide|ensembleCaseValide) )
                    ensembleCaseAValide = set([(nouvellesCasesDist,nouvCase)])|ensembleCaseAValide
            return self.testRemplissageRecursif(ensembleCaseAValide,ensembleCaseValide,numJoueur)
            
    #fonction  qui rempli les cases coincées
    # à partir de d'une liste de case mis en argument (celles dans la liste)
    # numJoueur concerne le joueur qui bloque potentiellement la case.
    #idée :  faire la grosse partie en récursif!
    def remplissage(self,listeCase,numJoueur):
        for case in listeCase:
            listeAtester=[(self.distanceMana(case,self.joueurs[(numJoueur+1)%2]),case)]
            
            estCoince,listeCoince = self.testRemplissageRecursif(set(listeAtester),set(),numJoueur)
            if (estCoince):
                for caseCoince in listeCoince:
                    self.tableau[caseCoince[1]]=numJoueur
                

    def distanceMana(self,caseA,caseB):
        return abs(caseA[0]-caseB[0])+abs(caseA[1]-caseB[1])
    
    def situation(self):
        return (self.tableau,self.joueurs)
     
    # Remet à 0 le plateau pour recommencer une partie
    def nettoyePlateau(self):
        for x in range(self.taille):
            for y in range(self.taille):
                self.tableau[(x,y)]=-8
        self.joueurs[0]=(0,0)
        self.tableau[(0,0)]=0
        self.joueurs[1]=(self.taille-1,self.taille-1)
        self.tableau[(self.taille-1,self.taille-1)]=1
    
    def deplacementValide(self,deplacement,numero):
        caseDestination = self.joueurs[numero][0]+self.listeMouvement[deplacement][0] , self.joueurs[numero][1]+self.listeMouvement[deplacement][1]  
        return caseDestination in list(filter(lambda cellule : not(environnement.appartient(cellule,(self.numero+1)%2)),self.casesVoisines(environnement.joueurs[self.numero])))
        list(filter(lambda cellule : not(environnement.appartient(cellule,(self.numero+1)%2)),nouvelleListe))
    
class JeuEnCarton :
    def __init__(self,longeurPlateau):
        self.environnement=PlateauCarton(longeurPlateau)
        self.joueur0 =IARandom(0)
        self.joueur1 =IARandom(1)
        # self.numTour = 1
    #joueur0.joueExploration(environnement)
    
    
    #fait une partie ou les joueurs joueront exactement 50 fois chaqu'un
    def debutPartie50(self):
        for numTour in range(0,50,1):
            #joueur 0 choisit son action
            deplacement = self.joueur0.joueSerieusement(self.environnement)
            self.environnement.mouvement(deplacement,0)
            #joueur 1 choisit son action
            deplacement = self.joueur1.joueSerieusement(self.environnement)
            self.environnement.mouvement(deplacement,1)
            #On visualise la situation
            print(numTour)
            self.environnement.dessinePlateau()
        score0,score1 = self.environnement.obtenir_score()
        print( str(score0)+" et "+str(score1))
        
    @decoTemps
    def debutPartieNormal(self):
        self.environnement.nettoyePlateau()
        numTour=1
        while (not self.environnement.jeuFini() ):
            #joueur 0 choisit son action
            deplacement = self.joueur0.joueSerieusement(self.environnement)
            self.environnement.mouvement(deplacement,0)
            if(not self.environnement.jeuFini()):
                #joueur 1 choisit son action
                deplacement = self.joueur1.joueSerieusement(self.environnement)
                self.environnement.mouvement(deplacement,1)
                #print("Tour " + str(numTour))
                #self.environnement.dessinePlateau()
            numTour +=1
        print("Nombres de tours : " + str(numTour))
        self.environnement.dessinePlateau()
        score0,score1 = self.environnement.obtenir_score()
        print( str(score0)+" et "+str(score1))
            
        
class JeuEnBois :
    def __init__(self,longeurPlateau):
        self.environnement=PlateauCarton(longeurPlateau)
        self.joueurs = dict()
        self.joueurs[0] =IARandom(0)
        self.joueurs[1] =IARandom(1)
        # self.numTour = 1
        
    @decoTemps
    def debutPartieNormal(self):
        self.environnement.nettoyePlateau()
        numDemiTour=0
        numJoueurActuel =0
        while (not self.environnement.jeuFini() ):
            deplacement = self.joueurs[numJoueurActuel].joueSerieusement(self.environnement)
            while( not self.environnement.deplacementValide(deplacement,numJoueurActuel)):
                #Plus tard : envoyer une exception !
                print("Ce mouvement est incorrect : veuillez en choisir un autre")
                deplacement = self.joueurs[numJoueurActuel].joueSerieusement(self.environnement)
            #joueur 0 choisit son action
            deplacement = self.joueur0.joueSerieusement(self.environnement)
            self.environnement.mouvement(deplacement,0)
            if(not self.environnement.jeuFini()):
                #joueur 1 choisit son action
                deplacement = self.joueur1.joueSerieusement(self.environnement)
                self.environnement.mouvement(deplacement,1)
                #print("Tour " + str(numTour))
                #self.environnement.dessinePlateau()
            numDemiTour +=1
            numJoueurActuel = (numJoueurActuel+1)%2
        print("Nombres de tours : " + str(numDemiTour-1))
        self.environnement.dessinePlateau()
        score0,score1 = self.environnement.obtenir_score()
        print( str(score0)+" et "+str(score1))
            
        
"""        
if __name__ == "__main__" :
    
    @decoTemps
    def testJeu():
        for i in range(2000):
            jeuTest = JeuEnCarton(8)
            jeuTest.debutPartieNormal()
            
    testJeu()
"""
#jeuTest = JeuEnCarton(8)
#jeuTest.debutPartie50()
#jeuTest.debutPartieNormal()
        
#jeuTest.environnement.dessinePlateau()
#jeuTest.environnement.mouvement(0,0)
#jeuTest.environnement.mouvement(1,0)
        
"""
for i in range(10):
    jeuTest = JeuEnCarton(8)
    jeuTest.debutPartieNormal()

"""        
        
    
"""
droite = 0
bas = 1
gauche = 2
haut = 3
((dirOpposée=(dir+2)%4))
"""