import pygame
from config import TAMANHO, janela

def desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela):
    for linha in range(LINHA):
        for coluna in range(COLUNA):
            cor = transformado[linha][coluna]
            pygame.draw.rect(janela, cor, (coluna * TAMANHO, linha * TAMANHO, TAMANHO - 1, TAMANHO - 1))

def montar_caminho(caminho_recente, ponto_chegada):
    esfera = pygame.image.load('.\mapas\esfera.png')
    esfera = pygame.transform.scale(esfera, (TAMANHO, TAMANHO))
    goku = pygame.image.load('.\mapas\gradar1.png')
    goku = pygame.transform.scale(goku, (TAMANHO, TAMANHO))

    janela.blit(esfera, (ponto_chegada[1] * TAMANHO, ponto_chegada[0] * TAMANHO))
    tempo = pygame.time.Clock()

    for quadrado in caminho_recente:
        x, y = quadrado
        janela.blit(goku, (y * TAMANHO, x * TAMANHO))
        pygame.display.update()
        tempo.tick(7)
