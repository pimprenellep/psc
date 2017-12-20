# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:26:13 2017

@author: pimpim
"""

class morph :
    
    def __init__(self,taille, poids):
        self.poids = {'tete': 0.09 * poids, 
                      'tronc_bassin_1': 0.48/2 * poids,
                      'tronc_bassin_2': 0.48/2 * poids,
                      'avant-bras_g': 0.024 * poids,
                      'avant-bras_d': 0.024 * poids,
                      'bras_g': 0.028 * poids, 
                      'bras_d': 0.028 * poids,
                      'cuisse_g': 0.1 * poids, 
                      'cuisse_d': 0.1 * poids,
                      'mollet_g': 0.063 * poids,
                      'mollet_d': 0.063 * poids}
        self.longeurs = {'tete': 0.1 * taille, 
                         'tronc_bassin_bas': 0.11 * taille, 
                         'tronc_bassin_haut': 0.10 * taille, 
                         'bassin': 0.08 * taille,
                         'largeur':0.23*taille,
                         'epaule': 0.2 * taille,
                         'avant-bras': 0.22 * taille, 
                         'bras': 0.17 * taille, 
                         'cuisse': 0.246 * taille, 
                         'mollet': 0.325 * taille}
        
    def getLongeur(self,partie):
        return self.longeurs[partie]
    
    def getPoid(self,partie):
        return self.poids[partie]
        
        