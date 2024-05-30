import pygame

# Inicialização do Pygame
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

# Coordenadas do início, destinos, chegada
inicio = (19, 19)
esfera = (2, 3)
chegada = (7, 8)

# Cores de cada tipo de terreno (mantidas para referência ou outros usos)
AGUA = (30, 144, 255)
GRAMA = (124, 252, 0)
MONTANHA = (139, 137, 137)
CAMINHO = (224, 224, 224)
PAREDE = (139, 137, 137)
KAMI = (255, 0, 0)
cor_radar = (255, 255, 255, 20)

# Dicionário de cores
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

# Carregar imagens de cada tipo de terreno
IMAGENS = {
    "AGUA": pygame.image.load('./mapas/agua1.png'),
    "GRAMA": pygame.image.load('./mapas/grama1.png'),
    "MONTANHA": pygame.image.load('./mapas/terra.jpg'),
    "KAMI": pygame.image.load('./mapas/kamee.png'),
}

# Redimensionar imagens para o tamanho da célula
for key in IMAGENS:
    IMAGENS[key] = pygame.transform.scale(IMAGENS[key], (TAMANHO, TAMANHO))
