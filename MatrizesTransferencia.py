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

# Funções auxiliares:

def elementos_paralelo(Z1, Z2):
    return Z1 * Z2 / (Z1 + Z2)