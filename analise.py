import csv

print("Para fazer a análise dos participantes, as seguintes colunas serão necessárias:")
print("  Categoria (Regular e Aberta)")
print("  Sexo (Masculino, Feminino, -)")
print("  Nome da Escola")
print("  Administração da escola (pública - pode ser municipal, estadual, ... - ou privada)")
print("  UF")
print("  Cidade")
print("Por padrão, vamos utilizar duas tabelas. A de 'classificação' contém as notas, e quase todas colunas acima, mas NÃO contém a coluna Administração por padrão. Logo, vamos precisar da tabela de 'inscritos', que contém a coluna de Administração.")
print()

tabela_classificacao = input("Digite o nome da planilha de classificação, COM a extensão '.csv': ")
tabela_inscritos = input("Digite o nome da planilha de inscritos, COM a extensão '.csv': ")
print()


    


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