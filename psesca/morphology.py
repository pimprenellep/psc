# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:26:13 2017

@author: pimpim
"""

class Morphology :
    
    def __init__(self,height, weight):
        self.weights = {'total' : weight,
                      'head': 0.09 * weight, 
                      'lbody': 0.48/2 * weight,
                      'ubody': 0.48/2 * weight,
                      'forearm': 0.024 * weight,
                      'arm': 0.028 * weight, 
                      'thigh': 0.1 * weight, 
                      'leg': 0.063 * weight}
        self.lengths = {'head': 0.1 * height, 
                         'lbody': 0.11 * height, 
                         'ubody': 0.10 * height, 
                         'bassin': 0.08 * height, # ???
                         'largeur':0.23*height, # ???
                         'epaule': 0.2 * height, # ???
                         'forearm': 0.22 * height, 
                         'arm': 0.17 * height, 
                         'thigh': 0.246 * height, 
                         'leg': 0.325 * height}
    def getParts(self):
        return self.weights.keys()
        
    def getLength(self,part):
        return self.lengths[part]
    
    def getWeight(self,part):
        return self.weights[part]

