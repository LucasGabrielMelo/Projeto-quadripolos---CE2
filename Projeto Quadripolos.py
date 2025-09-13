import MatrizesTransferencia as mt
import numpy as np

f = 60 # Frequencia em Hz
w = 2 * np.pi * f

# -------------------- Definindo os parâmetros dos transformadores no S.I: ------------------------

# Parâmetros gerais:

R1 = 7.6 * 10 ** (-3)
X1 = 3.8 * 10 ** (-3)
R2 = 33.9 * 10 ** (-3)
X2 = 0.85 * 10 ** (-3)

Z1 = np.complex128(R1 + 1j * X1)
Z2 = np.complex128(R2 + 1j * X2)

# Parâmetros do transformador 1:

Rm1 = 4320
Xm1 = 5050

Zm1 = mt.elementos_paralelo(Rm1, np.complex128(1j * Xm1))

Nt1_1 = 69 # Numero escolhido para representar o N1 do transformador 1
Nt1_2 = 230 # Numero escolhido para representar o N2 do transformador 1

# Parâmetros do transformador 2:

Rm2 = 432000
Xm2 = 505000

Zm2 = mt.elementos_paralelo(Rm2, np.complex128(1j * Xm2))

Nt2_1 = 230  # Numero escolhido para representar o N1 do transformador 2
Nt2_2 = 138 # Numero escolhido para representar o N2 do transformador 2

# Parâmetros do transformador 3:

Rm3 = 4020000
Xm3 = 6070000

Zm3 = mt.elementos_paralelo(Rm3, np.complex128(1j * Xm3))

Nt3_1 = 138  # Numero escolhido para representar o N1 do transformador 3
Nt3_2 = 69 # Numero escolhido para representar o N2 do transformador 3

# ------------------------ Parametros das linhas de transmissão: ---------------------------------

# Parâmetros distribuidos por km:

RL = 0.172 
LL = 2.18 * 10 ** (-3)
CL = 0.0136 * 10 ** (-6)

# Criação da linha:

def linha_transmissao(comprimento): # comprimento em km
    R = RL * comprimento
    L = LL * comprimento
    C = CL * comprimento

    Z1 = np.complex128(R + 1j * w * L)
    Z2 = np.complex128(1 / (1j * w  * C/2))

    Matriz_linha = mt.matriz_linha(Z1, Z2)

    return Matriz_linha

# ------------------------ Criando os elementos do circuito: -----------------------------------------

# Criando os transformadores:

T1 = mt.transformador_real(Z1, Z2, Zm1, Nt1_1, Nt1_2)
T2 = mt.transformador_real(Z1, Z2, Zm2, Nt2_1, Nt2_2)
T3 = mt.transformador_real(Z1, Z2, Zm3, Nt3_1, Nt3_2)

# Criando as linhas de transmissão: 

Lt1 = linha_transmissao(80)
Lt2 = linha_transmissao(80)
Lt3 = linha_transmissao(80)
Lt4 = linha_transmissao(120)
Lt5 = linha_transmissao(120)
Lt6 = linha_transmissao(160)

# Criando a impedância em série no S.I:

Rf = 2
Xf = 0.38

Zf = np.complex128(Rf + 1j * Xf)

impedancia_serie = mt.matriz_impedancia_serie(Zf)


