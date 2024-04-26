'''
Created on 23 April 2024
Author: Adrián Robles Arques

Synthetic photometry generator using GaiaXPy
Intendet to create J-Pas photometry for VOSA.
'''

import numpy as np 
import gaiaxpy as gxpy 
import pandas as pd 

header = ['Name', 'RA', 'DEC', 'Dist', 'Av', 'Filter', 'flux', 'error', 'pntopts', 'objopts']
data = pd.read_csv('Datos/VOSANGC2099HM.txt',names=header,sep='\\t',engine='python')

phot_system = gxpy.PhotometricSystem.JPAS
names = [id for id in data['Name']]

print(names)

Synth_phot = gxpy.generate(names, photometric_system=phot_system, save_file=False)