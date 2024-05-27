tipo_terreno = {
    "v": "GRAMA",
    "t": "MONTANHA",
    "a": "AGUA",
    "r": "KAMI",
    "p": "PAREDE",
    "c": "CAMINHO"
}

terreno = []

with open("./mapas/terreno.txt", "r") as arquivo:
    mapa = arquivo.readlines()
    for linha in mapa:
        temp = []
        for caractere in linha:
            if caractere != '\n':
                temp.append(tipo_terreno[caractere])
        terreno.append(temp)

def retorna_terreno():
    return terreno

