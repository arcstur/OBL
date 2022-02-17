import csv
from collections import Counter

def str_porcentagem(a,b):
    return('(' + str(int(100*round(a/b,2))) + '%)')



print('Para fazer a análise dos participantes, as seguintes colunas serão necessárias:')
print('  Categoria (Regular e Aberta)')
print('  Sexo (Masculino, Feminino)')
print('  Nome da Escola')
print('  Administração da escola (pública ou privada)')
print('  UF')
print('  Cidade')
print('Por padrão, vamos utilizar duas tabelas. A de "classificação" contém as notas, e quase todas colunas acima, mas NÃO contém a coluna Administração por padrão. Logo, vamos precisar da tabela de "inscritos", que contém a coluna de Administração.')
print()

# tabela_classificacao = input('Digite o nome da planilha de classificação, COM a extensão '.csv': ')
tabela_classificacao = 'mascate-regular-e-aberta_2021_fase-1_classificacao.csv'
# tabela_inscritos = input('Digite o nome da planilha de inscritos, COM a extensão '.csv': ')
tabela_inscritos = 'mascate-regular-e-aberta_inscritos_atualizado.csv'

count_total= 0
count_regular, count_aberta = 0,0
count_reg_publica, count_reg_privada = 0,0
count_masc, count_fem = 0,0
set_escola = set()
count_escola_publica, count_escola_privada = 0,0
lista_UF = []
set_cidade = set()

#Faz um dicionário escola/administração com a planilha de inscritos
dic_escolas={'':''}



with open(tabela_inscritos, 'r') as f:
    reader = csv.reader(f)

    headers = next(reader)
    print(headers)

    index_escola = headers.index('Escola')
    index_adm = headers.index('Administração')

    for line in reader:
        dic_escolas[line[index_escola]] = line[index_adm]
        
ok = True
for nome,adm in dic_escolas.items():
    if adm=='' and nome!='':
        ok = False
        print('A seguinte escola não possui valor em Administração (pública ou privada). Digite o novo valor.')
        nova_adm = input(nome + ': ')
        while not (nova_adm in {'pública', 'privada'}):
            print('Deve ser "pública" ou "privada"')
            nova_adm = input(nome + ': ')

        dic_escolas[nome] = nova_adm
print()
if not ok:
    resposta = input('Gostaria de salvar estes novos valores na planilha? [S/n] ')
    if resposta != 'n':
        with open(tabela_inscritos.replace('.csv','') + '_atualizado.csv', 'w') as fw, open(tabela_inscritos, 'r') as fr:
            reader = csv.reader(fr)
            writer = csv.writer(fw)

            for line in reader:
                if line[index_adm]=='':
                    line[index_adm] = dic_escolas[line[index_escola]]
                writer.writerow(line)

        print()
        print('Os valores atualizados foram salvos na planilha')
        print(tabela_inscritos.replace('.csv','') + '_atualizado.csv')
        print()

def é_publica(nome):
    return (dic_escolas[nome].lower() in {'state', 'federal', 'municipal', 'pública'})

def é_privada(nome):
    return (dic_escolas[nome].lower() in {'privada', 'particular'})

with open(tabela_classificacao, 'r') as f:
    reader = csv.reader(f)

    headers = next(reader)
    index_categoria, index_sexo = headers.index('Categoria'), headers.index('Sexo')
    index_escola = headers.index('Escola')
    index_UF, index_cidade = headers.index('UF'), headers.index('Cidade')

    #Ler cada linha e trabalhar
    for line in reader:
        count_total += 1

        if line[index_categoria]=='Aberta': count_aberta += 1
        elif line[index_categoria]=='Regular':
            count_regular += 1
            if é_publica(line[index_escola]): count_reg_publica += 1
            elif é_privada(line[index_escola]): count_reg_privada += 1

        if line[index_sexo] in {'Masculino', 'M'}: count_masc += 1
        elif line[index_sexo] in {'Feminino', 'F'}: count_fem += 1

        if line[index_categoria]=='Regular':
            lista_UF.append(line[index_UF])
            set_cidade.add(line[index_cidade])
            set_escola.add(line[index_escola])
    
set_UF = set(lista_UF)
counter_UF = Counter(lista_UF)

#Remover valores inválidos
for x in ['', 'Não identificado']:
    if x in set_UF: set_UF.remove(x)
    if x in set_cidade: set_cidade.remove(x)
    if x in set_escola: set_escola.remove(x)

#Cálculo escolas públicas/privadas
for nome in set_escola:
    if é_privada(nome): count_escola_privada += 1
    elif é_publica(nome): count_escola_publica += 1

print('Total de',str(count_regular + count_aberta),'participantes')
print('    Aberta:', str(count_aberta))
print('    Regular:', str(count_regular))
print('        de escola pública:', str(count_reg_publica), str_porcentagem(count_reg_publica, count_regular))
print('        de escola privada:', str(count_reg_privada))
print()
print('    Masculino:', str(count_masc))
print('    Feminino:', str(count_fem), str_porcentagem(count_fem,count_total))
print('    Outro:', str(count_total - count_masc - count_fem))
print()

print('# Categoria Regular')

# print(set_UF)
print('Total de', str(len(set_UF)), 'estados')

# print(set_cidade)
print('Total de', str(len(set_cidade)), 'cidades')

# print(set_escola)
print('Total de', str(len(set_escola)), 'escolas')
print('    escolas públicas:', str(count_escola_publica), str_porcentagem(count_escola_publica, len(set_escola)))
print('    escolas privadas:', str(count_escola_privada))

print('Participantes por estado:')
for dupla in counter_UF.most_common(len(counter_UF)):
    print(dupla[0] + ':', dupla[1])

