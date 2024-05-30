import pygame
import random
import traduz_terreno
import transforma_terreno
import desenha_terreno
from config import *
from terreno import gera_destinos_dinamicos, carrega_terreno
from algoritmo import algoritmo_estrela
from desenha import montar_caminho, desenha_radar
from moviepy.editor import VideoFileClip

def desenha_esferas(janela, esferas, tamanho):
    esfera_img = pygame.image.load('.\\mapas\\esfera.png')
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
    agente_movendo = True
    caminhos = []
    esferas_coletadas = 0
    posicao_anterior = None
    retorno_inicial = False

    # Posição inicial do agente
    posicao_atual = partida
    direcao = (0, 1)  # Começa movendo para a direita

    # Passo inicial: mover até a primeira célula (0,0) usando A*
    caminho_inicial, _ = algoritmo_estrela(transformado, partida, (0, 0))
    caminhos.extend(caminho_inicial)

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if agente_movendo:
            if caminhos:
                proximo_passo = caminhos.pop(0)
                montar_caminho(posicao_anterior, proximo_passo, janela, transformado)
                esferas_no_radar = desenha_radar(janela, proximo_passo, TAMANHO, destinos_dinamicos)
                
                # Verificar e coletar esferas dentro do radar
                if esferas_no_radar:
                    for esfera in esferas_no_radar:
                        if esfera in destinos_dinamicos:
                            # Mover o agente até a esfera e coletar
                            caminho_para_esfera, _ = algoritmo_estrela(transformado, proximo_passo, esfera)
                            caminhos = caminho_para_esfera + caminhos
                            destinos_dinamicos.remove(esfera)
                            esferas_coletadas += 1
                            break  # Sair do loop após encontrar uma esfera

                posicao_anterior = proximo_passo
                posicao_atual = proximo_passo
            else:
                if esferas_coletadas == 7 and not retorno_inicial:
                    retorno_inicial = True
                    
                elif retorno_inicial:
                    caminho_de_volta, _ = algoritmo_estrela(transformado, posicao_atual, inicio)
                    if caminho_de_volta:
                        caminhos.extend(caminho_de_volta)
                else:
                    # Mover o agente célula por célula em padrão zig-zag
                    if direcao == (0, 1):  # Direita
                        if posicao_atual[1] < COLUNA - 1:
                            proxima_posicao = (posicao_atual[0], posicao_atual[1] + 1)
                        else:
                            direcao = (1, 0)  # Baixo
                            proxima_posicao = (posicao_atual[0] + 1, posicao_atual[1])
                    elif direcao == (0, -1):  # Esquerda
                        if posicao_atual[1] > 0:
                            proxima_posicao = (posicao_atual[0], posicao_atual[1] - 1)
                        else:
                            direcao = (1, 0)  # Baixo
                            proxima_posicao = (posicao_atual[0] + 1, posicao_atual[1])
                    elif direcao == (1, 0):  # Baixo
                        if posicao_atual[0] < LINHA - 1:
                            proxima_posicao = (posicao_atual[0] + 1, posicao_atual[1])
                            if posicao_atual[1] == COLUNA - 1:
                                direcao = (0, -1)  # Esquerda
                            elif posicao_atual[1] == 0:
                                direcao = (0, 1)  # Direita
                        else:
                            proxima_posicao = posicao_atual

                    esferas_no_radar = desenha_radar(janela, posicao_atual, TAMANHO, destinos_dinamicos)
                    if esferas_no_radar:
                        for esfera in esferas_no_radar:
                            caminhos.extend(algoritmo_estrela(transformado, posicao_atual, esfera)[0])
                            destinos_dinamicos.remove(esfera)
                            esferas_coletadas += 1
                    else:
                        posicao_atual = proxima_posicao
                        montar_caminho(posicao_anterior, posicao_atual, janela, transformado)

                    posicao_anterior = posicao_atual

            if retorno_inicial and posicao_atual == inicio:
                rodando = False
                reproduz_video(".\\mapas\\summon.mp4")
                


        pygame.time.delay(100)  # Delay para não sobrecarregar a CPU
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
