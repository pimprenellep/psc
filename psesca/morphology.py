# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:26:13 2017

@author: pimpim
"""

class Morphology :
    
    def __init__(self,height, weight):
        self.weights = {'tete': 0.09 * weight, 
                      'tronc_bassin_1': 0.48/2 * weight,
                      'tronc_bassin_2': 0.48/2 * weight,
                      'avant-bras_g': 0.024 * weight,
                      'avant-bras_d': 0.024 * weight,
                      'bras_g': 0.028 * weight, 
                      'bras_d': 0.028 * weight,
                      'cuisse_g': 0.1 * weight, 
                      'cuisse_d': 0.1 * weight,
                      'mollet_g': 0.063 * weight,
                      'mollet_d': 0.063 * weight}
        self.lengths = {'tete': 0.1 * height, 
                         'tronc_bassin_bas': 0.11 * height, 
                         'tronc_bassin_haut': 0.10 * height, 
                         'bassin': 0.08 * height,
                         'largeur':0.23*height,
                         'epaule': 0.2 * height,
                         'avant-bras': 0.22 * height, 
                         'bras': 0.17 * height, 
                         'cuisse': 0.246 * height, 
                         'mollet': 0.325 * height}
    def getParts(self):
        return self.weights.keys()
        
    def getLength(self,part):
        return self.lengths[part]
    
    def getWeight(self,part):
        return self.weights[part]

