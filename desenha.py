import pygame
from config import COLUNA, LINHA, TAMANHO, cor_radar

def desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela):
    for linha in range(LINHA):
        for coluna in range(COLUNA):
            cor = transformado[linha][coluna]
            pygame.draw.rect(janela, cor, (coluna * TAMANHO, linha * TAMANHO, TAMANHO - 1, TAMANHO - 1))

def montar_caminho(posicao_anterior, posicao_atual, janela, transformado):
    goku = pygame.image.load('.\\mapas\\goku.png')
    goku = pygame.transform.scale(goku, (TAMANHO, TAMANHO))

    x_atual, y_atual = posicao_atual
    janela.blit(goku, (y_atual * TAMANHO, x_atual * TAMANHO))
    pygame.display.update()

def desenha_radar(janela, posicao, tamanho, esferas):
    x, y = posicao
    radar_tamanho = 7  # 7x7
    esferas_dentro_radar = []

    for dx in range(-radar_tamanho//2, radar_tamanho//2 + 1):
        for dy in range(-radar_tamanho//2, radar_tamanho//2 + 1):
            px, py = x + dx, y + dy
            if 0 <= px < LINHA and 0 <= py < COLUNA:
                rect = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
                rect.fill(cor_radar)
                janela.blit(rect, (py * tamanho, px * tamanho))
                # Verifica se há uma esfera na posição atual
                if (px, py) in esferas:
                    esferas_dentro_radar.append((px, py))

    return esferas_dentro_radar


def desenha_esferas(janela, esferas, tamanho):
    esfera_img = pygame.image.load('.\\mapas\\esfera.png')
    esfera_img = pygame.transform.scale(esfera_img, (tamanho, tamanho))
    for esfera in esferas:
        janela.blit(esfera_img, (esfera[1] * tamanho, esfera[0] * tamanho))