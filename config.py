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

# Dimensões da tela
LARGURA = 800
ALTURA = 800
TAMANHO = 17

# Dimensões da matriz do terreno
LINHA = 42
COLUNA = 42

# Coordenadas do inicio e chegada
inicio = (19, 17)
chegada = (7, 8)
