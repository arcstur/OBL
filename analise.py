import pandas as pd
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
        self.dic_escolas = dict() #Faz um dicionário escola/administração com a planilha de inscritos

        if tabela_classificacao == '':
            self.tabela_classificacao = input('Digite o nome da planilha de classificação, COM a extensão ".csv": ')
        else:
            self.tabela_classificacao = tabela_classificacao
            
        if tabela_inscritos == '':
            self.tabela_inscritos = input('Digite o nome da planilha de inscritos, COM a extensão ".csv": ')
        else:
            self.tabela_inscritos = tabela_inscritos

    def receber_nome_da_coluna(self, dataframe, tentativa):
        if tentativa not in dataframe.columns:
            print(dataframe.columns)
            nome_certo_da_coluna = input('Qual o nome certo da coluna ' + tentativa + '?')
            return(nome_certo_da_coluna)
        else:
            return(tentativa)

    def criar_dicionario_escolas(self):
        df = pd.read_csv(self.tabela_inscritos)

        col = {}
        for id_coluna in ('Categoria', 'Escola', 'Administração'):
            col[id_coluna] = self.receber_nome_da_coluna(df, id_coluna)

        ok = True
        for row in df.itertuples():
            row = row._asdict()
            if row[col['Categoria']] == 'Regular':
                nome, adm = row[col['Escola']], row[col['Administração']]

                # Além de criar o dicionário, a função ajusta os valores errados no dataframe
                # Se a escola não possui administração no dataframe,
                if pd.isnull(adm) or adm=='':
                    # Se a escola já possui valor no dicionário, utilizar este valor
                    if nome in self.dic_escolas.keys():
                        adm = self.dic_escolas[nome]
                    # Se não possui, pedir um valor novo para o usuário
                    else:
                        ok = False
                        print('A seguinte escola não possui valor em Administração (1=pública ou 2=privada). Digite o novo valor.')
                        adm = input(nome + ': ')
                        while not (adm in {'pública', 'privada', '1', '2'}):
                            print('Deve ser "pública" (1) ou "privada" (2)')
                            adm = input(nome + ': ')
                    
                        if adm == '1': adm = 'pública'
                        if adm == '2': adm = 'privada'
                    # Salvar o valor atualizado no dataframe
                    df.loc[row['Index'],col['Administração']] = adm
                
                # Se já não está no dicionário, salvar
                if nome not in self.dic_escolas.keys():
                    self.dic_escolas[row[col['Escola']]] = adm

        if not ok:
            tabela_inscritos_nova = self.tabela_inscritos.replace('.csv','') + '_atualizado.csv'
            df.to_csv(tabela_inscritos_nova)
            print()
            print('Os valores atualizados foram salvos na planilha ' + tabela_inscritos_nova)
            input('Pressione Enter para continuar.')

    def é_pública(self, nome):
        return (self.dic_escolas[nome].lower() in {'state', 'federal', 'municipal', 'pública'})

    def é_privada(self, nome):
        return (self.dic_escolas[nome].lower() in {'privada', 'particular'})


    def analisar(self):
        self.criar_dicionario_escolas()

        df = pd.read_csv(self.tabela_classificacao)

        col = {}
        for id_coluna in ('Categoria', 'Sexo', 'Escola', 'UF', 'Cidade'):
            col[id_coluna] = self.receber_nome_da_coluna(df, id_coluna)
        
        self.count_total = len(df)

        self.counts_cat = df[col['Categoria']].value_counts()
        self.count_regular = self.counts_cat['Regular']
        try: self.count_aberta = self.counts_cat['Aberta']
        except: self.count_aberta = 0 

        # Ficando com apenas os da categoria regular
        df = df.loc[ df['Categoria'] == 'Regular' ]

        self.counts_sexo = df[col['Sexo']].value_counts()
        self.set_escola = set(df[col['Escola']])
        self.set_cidade = set(df[col['Cidade']])
        self.set_UF = set(df[col['UF']])
        self.counts_UF = df[col['UF']].value_counts()

        #Cálculo participantes de escolas públicas/privadas
        self.count_reg_publica, self.count_reg_privada = 0,0
        for nome in df[col['Escola']]:
            if self.é_pública(nome): self.count_reg_publica += 1
            elif self.é_privada(nome): self.count_reg_privada += 1

        #Cálculo escolas públicas/privadas
        self.count_escola_publica, self.count_escola_privada = 0,0
        for nome in self.set_escola:
            if self.é_privada(nome): self.count_escola_privada += 1
            elif self.é_pública(nome): self.count_escola_publica += 1

    def print_resultados(self):
        print()
        print(self.nome)
        print('Total de',str(self.count_total),'participantes')
        print()
        print('# Categoria Aberta')
        print('    Total:', str(self.count_aberta))
        print()
        print('# Categoria Regular')
        print('    Total:', str(self.count_regular))
        print()
        print('    De escola pública:', str(self.count_reg_publica), str_porcentagem(self.count_reg_publica, self.count_regular))
        print('    De escola privada:', str(self.count_reg_privada), str_porcentagem(self.count_reg_privada, self.count_regular))
        print()
        for sexo, qnt in self.counts_sexo.iteritems():
            print('    ' + sexo + ':', str(qnt), str_porcentagem(qnt, self.count_regular))
        print()

        # print(set_escola)
        print('    Total de', str(len(self.set_escola)), 'escolas')
        print('      escolas públicas:', str(self.count_escola_publica), str_porcentagem(self.count_escola_publica, len(self.set_escola)))
        print('      escolas privadas:', str(self.count_escola_privada), str_porcentagem(self.count_escola_privada, len(self.set_escola)))

        # print(set_cidade)
        print('    Total de', str(len(self.set_cidade)), 'cidades')

        # print(set_UF)
        print('    Total de', str(len(self.set_UF)), 'estados')
        for estado,qnt in self.counts_UF.iteritems():
            print('      ' + estado + ':', qnt)
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
    #     prova.analisar()
    #     prova.print_resultados()


    regab = Prova('PROVA REGULAR E ABERTA', 'mascate-regular-e-aberta_2021_fase-1_classificacao.csv', 'mascate-regular-e-aberta_inscritos_atualizado.csv')
    regab.analisar()
    regab.print_resultados()

    mirim = Prova('PROVA MIRIM', 'mascate-mirim_2021_fase-1_classificacao.csv', 'mascate-mirim_inscritos_atualizado.csv')
    mirim.analisar()
    mirim.print_resultados()

def profiling():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
    # snakeviz profiling.prof

if __name__ == '__main__':
    main()