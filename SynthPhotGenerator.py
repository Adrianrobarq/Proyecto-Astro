'''
Created on 23 April 2024
Author: Adrián Robles Arques

Synthetic photometry generator using GaiaXPy
Intendet to create J-PAS photometry for VOSA.
'''

import numpy as np 
import gaiaxpy as gxpy 
import pandas as pd 

DocName = 'VOSANGC2099HM'
DocFolder = 'Datos'
DocFormat = 'txt'

header = ['Name', 'RA', 'DEC', 'Dist', 'Av', 'Filter', 'flux', 'error',
          'pntopts', 'objopts']

data = pd.read_csv(DocFolder + '/' + DocName + '.' + DocFormat , names=header,
                   sep='\\t',engine='python')

phot_system = gxpy.PhotometricSystem.JPAS

names = [id for id in data['Name']]

Synth_phot = gxpy.generate(names, photometric_system=phot_system,
                           save_file=False)

Synth_phot.set_index('source_id', inplace=True)

filterbase = 'OAJ/JPAS.'

filterlist = [colname[9:] for colname in Synth_phot.columns[:60]]

newdata = []

data.set_index('Name', inplace=True)

for name in names:
    line = [name]
    for i in data.loc[name]:
        line.append(i)
    newdata.append(line)
    
    for filt in filterlist:
        line = [name]
        for i in data.loc[name]:
            line.append(i)
        line[5] = filterbase + filt
        line[6] = Synth_phot.loc[name]['Jpas_mag_' + filt]
        newdata.append(line)
        
newfilename = DocName + 'SPhot' + 'JPAS'

newfile = open(DocFolder + '/' + newfilename + '.txt', 'w')


for line in newdata:
    for item in line:
        newfile.write(str(item) + '\t')
        
    newfile.write('\n')

newfile.close()
        
        
        