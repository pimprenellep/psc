# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:48:00 2017

"""

class static morph:
    
    def __init__(taille, poids):
        self.poids = {'tete': 0.09 * poids, 'tronc_bassin': 0.48 * poids,'avant-bras': 0.024 * poids,
                    'bras': 0.028 * poids, 'cuisse': 0.1 * poids, 'mollet': 0.063 * poids};
        self.longeurs = {'tete': 0.1 * taille, 'tronc': 0.21 * taille, 'bassin': 0.08 * taille, 'epaule': 0.2 * taille,
                         'avant-bras': 0.22 * taille, 'bras': 0.17 * taille, 'cuisse': 0.246 * taille, 'mollet': 0.325 * taille};
        
    def getLongeur(partie):
        return self.longeurs[partie];
    
    def getPoid(partie):
        return self.poids[partie];