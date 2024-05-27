def transforma_terreno(terreno, converte_variavel):
    terreno_transformado = []
    for linha in terreno:
        linha_convertida = []
        for item in linha:
            linha_convertida.append(converte_variavel[item])
        terreno_transformado.append(linha_convertida)
    return terreno_transformado