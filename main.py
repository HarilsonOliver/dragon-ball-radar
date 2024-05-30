import pygame
import random
import traduz_terreno
import transforma_terreno
import desenha_terreno
from config import *
from terreno import gera_destinos_dinamicos, carrega_terreno
from algoritmo import algoritmo_estrela
from desenha import montar_caminho
from moviepy.editor import VideoFileClip


def desenha_esferas(janela, esferas, tamanho):
    esfera_img = pygame.image.load('.\mapas\esfera.png')
    esfera_img = pygame.transform.scale(esfera_img, (tamanho, tamanho))
    for esfera in esferas:
        janela.blit(esfera_img, (esfera[1] * tamanho, esfera[0] * tamanho))

def reproduz_video(caminho_video):
    clip = VideoFileClip(caminho_video)
    clip.preview()

def main():
    pygame.init()
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Dragon Ball Radar")

    transformado = carrega_terreno(traduz_terreno, transforma_terreno, variavel)
    destinos_dinamicos = gera_destinos_dinamicos()
    partida = inicio

    desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)
    desenha_esferas(janela, destinos_dinamicos, TAMANHO)
    pygame.display.update()

    rodando = True
    agente_movendo = False
    caminhos = []
    esferas_coletadas = 0

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if not agente_movendo:
            posicao_atual = partida

            # Coletar esferas
            for destino in destinos_dinamicos:
                caminho, _ = algoritmo_estrela(transformado, posicao_atual, destino)
                if caminho:
                    caminhos.extend(caminho)
                    posicao_atual = destino
                    esferas_coletadas += 1

            # Voltar ao ponto inicial
            caminho_de_volta, _ = algoritmo_estrela(transformado, posicao_atual, inicio)
            if caminho_de_volta:
                caminhos.extend(caminho_de_volta)

            agente_movendo = True

        if agente_movendo:
            if caminhos:
                proximo_passo = caminhos.pop(0)
                montar_caminho([proximo_passo], proximo_passo, janela)
            else:
                if esferas_coletadas == 7:
                    rodando = False  # Todas as esferas foram coletadas e o agente voltou ao início
                reproduz_video(".\\mapas\\summon.mp4")
                agente_movendo = False

        pygame.time.delay(100)  # Delay para não sobrecarregar a CPU
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
