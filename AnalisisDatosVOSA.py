"""
Ajuste Initial Mass Function
Salpeter IMF 1955

@autor: Adrián Robles Arques

"""
#Tratamiento de datos -----------------
import numpy as np
import pandas as pd

#Graficos -----------------------------
import matplotlib.pyplot as plt

#Procesado y modelado -----------------
#Usamos numpy --> Polyfit (deg 1)

#Leer archivo de datos y extraer masas (Voy a intentar usar pandas)
def readVOSA(FolderName):
    path = 'C:/Users/Usuario/Desktop/Proyecto Astro/Resultados/'

    archivo = open(path + FolderName + '/results/bestfitp.dat' , 'r')
    lines = archivo.readlines()

    header = lines[2].split()[1:]
    #se nos cuela un (pc) por la separación, redefinimos
    header = header[:4] + header[5:]
    
    VOSAdata = []
    for line in lines[5:]:
        VOSAdata.append(line.split())

    archivo.close()

    return pd.DataFrame(data = VOSAdata, columns = header)

#Código para generar los subconjuntos de datos de un tamaño determinado
def setBins(data, binwide, widelast = True):

    L = len(data)
    N = L//binwide

    data_sorted = data.sort_values(ascending = False)

    bins = []

#Comprobamos si queremos hacer el último bin ancho o añadir solo los restos
    if widelast == True: 
        bins.extend(data_sorted[i*binwide: (i+1)*binwide] for i in range(N-1))
        bins.append(data_sorted[(N-1)*binwide : ])
    
    else:
        bins.extend(data_sorted[i*binwide: (i+1)*binwide] for i in range(N))
        bins.append(data_sorted[(N)*binwide : ])


    return bins

#Extraemos los datos necesarios para el análisis (media, desviación y N, por subconjunto)
def MeanDelta(Bin):
    
    mean = np.array([m.mean() for m in Bin])
    delta = np.array([m.max()-m.min() for m in Bin])
    N = np.array([len(m) for m in Bin])
    
    return N, mean, delta
    
#Realizamos en ajuste lineal, extraemos el coeficiente y su error
def LinAdjust(Bin):
    
    N, mean, delta = MeanDelta(Bin)
    
    X = np.log10(mean)
    Y = np.log10(N/delta)
    
    adjust, cov = np.polyfit(X,Y,1, cov= True)
    gamma = adjust[0]
    gamma_err = np.sqrt(np.diag(cov)[0])
    
    pol1d_fn = np.poly1d(adjust)
    
    return X, Y, gamma, gamma_err, pol1d_fn

#Código para la representación de los datos
def plotAdj(X, Y, gamma, gamma_err, pol1d_fn):
    
    plt.plot(X, Y, 'o', X, pol1d_fn1(X))
    plt.text(X[-1],Y[0],'$\\gamma$ = {0}$\\pm${1}'.format(round(gamma,3), round(gamma_err,3)))
    plt.title('IMF adjustment')
    plt.xlabel('$log_{10}m_i$')
    plt.ylabel('$log_{10}(N_i/\\Delta m_i)$')
    plt.show()
    
    return
    
#Lectura de datos

Folder = 'NGC2099_HMag'
datos = readVOSA(Folder)

#Manejo de datos
#Creamos subsets de las masas (dos cálculos distintos)
Mass1 = datos['M1']
Mass2 = datos['M2']

#Limpiamos los datos
Mass1c = pd.to_numeric(Mass1, errors ='coerce').dropna()
Mass2c = pd.to_numeric(Mass2, errors ='coerce').dropna()

#Creamos los bins
binwide = 10

BinsM1 = setBins(Mass1c, binwide)
BinsM2 = setBins(Mass2c, binwide)

#Ajuste lineal de los datos

X1, Y1, gamma1, gamma1_err, pol1d_fn1 = LinAdjust(BinsM1)

plotAdj(X1, Y1, gamma1, gamma1_err, pol1d_fn1)

X2, Y2, gamma2,  gamma2_err, pol1d_fn2 = LinAdjust(BinsM2)

plotAdj(X2, Y2, gamma2, gamma2_err, pol1d_fn2)