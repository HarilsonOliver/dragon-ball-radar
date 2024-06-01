import math
from config import CUSTO
from celula import Celula

def verifica_distancia(primeiro_ponto, segundo_ponto):
    x1, y1 = primeiro_ponto
    x2, y2 = segundo_ponto
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def heuristica(lugar_atual, destino1):
    return verifica_distancia(lugar_atual.posicao, destino1) * 10

def custo(lugar_atual, vizinho):
    if vizinho in lugar_atual.vizinhos:
        return lugar_atual.custo + vizinho.custo
    else:
        return float('inf')

def algoritmo_estrela(transformado, ponto_partida, ponto_chegada):
    LINHA = len(transformado)
    COLUNA = len(transformado[0])
    espacos = [[Celula((linha, coluna), CUSTO[transformado[linha][coluna]])
                for coluna in range(COLUNA)] for linha in range(LINHA)]

    for linha in range(LINHA):
        for coluna in range(COLUNA):
            if linha > 0:
                espacos[linha][coluna].vizinhos.append(espacos[linha - 1][coluna])
            if linha < LINHA - 1:
                espacos[linha][coluna].vizinhos.append(espacos[linha + 1][coluna])
            if coluna > 0:
                espacos[linha][coluna].vizinhos.append(espacos[linha][coluna - 1])
            if coluna < COLUNA - 1:
                espacos[linha][coluna].vizinhos.append(espacos[linha][coluna + 1])

    aberta = []
    fechada = []

    lugar_atual = espacos[ponto_partida[0]][ponto_partida[1]]
    aberta.append(lugar_atual)

    while aberta:
        lugar_atual = min(aberta, key=lambda quadrado: quadrado.f + quadrado.h)

        if lugar_atual.posicao == ponto_chegada:
            caminho = []
            custos = []
            while lugar_atual:
                caminho.append(lugar_atual.posicao)
                if lugar_atual.pai:
                    custos.append(lugar_atual.custo)
                lugar_atual = lugar_atual.pai
            return (caminho[::-1], custos[::-1])  # Retornar os custos dos passos

        aberta.remove(lugar_atual)
        fechada.append(lugar_atual)

        for vizinho in lugar_atual.vizinhos:
            if vizinho in fechada:
                continue

            novo_g = lugar_atual.g + custo(lugar_atual, vizinho)

            if vizinho not in aberta:
                aberta.append(vizinho)

            elif novo_g >= vizinho.g:
                continue

            vizinho.g = novo_g
            vizinho.h = heuristica(vizinho, ponto_chegada)
            vizinho.f = vizinho.g + vizinho.h
            vizinho.pai = lugar_atual

    return None
