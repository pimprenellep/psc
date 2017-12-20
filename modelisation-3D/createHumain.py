# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:23:11 2017

@author: pimpim
"""

"""Création des volumes"""

import * from pyOde;


class humain:
    
    def ___init___(self,morphologie,x0,y0,z0):
        self.corps = {
            'tete': dBodyCreate(dIdWordID), 
            'tronc_bassin_haut': dBodyCreate(dIdWordID),
            'tronc_bassin_bas': dBodyCreate(dIdWordID),
            'avant-bras_d':dBodyCreate(dIdWordID),
            'avant-bras_g':dBodyCreate(dIdWordID),
            'bras_g': dBodyCreate(dIdWordID), 
            'bras_d': dBodyCreate(dIdWordID),
            'cuisse_g': dBodyCreate(dIdWordID), 
            'cuisse_d': dBodyCreate(dIdWordID),
            'mollet_g': dBodyCreate(dIdWordID),
            'mollet_g': dBodyCreate(dIdWordID)}
        
        for(membre in self.corps):
            dBodySetMass(membre, morphologie.poids[membre])
        
        #on commence par le bas !
        dBodySetPosition(corps['mollet_d'],morphologie.taille['largeur']/2,0, morphologie.taille['mollet']/2 )
        dBodySetPosition(corps['mollet_g'],-morphologie.taille['largeur']/2,0, morphologie.taille['mollet']/2 )
        
        dBodySetPosition(corps['cuisse_d'],morphologie.taille['largeur']/2,0, morphologie.taille['mollet']+morphologie['cuisse']/2 )
        dBodySetPosition(corps['cuisse_g'],-morphologie.taille['largeur']/2,0, morphologie.taille['mollet']+morphologie['cuisse']/2 )
        
        dBodySetPosition(corps['tronc_bassin_bas'],0,0,morphologie.taille['mollet']+morphologie.taille['cuisse']+morphologie.taille['tronc_bassin_bas']/2)
        dBodySetPosition(corps['tronc_bassin_haut'],0,0,morphologie.taille['mollet']+morphologie.taille['cuisse']+morphologie.taile['tronc_bassin_bas']+morphologie.taille['tronc_bassin_baut']/2)
        
        