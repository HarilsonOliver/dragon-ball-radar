import pygame

def desenha_terreno(transformado, LINHA, COLUNA, AGUA, GRAMA, MONTANHA, KAMI, CAMINHO, PAREDE, TAMANHO, janela):

  for linha in range(LINHA):
    for coluna in range(COLUNA):
      #Cor do espaço com base no seu valor de custo
        if transformado[linha][coluna] == AGUA:
          cor = (45,72,181)
        elif transformado[linha][coluna] == GRAMA:
          cor = (140,211,70)
        elif transformado[linha][coluna] == MONTANHA:
          cor = (82,70,44)
        elif transformado[linha][coluna] == KAMI:
          cor = (255,0,0)
        elif transformado[linha][coluna] == CAMINHO:
          cor = (201, 176, 10)
        elif transformado[linha][coluna] == PAREDE:
          cor = (255, 255, 255)
        
        pygame.draw.rect(janela, cor, (coluna * TAMANHO, linha * TAMANHO, TAMANHO-1, TAMANHO-1))