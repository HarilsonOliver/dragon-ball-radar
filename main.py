import pygame
import random
import traduz_terreno
import transforma_terreno
import desenha_terreno
from config import *
from terreno import gera_destinos_dinamicos, carrega_terreno
from algoritmo import algoritmo_estrela
from desenha import montar_caminho, desenha_radar, desenha_esferas
from moviepy.editor import VideoFileClip


def reproduz_video(caminho_video):
    clip = VideoFileClip(caminho_video)
    clip.preview()

def main():
    pygame.init()
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Dragon Ball Radar")

    # Carregar efeitos sonoros
    pygame.mixer.music.load('./mapas/soundtrack.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.init()
    searching = pygame.mixer.Sound('./mapas/searching.mp3')
    found = pygame.mixer.Sound('./mapas/found.mp3')
    flying = pygame.mixer.Sound('./mapas/flying.mp3')

    searching_channel = searching.play(loops=-1)
    flying_channel = flying.play(loops=-1)

    transformado = carrega_terreno(traduz_terreno, transforma_terreno, variavel)
    destinos_dinamicos = gera_destinos_dinamicos()
    partida = inicio

    desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)
    desenha_esferas(janela, destinos_dinamicos, TAMANHO)
    
    # Desenha o radar desde o início
    desenha_radar(janela, partida, TAMANHO, destinos_dinamicos)
    pygame.display.update()

    rodando = True
    agente_movendo = True
    caminhos = []
    custos = []
    custo_total_acumulado = 0
    esferas_coletadas = 0
    posicao_anterior = None
    retorno_inicial = False

    # Posição inicial do agente
    posicao_atual = partida
    direcao = (0, 1)  # Começa movendo para a direita

    # Passo inicial: mover até a primeira célula (0,0) usando A*
    caminho_inicial, custos_iniciais = algoritmo_estrela(transformado, partida, (0, 0))
    caminhos.extend(caminho_inicial)
    custos.extend(custos_iniciais)

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if agente_movendo:
            if caminhos:
                proximo_passo = caminhos.pop(0)
                custo_do_passo = custos.pop(0) if custos else 0
                custo_total_acumulado += custo_do_passo
                print(f'Movimento para {proximo_passo} com custo {custo_do_passo}. Custo total acumulado: {custo_total_acumulado}')
                montar_caminho(posicao_anterior, proximo_passo, janela, transformado)
                
                # Desenhar o radar na posição atual do agente
                esferas_no_radar = desenha_radar(janela, proximo_passo, TAMANHO, destinos_dinamicos)
                
                # Verificar se a posição atual é uma posição de esfera
                if proximo_passo in destinos_dinamicos:
                    destinos_dinamicos.remove(proximo_passo)
                    found_channel = found.play()
                    esferas_coletadas += 1
                    found_channel.stop()
                    print(f'Esfera coletada na posição {proximo_passo}')
                            
                posicao_anterior = proximo_passo
                posicao_atual = proximo_passo
            else:
                if esferas_coletadas == 7 and not retorno_inicial:
                    retorno_inicial = True
                    searching_channel.stop()
                    
                elif retorno_inicial:
                    caminho_de_volta, custos_de_volta = algoritmo_estrela(transformado, posicao_atual, inicio)
                    if caminho_de_volta:
                        caminhos.extend(caminho_de_volta)
                        custos.extend(custos_de_volta)
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
                            caminho_para_esfera, custos_para_esfera = algoritmo_estrela(transformado, posicao_atual, esfera)
                            caminhos.extend(caminho_para_esfera)
                            custos.extend(custos_para_esfera)
                            print(f'Custo para coletar a esfera na posição {esfera}: {sum(custos_para_esfera)}')
                    else:
                        posicao_atual = proxima_posicao
                        montar_caminho(posicao_anterior, posicao_atual, janela, transformado)

                    posicao_anterior = posicao_atual

            # Redesenhar o terreno e as esferas a cada movimento
            janela.fill((0, 0, 0))  # Limpar a tela
            desenha_terreno.desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela)
            desenha_esferas(janela, destinos_dinamicos, TAMANHO)
            montar_caminho(None, posicao_atual, janela, transformado)
            
            # Desenhar o radar na posição atual do agente
            desenha_radar(janela, posicao_atual, TAMANHO, destinos_dinamicos)

            if retorno_inicial and posicao_atual == inicio:
                rodando = False
                flying_channel.stop()
                
                reproduz_video(".\\mapas\\shenlong1.mov")
                
                # Imprimir o custo total ao final
                print(f'CUSTO TOTAL: {custo_total_acumulado}')

        pygame.time.delay(1)  # Delay para não sobrecarregar a CPU
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
