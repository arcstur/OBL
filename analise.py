import csv
from collections import Counter

def str_porcentagem(a,b):
    return('(' + str(int(100*round(a/b,2))) + '%)')

def intro():
    print('Para fazer a análise dos participantes, as seguintes colunas serão necessárias:')
    print('  Categoria (Regular e Aberta)')
    print('  Sexo (Masculino, Feminino)')
    print('  Nome da Escola')
    print('  Administração da escola (pública ou privada)')
    print('  UF')
    print('  Cidade')
    print('Por padrão, vamos utilizar duas tabelas. A de "classificação" contém as notas, e quase todas colunas acima, mas NÃO contém a coluna Administração por padrão. Logo, vamos precisar da tabela de "inscritos", que contém a coluna de Administração.')
    print()

class Prova():
    def __init__(self, nome, tabela_classificacao='', tabela_inscritos=''):
        self.nome = nome
        self.tabela_classificacao = ''
        self.tabela_inscritos = ''
        self.count_total = 0
        self.count_regular = 0
        self.count_aberta = 0
        self.count_reg_publica = 0
        self.count_reg_privada = 0
        self.count_masc = 0
        self.count_fem = 0
        self.set_escola = set()
        self.count_escola_publica = 0
        self.count_escola_privada = 0
        self.lista_UF = list()
        self.set_cidade = set()
        self.dic_escolas = dict() #Faz um dicionário escola/administração com a planilha de inscritos

        if tabela_classificacao == '':
            self.tabela_classificacao = input('Digite o nome da planilha de classificação, COM a extensão ".csv": ')
        else:
            self.tabela_classificacao = tabela_classificacao
            
        if tabela_inscritos == '':
            self.tabela_inscritos = input('Digite o nome da planilha de inscritos, COM a extensão ".csv": ')
        else:
            self.tabela_inscritos = tabela_inscritos

    def criar_dicionario_escolas(self):
        with open(self.tabela_inscritos, 'r') as f:
            reader = csv.reader(f)

            headers = next(reader)

            index_escola = headers.index('Escola')
            index_adm = headers.index('Administração')

            for line in reader:
                self.dic_escolas[line[index_escola]] = line[index_adm]
                
        ok = True
        for nome,adm in self.dic_escolas.items():
            if adm=='' and nome!='':
                ok = False
                print('A seguinte escola não possui valor em Administração (pública ou privada). Digite o novo valor.')
                nova_adm = input(nome + ': ')
                while not (nova_adm in {'pública', 'privada'}):
                    print('Deve ser "pública" ou "privada"')
                    nova_adm = input(nome + ': ')

                self.dic_escolas[nome] = nova_adm

        if not ok:
            print()
            resposta = input('Gostaria de salvar estes novos valores na planilha? [S/n] ')
            if resposta != 'n':
                with open(self.tabela_inscritos.replace('.csv','') + '_atualizado.csv', 'w') as fw, open(self.tabela_inscritos, 'r') as fr:
                    reader = csv.reader(fr)
                    writer = csv.writer(fw)

                    for line in reader:
                        if line[index_adm]=='':
                            line[index_adm] = self.dic_escolas[line[index_escola]]
                        writer.writerow(line)

                print()
                print('Os valores atualizados foram salvos na planilha')
                print(self.tabela_inscritos.replace('.csv','') + '_atualizado.csv')
                print()

    def é_pública(self, nome):
        return (self.dic_escolas[nome].lower() in {'state', 'federal', 'municipal', 'pública'})

    def é_privada(self, nome):
        return (self.dic_escolas[nome].lower() in {'privada', 'particular'})


    def analise(self):
        if len(self.dic_escolas) <= 1:
            self.criar_dicionario_escolas()

        with open(self.tabela_classificacao, 'r') as f:
            reader = csv.reader(f)

            headers = next(reader)
            index_categoria, index_sexo = headers.index('Categoria'), headers.index('Sexo')
            index_escola = headers.index('Escola')
            index_UF, index_cidade = headers.index('UF'), headers.index('Cidade')

            #Ler cada linha e trabalhar
            for line in reader:
                self.count_total += 1

                if line[index_categoria]=='Aberta': self.count_aberta += 1
                elif line[index_categoria]=='Regular':
                    self.count_regular += 1
                    if self.é_pública(line[index_escola]): self.count_reg_publica += 1
                    elif self.é_privada(line[index_escola]): self.count_reg_privada += 1

                    if line[index_sexo] in {'Feminino', 'F'}: self.count_fem += 1
                    elif line[index_sexo] in {'Masculino', 'M'}: self.count_masc += 1

                    self.lista_UF.append(line[index_UF])
                    self.set_cidade.add(line[index_cidade])
                    self.set_escola.add(line[index_escola])
            
        self.set_UF = set(self.lista_UF)
        self.counter_UF = Counter(self.lista_UF)

        #Cálculo escolas públicas/privadas
        for nome in self.set_escola:
            if self.é_privada(nome): self.count_escola_privada += 1
            elif self.é_pública(nome): self.count_escola_publica += 1

    def print_resultados(self):
        print()
        print(self.nome)
        print('Total de',str(self.count_regular + self.count_aberta),'participantes')
        print()
        print('# Categoria Aberta')
        print('    Total:', str(self.count_aberta))
        print()
        print('# Categoria Regular')
        print('    Total:', str(self.count_regular))
        print()
        print('    De escola pública:', str(self.count_reg_publica), str_porcentagem(self.count_reg_publica, self.count_regular))
        print('    De escola privada:', str(self.count_reg_privada))
        print()
        print('    Feminino:', str(self.count_fem), str_porcentagem(self.count_fem,self.count_regular))
        print('    Masculino:', str(self.count_masc))
        print()

        print('    Total de', str(len(self.set_escola)), 'escolas')
        print('      escolas públicas:', str(self.count_escola_publica), str_porcentagem(self.count_escola_publica, len(self.set_escola)))
        print('      escolas privadas:', str(self.count_escola_privada))

        # print(set_cidade)
        print('    Total de', str(len(self.set_cidade)), 'cidades')

        # print(set_UF)
        print('    Total de', str(len(self.set_UF)), 'estados')
        for dupla in self.counter_UF.most_common():
            print('      ' + dupla[0] + ':', dupla[1])
        print()



def main():
    intro()

    # lista_provas = list()
    # n = int(input('Diga o número de provas/edições que queres analisar: '))

    # for i in range(n):
    #     print()
    #     print('PROVA ', str(i+1))
    #     nome = input('Digite o nome da prova: ')
    #     lista_provas.append(Prova(nome, '', ''))

    # for prova in lista_provas:
    #     prova.analise()
    #     prova.print_resultados()


    regab = Prova('PROVA REGULAR E ABERTA', 'a.csv', 'b.csv')
    regab.analise()
    regab.print_resultados()

    mirim = Prova('PROVA MIRIM', 'mascate-mirim_2021_fase-1_classificacao.csv', 'mascate-mirim_inscritos_atualizado.csv')
    mirim.analise()
    mirim.print_resultados()

if __name__ == '__main__':
    main()