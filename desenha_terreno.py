import pygame
from config import COLUNA, LINHA, TAMANHO, IMAGENS

def desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela):
    for linha in range(LINHA):
        for coluna in range(COLUNA):
            tipo_terreno = transformado[linha][coluna]
            imagem = None
            if tipo_terreno == (30, 144, 255):  # AGUA
                imagem = IMAGENS["AGUA"]
            elif tipo_terreno == (124, 252, 0):  # GRAMA
                imagem = IMAGENS["GRAMA"]
            elif tipo_terreno == (139, 137, 137):  # MONTANHA
                imagem = IMAGENS["MONTANHA"]
            elif tipo_terreno == (255, 0, 0):  # KAMI
                imagem = IMAGENS["KAMI"]
            elif transformado[linha][coluna] == CAMINHO:
              cor = (201, 176, 10)
            elif transformado[linha][coluna] == PAREDE:
              cor = (255, 255, 255)
            
            if imagem:
                janela.blit(imagem, (coluna * TAMANHO, linha * TAMANHO))
