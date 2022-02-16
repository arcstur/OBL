import csv
import pandas as pd

print("Para fazer a análise dos participantes, as seguintes colunas serão necessárias:")
print("  Categoria (Regular e Aberta)")
print("  Sexo (Masculino, Feminino, -)")
print("  Nome da Escola")
print("  Administração da escola (pública - pode ser municipal, estadual, ... - ou privada)")
print("  UF")
print("  Cidade")
print("Por padrão, vamos utilizar duas tabelas. A de 'classificação' contém as notas, e quase todas colunas acima, mas NÃO contém a coluna Administração por padrão. Logo, vamos precisar da tabela de 'inscritos', que contém a coluna de Administração.")
print()

# tabela_classificacao = input("Digite o nome da planilha de classificação, COM a extensão '.csv': ")
tabela_classificacao = "mascate-regular-e-aberta_2021_fase-1_classificacao.csv"
# tabela_inscritos = input("Digite o nome da planilha de inscritos, COM a extensão '.csv': ")

with open(tabela_classificacao, 'r') as fc:
    reader = csv.reader(fc)

    headers = next(reader)

    index_categoria, index_sexo = headers.index('Categoria'), headers.index('Sexo')
    index_escola = headers.index('Escola')
    index_UF, index_cidade = headers.index('UF'), headers.index('Cidade')

    count_total=0
    count_regular, count_aberta = 0,0
    count_masc, count_fem = 0,0
    set_escola = set()
    set_UF = set()
    set_cidade = set()

    #Ler cada linha e trabalhar
    for line in reader:
        count_total += 1

        if line[index_categoria]=="Aberta": count_aberta += 1
        elif line[index_categoria]=="Regular": count_regular += 1

        var_sexo = line[index_sexo]
        if var_sexo in {"Masculino", "M"}: count_masc += 1
        elif var_sexo in {"Feminino", "F"}: count_fem += 1

        set_UF.add(line[index_UF])
        set_cidade.add(line[index_cidade])
        set_escola.add(line[index_escola])
    
    #Remover valores inválidos
    for x in ["", "Não identificado"]:
        if x in set_UF: set_UF.remove(x)
        if x in set_cidade: set_cidade.remove(x)
        if x in set_escola: set_escola.remove(x)

    print("Total de",str(count_regular + count_aberta),"participantes")
    print("    Regular:", str(count_regular))
    print("    Aberta:", str(count_aberta))
    print()
    print("    Masculino:", str(count_masc))
    print('    Feminino:', str(count_fem))
    print('    Outro:', str(count_total - count_masc - count_fem))
    print()

    # print(set_UF)
    print("Total de", str(len(set_UF)), "estados")

    # print(set_cidade)
    print("Total de", str(len(set_cidade)), "cidades")

    # print(set_escola)
    print("Total de", str(len(set_escola)), "escolas")
