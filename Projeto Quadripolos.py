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

Zm1 = mt.elementos_paralelos(Rm1, np.complex128(1j * Xm1))

Nt1_1 = 69 # Numero escolhido para representar o N1 do transformador 1
Nt1_2 = 230 # Numero escolhido para representar o N2 do transformador 1

# Parâmetros do transformador 2:

Rm2 = 432000
Xm2 = 505000

Zm2 = mt.elementos_paralelos(Rm2, np.complex128(1j * Xm2))

Nt2_1 = 230  # Numero escolhido para representar o N1 do transformador 2
Nt2_2 = 138 # Numero escolhido para representar o N2 do transformador 2

# Parâmetros do transformador 3:

Rm3 = 402000
Xm3 = 607000

Zm3 = mt.elementos_paralelos(Rm3, np.complex128(1j * Xm3))

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

# -------------------------- Parâmetros das cargas no S.I: -------------------------------------------

# Carga 1:

P1 = 29.0464 * 10 ** 6
Q1 = 54.7512 * 10 ** 6 

S1 = np.complex128(P1 + 1j * Q1)

# Carga 2:

P2 = 0.6600 * 10 ** 6
Q2 = 13.3313 * 10 ** 6

S2 = np.complex128(P2 + 1j * Q2)

# Carga 3:

P3 = 36.3169 * 10 ** 6
Q3 = 63.3849 * 10 ** 6

S3 = np.complex128(P3 + 1j * Q3)

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

# Criando a impedância do gerador no S.I:

Rf = 2
Xf = 0.38

Zf = np.complex128(Rf + 1j * Xf)

impedancia_gerador = mt.matriz_impedancia_serie(Zf)

# ---------------------------------- Modelando o sistema: ---------------------------------------------

# Determinando as impedâncias Z1, Z2 e Z3

'''
Conhecendo a potência complexa dissipada pelas cargas Z1, Z2 e Z3 quando estas são submetidas as
suas tensões nominais, que são as tensões de saída dos transformadores T1, T2 e T3, respectivamente,
podemos encontrar suas impedâncias pela equação:

S = V * I*
S = V * (V/Z)*
S = |V|²/Z*
Z = |V|²/S*
'''

Tensao_nominal_1 = 230 * 10 ** 3 # Valor RMS
Tensao_nominal_2 = 138 * 10 ** 3
Tensao_nominal_3 = 69 * 10 ** 3

Z1 = Tensao_nominal_1 ** 2 / np.conjugate(S1)
Z2 = Tensao_nominal_2 ** 2 / np.conjugate(S2)
Z3 = Tensao_nominal_3 ** 2 / np.conjugate(S3)

# Criando a matriz de cada carga:

Carga_1 = mt.matriz_impedancia_serie(Z1)
Carga_2 = mt.matriz_impedancia_serie(Z2)
Carga_3 = mt.matriz_impedancia_serie(Z3) 

print(f'Impedância da carga 1: {Z1}')
print(f'Impedância da carga 2: {Z2}')
print(f'Impedância da carga 3: {Z3}')

# Modelando o sistema:

'''
Para modelar o sistema, podemos usar o seguinte raciocínio: olhando Lt6, T3 e Carga_3 como uma co-
xeção em cascata, elas formaram uma parte do sistema que esta conectada em paralelo com a carga 2.
Essa coneção, por sua vez, esta em cascata com Lt4, Lt5 e T2. Essas partes juntas formam uma cone-
ção em paralelo com Z1 e, finalmente, podemos ver tudo isso como uma coneção em cascata com T1, Lt1,
Lt2 e Lt3.
'''

#  Definindo as partes do sistema:

Parte_3 = mt.ligação_cascata(Lt6, T3) #Parte 3 do sistema

Paralelo = mt.associacao_paralelo(Lt4, Lt5)
Parte_2 = mt.ligação_cascata(Paralelo, T2) # Parte 2 do sistema

Paralelo = mt.associacao_paralelo(Lt1, Lt2)
Paralelo2 = mt.associacao_paralelo(Paralelo, Lt3)
Parte_1 = mt.ligação_cascata(T1, Paralelo2) # Parte 1 do sistema

# Criando o sistema completo:

Sistema = mt.ligação_cascata(Parte_3, Carga_3)
Sistema = mt.associacao_paralelo(Sistema, Carga_2)
Sistema = mt.ligação_cascata(Parte_2, Sistema)
Sistema = mt.associacao_paralelo(Sistema, Carga_1)
Sistema = mt.ligação_cascata(Parte_1, Sistema)

# Adicionando a impedância do gerador:

Sistema_completo = mt.ligação_cascata(impedancia_gerador, Sistema)

#print(Sistema_completo)

# ------------ Determinando a tensão fasorial de saida e a corrente em Z3: --------------------------

'''
Para determinar a tensão fasorial de saída, utilizaremos o Sistema_completo, isso porque sua tensão
de entrada é a tensão da fonte e sua tensão de saída é 0, pois sua saída encontra-se na terra. Des-
sa forma, sendo A, B, C e D os parâmetros de sua matriz de transferência, temos que:

|V1| = |A B| * |0 |
|I1|   |C D|   |I2|

Disso, retiramos que:

V1 = B*I2

I1 = D*I2

Determinando I1, descobrimos a corrente que sai pela fonte
'''

