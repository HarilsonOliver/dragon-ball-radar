import pygame
import math
import traduz_terreno
import transforma_terreno
import desenha_terreno
import random

#Cores de cada tipo de terreno
AGUA = (30, 144, 255)
GRAMA = (124, 252, 0)
MONTANHA = (139, 137, 137)
CAMINHO = (224, 224, 224)
PAREDE = (139, 137, 137)
KAMI = (255, 0, 0)


variavel = {
    "AGUA": AGUA,
    "GRAMA": GRAMA,
    "MONTANHA": MONTANHA,
    "KAMI": KAMI,
    "PAREDE": PAREDE,
    "CAMINHO": CAMINHO
}

#Custo de cada tipo de terreno
CUSTO = {
    AGUA: 180,
    GRAMA: 10,
    KAMI: 0,
    MONTANHA: 150
}

pygame.init()

#Dimensões da tela
LARGURA = 800
ALTURA = 800
TAMANHO = 19

#Criação da janela
janela = pygame.display.set_mode((LARGURA, ALTURA))

#Dimensões da matriz do terreno
LINHA = 42
COLUNA = 42

#Constroi o terreno manualmente
terreno = traduz_terreno.retorna_terreno()
transformado = transforma_terreno.transforma_terreno(terreno, variavel)

#Coordenadas do inicio, destinos, espada e chegada
inicio = (19, 17)
destinos_dinamicos = []
esfera = (2,3)
chegada = (7, 8)

while len(destinos_dinamicos) < 7:
    destino = (random.randint(0, LINHA - 1), random.randint(0, COLUNA - 1))
    # Verifica se o destino gerado não é (21,21)
    if destino != (21, 21):
        destinos_dinamicos.append(destino)

def verifica_distancia(primeiro_ponto, segundo_ponto):
    x1,y1 = primeiro_ponto
    x2,y2 = segundo_ponto
    return math.sqrt(((x2-x1)**2) + ((y2 - y1)**2))


class Celula:
    def __init__(self, posicao, custo):
        self.posicao = posicao
        self.custo = custo
        self.vizinhos = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False


    def reset(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False


def heuristica(lugar_atual, destino1):
    return verifica_distancia(lugar_atual.posicao, destino1)*10

def custo(lugar_atual, vizinho):
    if vizinho in lugar_atual.vizinhos:
        return lugar_atual.custo + vizinho.custo
    else:
        return float('inf')


def montar_caminho(caminho_recente, ponto_partida, ponto_chegada):

    esfera = pygame.image.load('.\mapas\esfera.png')
    esfera = pygame.transform.scale(esfera, (TAMANHO, TAMANHO))
    goku = pygame.image.load('.\mapas\gradar1.png')
    goku = pygame.transform.scale(goku, (TAMANHO, TAMANHO))

    #Desenha o ponto de chegada
    janela.blit(esfera, (ponto_chegada[1] * TAMANHO, ponto_chegada[0] * TAMANHO))

    #Preenche o caminho
    tempo = pygame.time.Clock()

    for quadrado in caminho_recente:
        x, y = quadrado
        rect = pygame.Rect(y * TAMANHO, x * TAMANHO, TAMANHO - 1, TAMANHO - 1)
        janela.blit(goku, (y * TAMANHO, x * TAMANHO))
        pygame.display.update()
        tempo.tick(7)


def algoritmo_estrela(transformado, ponto_partida, ponto_chegada):
    #Cria os espaços do terreno
    espacos = [[Celula((linha, coluna), CUSTO[transformado[linha][coluna]])
                for coluna in range(COLUNA)] for linha in range(LINHA)]

    #Conecta o espaço aos espaços vizinhos
    for linha in range(LINHA):
        for coluna in range(COLUNA):
            if linha > 0:
                espacos[linha][coluna].vizinhos.append(espacos[linha-1][coluna])
            if linha < LINHA-1:
                espacos[linha][coluna].vizinhos.append(espacos[linha+1][coluna])
            if coluna > 0:
                espacos[linha][coluna].vizinhos.append(espacos[linha][coluna-1])
            if coluna < COLUNA-1:
                espacos[linha][coluna].vizinhos.append(espacos[linha][coluna+1])


    aberta = []
    fechada = []

    #Adiciona um ponto de partida à lista aberta
    lugar_atual = espacos[ponto_partida[0]][ponto_partida[1]]
    aberta.append(lugar_atual)

    #Loop do algoritmo A*
    while aberta:
        #Encontra a célula na lista aberta com o menor valor de f + h
        lugar_atual = min(aberta, key=lambda quadrado: quadrado.f + quadrado.h)

        if lugar_atual.posicao == ponto_chegada:
            caminho = []
            custo_total = 0
            while lugar_atual:
                caminho.append(lugar_atual.posicao)
                lugar_atual = lugar_atual.pai
                if lugar_atual:
                    custo_total =+ lugar_atual.custo
            #retorna o caminho encontrado
            return (caminho[::-1], custo_total)

        #Remove o espaço atual da lista aberta e adiciona na lista fechada
        aberta.remove(lugar_atual)
        fechada.append(lugar_atual)

        #Verifica os vizinhos do espaço atual
        for vizinho in lugar_atual.vizinhos:
            if vizinho in fechada:
                continue

            #Custo do caminho do espaço atual até o vizinho
            novo_g = lugar_atual.g + custo(lugar_atual,vizinho)

            if vizinho not in aberta:
                aberta.append(vizinho)

            #Ignora se o novo caminho for mais longo que o já calculado
            elif novo_g >= vizinho.g:
                continue

            #Atualiza os valores de g, h e f do vizinho
            vizinho.g = novo_g
            vizinho.h = heuristica(vizinho, ponto_chegada)
            vizinho.f = vizinho.g + vizinho.h
            vizinho.pai = lugar_atual

    return None

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

partida = inicio

while destinos_dinamicos:
    menor = float('inf')
    melhor_caminho = None
    prox_destino = None

    for i in destinos_dinamicos:

        pygame.draw.rect(janela, (255, 0, 0), (inicio[1] * TAMANHO, inicio[0] * TAMANHO, TAMANHO - 1, TAMANHO - 1))

        pygame.draw.rect(janela, (0, 250, 229), (inicio[1] * TAMANHO, inicio[0] * TAMANHO, TAMANHO - 1, TAMANHO - 1))

        caminho, custo_total = algoritmo_estrela(transformado, partida, i)
        if custo_total < menor:
            menor = custo_total
            melhor_caminho = caminho
            prox_destino = i

    desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)

    montar_caminho(melhor_caminho, partida, prox_destino)

    # Se o próximo destino for o primeiro da lista, adicione a espada
    if prox_destino == destinos_dinamicos[0]:
        destinos_dinamicos.append(esfera)
    # Se o próximo destino for a espada, adicione a chegada
    elif prox_destino == esfera:
        destinos_dinamicos.append(chegada)

    janela = pygame.display.set_mode((LARGURA, ALTURA))

    partida = prox_destino
    destinos_dinamicos.remove(prox_destino)