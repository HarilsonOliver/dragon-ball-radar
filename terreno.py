import random
from config import LINHA, COLUNA

def gera_destinos_dinamicos():
    destinos_dinamicos = []
    while len(destinos_dinamicos) < 7:
        destino = (random.randint(0, LINHA - 1), random.randint(0, COLUNA - 1))
        if destino not in destinos_dinamicos:
            destinos_dinamicos.append(destino)
    return destinos_dinamicos

def carrega_terreno(traduz_terreno, transforma_terreno, variavel):
    terreno = traduz_terreno.retorna_terreno()
    return transforma_terreno.transforma_terreno(terreno, variavel)