Vac = 69 * 10 **3

I_saida = Vac / Sistema_completo[0,1]
I_gerador = Sistema_completo[1,1] * I_saida

#print(np.abs(I_gerador))

'''
Dessa forma, sendo A, B, C e D os coeficientes da matriz de transmissão da impedância do gerador, a
sua tensão de saída é dada por:

Vac_saida = (Vac - B*I1) / A
'''

Vac_saida = (Vac - impedancia_gerador[0,1] * I_gerador) / impedancia_gerador[0,0]

print(f'\nCorrente no gerador: {np.abs(I_gerador)}\u2220{np.degrees(np.angle(I_gerador))} A')
print(f'Tensão na saida do gerador: {np.abs(Vac_saida)}\u2220{np.degrees(np.angle(Vac_saida))} V')

'''
Para encontrar a corrente na carga Z3, devemos considerar a parte do sistema que vai até ela. Conhe-
cendo a tensão e corrente que sai do gerador e sendo A, B, C e D a matriz de transmissão do sistema
até essa parte, temos que:

|V1| = |A B| * |V3|
|I1|   |C D|   |I3|

Onde V3 é a tensão na saida do quadripolo, que é a tensão que fica sobre a carga. Dessa forma, de-
senvolvendo essa matriz, determinamos que:

V3 =  V1 * Z2 / (A*Z2 + B)
'''

# Construindo o sistema até a carga Z3

Matriz_carga_2_paralelo = mt.matriz_carga(Z2)
Sistema_ate_Z3 = mt.ligação_cascata(Matriz_carga_2_paralelo, Parte_3)
Sistema_ate_Z3 = mt.ligação_cascata(Parte_2, Sistema_ate_Z3)
Sistema_ate_Z3 = mt.associacao_paralelo(Sistema_ate_Z3, Carga_1)
Sistema_ate_Z3 = mt.ligação_cascata(Parte_1, Sistema_ate_Z3)
Sistema_ate_Z3 = mt.ligação_cascata(impedancia_gerador, Sistema_ate_Z3)

A = Sistema_ate_Z3[0,0]
B = Sistema_ate_Z3[0,1]
C = Sistema_ate_Z3[1,0]
D = Sistema_ate_Z3[1,1]

V3 = (Vac - B*I_gerador/D) / (A - B*C/D)

I3 = V3 / Z3

print(f'\nCorrente na carga Z3: {np.abs(I3)}\u2220{np.degrees(np.angle(I3))} A')
print(f'Tensão na carga Z3: {np.abs(V3)}\u2220{np.degrees(np.angle(V3))} V')

# ------- Tensão e corrente nas cargas 1 e 2: -----------------------------------------------------

'''
Podemos obter a tensão e corrente nas cargas 1 e 2 de forma semelhante a feita para a carga 3, des-
sa vez, indo até essas respectivas cargas:
'''

# Tensão e corrente na carga 1:

Sistema_ate_Z1 = mt.ligação_cascata(impedancia_gerador, Parte_1)

A = Parte_1[0,0]
B = Parte_1[0,1]
C = Parte_1[1,0]
D = Parte_1[1,1]


V1 = (Vac - B*I_gerador/D) / (A - B*C/D)

I1 = V1 / Z1

print(f'\nCorrente na carga Z1: {np.abs(I1)}\u2220{np.degrees(np.angle(I1))} A')
print(f'Tensão na carga Z1: {np.abs(V1)}\u2220{np.degrees(np.angle(V1))} V')

# Tensão e corrente na carga 2:

Sistema_ate_Z2 = mt.associacao_paralelo(Parte_2, Carga_1)
Sistema_ate_Z2 = mt.ligação_cascata(Parte_1, Sistema_ate_Z2)
Sistema_ate_Z2 = mt.ligação_cascata(impedancia_gerador, Sistema_ate_Z2)

A = Sistema_ate_Z2[0,0]
B = Sistema_ate_Z2[0,1]
C = Sistema_ate_Z2[1,0]
D = Sistema_ate_Z2[1,1]

V2 = (Vac - B*I_gerador/D) / (A - B*C/D)

I2 = V2 / Z2

print(f'\nCorrente na carga Z2: {np.abs(I2)}\u2220{np.degrees(np.angle(I2))} A')
print(f'Tensão na carga Z2: {np.abs(V2)}\u2220{np.degrees(np.angle(V2))} V')

# ---------------- Potencia ativa e reativa fornecida pelo gerador: -------------------------------

S_gerador = -Vac * np.conjugate(I_gerador)

print(f'\nPotencia complexa fornecida pelo gerador: {S_gerador}')

# -------------- Potencia complexa consumida pelas cargas: -------------------------------------------

S_carga1 = V1 * np.conjugate(I1)
S_carga2 = V2 * np.conjugate(I2)
S_carga3 = V3 * np.conjugate(I3)

S_cargas = S_carga1 + S_carga2 + S_carga3

print(f'Potencia consumida pelas cargas: {S_cargas}')

# --------------------- Potencia complexa no resto do sistema: -----------------------------------------

print(f'Potencia complexa no sistema: {-S_gerador - S_cargas}')