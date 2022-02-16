import csv

print("Para fazer a análise dos participantes, as seguintes colunas serão necessárias:")
print("  Categoria (Regular e Aberta)")
print("  Sexo (Masculino, Feminino, -)")
print("  Nome da Escola")
print("  Administração da escola (pública - pode ser municipal, estadual também - ou privada)")
print("  UF")
print("  Cidade")

resposta = input("Caso seu .csv tenha todas as colunas acima, digite 's'. Caso tenha um arquivo separado com a Administração da escola (padrão), aperte Enter:\n")


if resposta=="s":
    arquivo = input("Digite o nome do csv que contém todas as colunas necessárias:\n")
    if not arquivo.endswith('.csv'):
        arquivo += ".csv"
    print("Vamos abrir o arquivo " + arquivo)

    


# with open('mascate-regular-e-aberta_2021_fase-1_classificacao.csv', 'r') as f:
#     reader = csv.reader(f)

#     headers = next(reader)

#     ColNota = headers.index('Nota')
#     ColCategoria = headers.index('Categoria')

#     print(headers)

#     count_total = 0

#     for line in reader:
#         count_total += 1

#     print(count_total)