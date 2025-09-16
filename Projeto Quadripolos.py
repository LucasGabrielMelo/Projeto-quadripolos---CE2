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
Lt6 = linha_transmissao(100)

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

Carga_1 = mt.matriz_carga(Z1)
Carga_2 = mt.matriz_carga(Z2)
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

Parte_1 = mt.ligação_cascata(impedancia_gerador, T1)
Paralelo = mt.associacao_paralelo(Lt1, Lt2)
Paralelo = mt.associacao_paralelo(Paralelo, Lt3)
Matriz_1 = mt.ligação_cascata(Parte_1, Paralelo) # Matriz até a carga 1 

Paralelo = mt.associacao_paralelo(Lt4, Lt5)
Parte_2 = mt.ligação_cascata(Paralelo, T2)
Matriz_2 = mt.ligação_cascata(Matriz_1, Carga_1)
Matriz_2 = mt.ligação_cascata(Matriz_2, Parte_2) # Matriz até a carga 2

Parte_3 = mt.ligação_cascata(Lt6, T3)
Matriz_3 = mt.ligação_cascata(Matriz_2, Carga_2)
Matriz_3 = mt.ligação_cascata(Matriz_3, Parte_3) # Matriz até a carga 3

Sistema_completo = mt.ligação_cascata(Matriz_3, Carga_3)

#print(Sistema_completo)

# ------------ Determinando a tensão fasorial de saida e a corrente em Z3: --------------------------

'''
Para determinar a corrente e a tensão na carga 3, devemos utilizar a matriz que vai até ela, que é
a matriz_3. A utilizando-a, conseguimos determinar que:

V3 = Vg*Z3/(A*Z3+B)

Onde Vg é a tensão no gerador, A e B são os coeficientes de Matriz_3.
'''

Vg = 63e3
V3 = Vg * Z3 / (Matriz_3[0][0] * Z3 + Matriz_3[0][1])
I3 = V3 / Z3

print(f'\nTensão na carga 3: {np.abs(V3)}\u2220{np.degrees(np.angle(V3))}°')
print(f'Corrente na carga 3: {np.abs(I3)}\u2220{np.degrees(np.angle(I3))}°')

# ---------------------- Tensão e corrente nas cargas Z1 e Z2: -------------------------------------

'''
De forma semelhante a feita para a carga Z3, temos que:
'''

V1 = Vg * Z1 / (Matriz_1[0][0] * Z1 + Matriz_1[0][1])
I1 = V1 / Z1

V2 = Vg * Z2 / (Matriz_2[0][0] * Z2 + Matriz_2[0][1])
I2 = V2 / Z2

print(f'\nTensão na carga 1: {np.abs(V1)}\u2220{np.degrees(np.angle(V1))}°')
print(f'Corrente na carga 1: {np.abs(I1)}\u2220{np.degrees(np.angle(I1))}°')

print(f'\nTensão na carga 2: {np.abs(V2)}\u2220{np.degrees(np.angle(V2))}°')
print(f'Corrente na carga 2: {np.abs(I2)}\u2220{np.degrees(np.angle(I2))}°')

# ---------------------- Corrente no gerador: -----------------------------------------------------

'''
Conhecendo as correntes e tensões nas cargas 1, 2 e 3, podemos fazer um professo inverso até deter-
minar a corrente que sai do gerador, como no código abaixo:
'''

# Corrente da parte 3 do circuito:

Ip_3 = Parte_3[1,0] * V3 + Parte_3[1,1] * I3

# Corrente da parte 2 do circuito:

Ip_2 = Parte_2[1,0] * V2 + Parte_2[1,1] * (Ip_3+I2)

# Corrente da parte 1 do circuito:

I_gerador = Matriz_1[1,0] * V1 + Matriz_1[1,1] * (Ip_2+I1)

print(f'\nCorrente no gerador: {np.abs(I_gerador)}\u2220{np.degrees(np.angle(I_gerador))}°')

# ------------- Potência ativa e reativa no gerador: -------------------------------------------------


