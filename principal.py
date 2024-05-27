import pygame
import math
import traduz_terreno
import transforma_terreno
import desenha_terreno
import random

# Cores de cada tipo de terreno
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

# Custo de cada tipo de terreno
CUSTO = {
    AGUA: 10,
    GRAMA: 1,
    KAMI: 0,
    MONTANHA: 60
}

pygame.init()

# Dimensões da tela
LARGURA = 800
ALTURA = 800
TAMANHO = 19

# Criação da janela
janela = pygame.display.set_mode((LARGURA, ALTURA))

# Dimensões da matriz do terreno
LINHA = 42
COLUNA = 42

# Constroi o terreno manualmente
terreno = traduz_terreno.retorna_terreno()
transformado = transforma_terreno.transforma_terreno(terreno, variavel)

# Coordenadas do inicio e chegada
inicio = (19, 17)
chegada = (21, 21)

# Sorteio das posições das esferas do dragão
esferas = []
while len(esferas) < 7:
    esfera = (random.randint(0, LINHA - 1), random.randint(0, COLUNA - 1))
    if esfera != inicio and esfera not in esferas:
        esferas.append(esfera)

# Função para verificar a distância entre dois pontos
def verifica_distancia(primeiro_ponto, segundo_ponto):
    x1, y1 = primeiro_ponto
    x2, y2 = segundo_ponto
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

# Classe Celula para representar cada posição no mapa
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

# Função heurística para A*
def heuristica(lugar_atual, destino1):
    return verifica_distancia(lugar_atual.posicao, destino1) * 10

# Função para calcular o custo entre duas células
def custo(lugar_atual, vizinho):
    if vizinho in lugar_atual.vizinhos:
        return lugar_atual.custo + vizinho.custo
    else:
        return float('inf')

# Função para montar o caminho encontrado pelo algoritmo A*
def montar_caminho(caminho_recente, ponto_partida, ponto_chegada):
    esfera = pygame.image.load('./mapas/esfera.png')
    goku = pygame.image.load('./mapas/gradar1.png')
    esfera = pygame.transform.scale(esfera, (TAMANHO, TAMANHO))
    goku = pygame.transform.scale(goku, (TAMANHO, TAMANHO))

    # Desenha o ponto de chegada
    janela.blit(esfera, (ponto_chegada[1] * TAMANHO, ponto_chegada[0] * TAMANHO))

    # Preenche o caminho
    tempo = pygame.time.Clock()

    for quadrado in caminho_recente:
        x, y = quadrado
        rect = pygame.Rect(y * TAMANHO, x * TAMANHO, TAMANHO - 1, TAMANHO - 1)
        janela.blit(goku, (y * TAMANHO, x * TAMANHO))
        pygame.display.update()
        tempo.tick(7)

# Algoritmo A* para encontrar o caminho de menor custo
def algoritmo_estrela(transformado, ponto_partida, ponto_chegada):
    # Cria os espaços do terreno
    espacos = [[Celula((linha, coluna), CUSTO[transformado[linha][coluna]])
                for coluna in range(COLUNA)] for linha in range(LINHA)]

    # Conecta o espaço aos espaços vizinhos
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

    # Adiciona um ponto de partida à lista aberta
    lugar_atual = espacos[ponto_partida[0]][ponto_partida[1]]
    aberta.append(lugar_atual)

    # Loop do algoritmo A*
    while aberta:
        # Encontra a célula na lista aberta com o menor valor de f + h
        lugar_atual = min(aberta, key=lambda quadrado: quadrado.f + quadrado.h)

        if lugar_atual.posicao == ponto_chegada:
            caminho = []
            custo_total = 0
            while lugar_atual:
                caminho.append(lugar_atual.posicao)
                lugar_atual = lugar_atual.pai
                if lugar_atual:
                    custo_total += lugar_atual.custo
            # Retorna o caminho encontrado
            return (caminho[::-1], custo_total)

        # Remove o espaço atual da lista aberta e adiciona na lista fechada
        aberta.remove(lugar_atual)
        fechada.append(lugar_atual)

        # Verifica os vizinhos do espaço atual
        for vizinho in lugar_atual.vizinhos:
            if vizinho in fechada:
                continue

            # Custo do caminho do espaço atual até o vizinho
            novo_g = lugar_atual.g + custo(lugar_atual, vizinho)

            if vizinho not in aberta:
                aberta.append(vizinho)

            # Ignora se o novo caminho for mais longo que o já calculado
            elif novo_g >= vizinho.g:
                continue

            # Atualiza os valores de g, h e f do vizinho
            vizinho.g = novo_g
            vizinho.h = heuristica(vizinho, ponto_chegada)
            vizinho.f = vizinho.g + vizinho.h
            vizinho.pai = lugar_atual

    return None

# Função para verificar esferas dentro do alcance do radar
def verificar_esferas_radar(posicao, esferas, alcance=3):
    esferas_visiveis = []
    for esfera in esferas:
        if verifica_distancia(posicao, esfera) <= alcance:
            esferas_visiveis.append(esfera)
    return esferas_visiveis

# Função para mover o agente explorando o mapa
def explorar_mapa(transformado, posicao_atual, esferas, chegada):
    caminhos_visitados = set()
    esferas_encontradas = []

    while esferas:
        esferas_visiveis = verificar_esferas_radar(posicao_atual, esferas)
        
        if esferas_visiveis:
            menor_custo = float('inf')
            melhor_caminho = None
            proxima_esfera = None

            for esfera in esferas_visiveis:
                caminho, custo_total = algoritmo_estrela(transformado, posicao_atual, esfera)
                if custo_total < menor_custo:
                    menor_custo = custo_total
                    melhor_caminho = caminho
                    proxima_esfera = esfera

            montar_caminho(melhor_caminho, posicao_atual, proxima_esfera)
            posicao_atual = proxima_esfera
            esferas.remove(proxima_esfera)
            esferas_encontradas.append(proxima_esfera)
        else:
            caminho_exploracao = algoritmo_estrela(transformado, posicao_atual, random.choice(list(set([(x, y) for x in range(LINHA) for y in range(COLUNA)]) - caminhos_visitados)))
            montar_caminho(caminho_exploracao[0], posicao_atual, caminho_exploracao[0][-1])
            posicao_atual = caminho_exploracao[0][-1]
            caminhos_visitados.add(posicao_atual)

    # Retorna para a Ilha do Mestre Kame
    caminho_volta, _ = algoritmo_estrela(transformado, posicao_atual, chegada)
    montar_caminho(caminho_volta, posicao_atual, chegada)

# Loop principal do jogo
def main():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)
    explorar_mapa(transformado, inicio, esferas, chegada)

if __name__ == "__main__":
    main()
