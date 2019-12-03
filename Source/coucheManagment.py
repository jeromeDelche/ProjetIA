# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:50:17 2019

@author: jerome

Pour passer de la couche utilisateur à la couche data access
"""

def plateauVersLigneEnregistrement(situation):
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

def ligneEnregistrementVersPlateau(ligneLue):
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