# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:56:22 2024

@author: Adrián Robles Arques

Proyecto Grupo de Astrofísica UA
Manejo de datos VOSA
Estimación de masas de cúmulos estelares abiertos
"""
import numpy as np
import pandas as pd
import os


def CreateVOSAdoc(DocName, dist,RApos = 1 , DEpos = 2 ,namepos = 6, ext = '---',
                  filt = '---', flux = '---', error = '---', 
                  pntopts = '---', objopts = '---'):
    
    path = 'C:/Users/Usuario/Desktop/Proyecto Astro/Datos/'
    
    fichero = open(path + DocName + '.txt', 'r') 
    lineas = fichero.readlines()
    
    tabla = []
    for item in lineas[2:]:
        linea = item.split('\t')
        tabla.append(linea)
    
    fluxpos = flux
    if fluxpos != '---':
        nTabla = [[line[namepos], line[RApos], line[DEpos], dist, str(ext),
               filt, line[fluxpos], error, pntopts, objopts] for line in tabla]
    else:
        nTabla = [[line[namepos], line[RApos], line[DEpos], dist, ext,
               filt, flux, error, pntopts, objopts] for line in tabla]

    fichero.close()

    vosadoc = open(path + 'VOSA' + doc + '.txt', 'w')

    for line in nTabla:
        for item in line:
            vosadoc.write(item + '\t')

        vosadoc.write('\n')

    vosadoc.close()
    
    return

def SetVOSASample(DocName, Len):
    
    path = 'C:/Users/Usuario/Desktop/Proyecto Astro/Datos/'
    
    fichero = open(path + DocName + '.txt', 'r') 
    lineas = fichero.readlines()
    Long = len(lineas)
    print('Estrellas totales: ', Long)
    
    N = Long//Len + 1
    print('Numero de muestras: ', N)
    
    newpath = path + 'Samples{0}/'.format(DocName)
    
    isExist = os.path.exists(newpath)
    
    if not isExist:
        os.makedirs(newpath)
    
    for i in range(N):
        sampledoc = open(newpath + 'sample' + doc + '_{0}.txt'.format(i), 'w')
        
        for j in range(Len):
            pos = i*Len+j
            if pos < Long:
                sampledoc.write(lineas[pos])
                
        sampledoc.close() 

    fichero.close()
    
    return            

doc = 'NGC2099HM'

dist = '1401'

extin = 0.62

fluxpos = 16

CreateVOSAdoc(doc, dist, namepos = 6, flux = fluxpos, ext = extin)

SetVOSASample('VOSA'+ doc, 10)


    

