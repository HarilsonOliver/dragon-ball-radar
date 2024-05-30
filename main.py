import pygame
import random
import traduz_terreno
import transforma_terreno
import desenha_terreno
from config import LARGURA, ALTURA, TAMANHO, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, variavel, inicio, chegada
from terreno import gera_destinos_dinamicos

def desenha_esferas(janela, esferas, tamanho):
    esfera_img = pygame.image.load('.\mapas\esfera.png')
    esfera_img = pygame.transform.scale(esfera_img, (tamanho, tamanho))
    for esfera in esferas:
        janela.blit(esfera_img, (esfera[1] * tamanho, esfera[0] * tamanho))

def main():
    pygame.init()
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Dragon Ball Radar")

    terreno = traduz_terreno.retorna_terreno()
    transformado = transforma_terreno.transforma_terreno(terreno, variavel)
    destinos_dinamicos = gera_destinos_dinamicos()

    desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)
    desenha_esferas(janela, destinos_dinamicos, TAMANHO)
    pygame.display.update()

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

    pygame.quit()

if __name__ == "__main__":
    main()
