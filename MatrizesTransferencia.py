import numpy as np
import scipy as sc
import math

# Definindo matrizes e funções necessárias para a linha de transmissão

def matriz_impedancia_serie(Z):
    A = 1
    B = Z
    C = 0
    D = 1
    return np.array([[A, B], [C, D]])

def matriz_carga(Z):
    A = 1
    B = 0
    C = 1/Z
    D = 1
    return np.array([[A, B], [C, D]])

def matriz_linha(Z1, Z2):
    A = 1 + Z1/Z2
    B = Z1
    C = Z1/(Z2**2) + 2/Z2
    D = 1 + Z1/Z2
    return np.array([[A, B], [C, D]])

def circuito_T(Z1,Z2,Z3):
    A = 1 + Z1/Z3
    B = Z1 + Z2 + Z1*Z2/Z3
    C = 1/Z3
    D = 1 + Z2/Z3
    return np.array([[A, B], [C, D]])

def transformador_ideal(N1,N2, t = 'D'):
    if t == 'D':
        A = N1/N2
        B = 0
        C = 0
        D = N2/N1
    else:
        A = -N1/N2
        B = 0
        C = 0
        D = -N2/N1
    return np.array([[A, B], [C, D]])

def ligação_cascata(T1, T2):
    return np.dot(T1, T2)

def transformador_real(Z1, Z2, Z3, N1, N2, t = 'D'):
    Tranformador_Ideal = transformador_ideal(N1, N2, t)
    Matriz_T = circuito_T(Z1, Z2, Z3)
    Transformador_real = ligação_cascata(Matriz_T, Tranformador_Ideal)
    return Transformador_real

def conversao_transmissao_para_admitancia(T): # Recebe uma matriz de transmissão
    delta_t = np.linalg.det(T)
    y11 = T[1,1] / T[0,1]
    y12 = - delta_t / T[0,1]
    y21 = -1/T[0,1]
    y22 = T[0,0] / T[0,1]
    return np.array([[y11, y12], [y21, y22]]) # Retorna a matriz de admitancia correspondente

def matriz_admitancia_para_transmissao(Y): # Recebe uma matriz de admitancia
    delta_y = np.linalg.det(Y)
    A = -Y[1,1] / Y[1,0]
    B = -1 / Y[1,0]
    C = -delta_y / Y[1,0]
    D = -Y[0,0] / Y[1,0]
    return np.array([[A, B], [C, D]]) # Retorna a matriz de transmissao correspondente

def associacao_paralelo(T1, T2): # Recebe duas matrizes de transmissão em paralelo
    Y1 = conversao_transmissao_para_admitancia(T1)
    Y2 = conversao_transmissao_para_admitancia(T2)
    Yeq = Y1 + Y2
    Teq = matriz_admitancia_para_transmissao(Yeq)
    return Teq # Retorna a matriz de transmissao equivalente

# Funções auxiliares:

def elementos_paralelos(Z1, Z2):
    return Z1 * Z2 / (Z1 + Z2)

def resolver_equação_2_grau(a,b,c):
    delta = b**2 - 4 * a * c
    raiz_delta = np.sqrt(np.complex128(delta))
    x1 = (-b + raiz_delta) / (2 * a)
    return x1