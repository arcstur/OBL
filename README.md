# OBL
Scripts da OBL

## Análise de Dados

- Pegue os arquivos .xlsx entregues pela Fractal
- Converta em .csv (pode utilizar o script `converter.py`)
- Rode `analise.py`

Por enquanto é necessário ter Python instalado, e lembre-se de instalar as dependências necessárias com `pip install`.

### Exemplo: OBL Edição Mascate

    Para fazer a análise dos participantes, as seguintes colunas serão necessárias:
    Categoria (Regular e Aberta)
    Sexo (Masculino, Feminino)
    Nome da Escola
    Administração da escola (pública ou privada)
    UF
    Cidade
    Por padrão, vamos utilizar duas tabelas. A de "classificação" contém as notas, e quase todas colunas acima, mas NÃO contém a coluna Administração por padrão. Logo, vamos precisar da tabela de "inscritos", que contém a coluna de Administração.

    Diga o número de provas/edições que queres analisar: 2

    PROVA  1
    Digite o nome da prova: PROVA REGULAR E ABERTA
    Digite o nome da planilha de classificação, COM a extensão ".csv": mascate-regular-e-aberta_2021_fase-1_classificacao.csv
    Digite o nome da planilha de inscritos, COM a extensão ".csv": mascate-regular-e-aberta_inscritos_atualizado.csv

    PROVA  2
    Digite o nome da prova: PROVA MIRIM
    Digite o nome da planilha de classificação, COM a extensão ".csv": mascate-mirim_2021_fase-1_classificacao.csv
    Digite o nome da planilha de inscritos, COM a extensão ".csv": mascate-mirim_inscritos_atualizado.csv

    PROVA REGULAR E ABERTA
    Total de 3300 participantes

    # Categoria Aberta
        Total: 387

    # Categoria Regular
        Total: 2913

        De escola pública: 806 (28%)
        De escola privada: 2107

        Feminino: 1734 (60%)
        Masculino: 1168

        Total de 822 escolas
        escolas públicas: 363 (44%)
        escolas privadas: 459
        Total de 325 cidades
        Total de 27 estados
        SP: 975
        RJ: 342
        SC: 269
        CE: 228
        MG: 220
        MA: 166
        PR: 96
        PE: 91
        BA: 86
        RS: 47
        PI: 44
        DF: 43
        ES: 42
        AM: 42
        RN: 38
        GO: 34
        MS: 29
        SE: 26
        PB: 26
        PA: 19
        AL: 18
        MT: 10
        TO: 8
        AP: 5
        RO: 4
        RR: 3
        AC: 2


    PROVA MIRIM
    Total de 752 participantes

    # Categoria Aberta
        Total: 0

    # Categoria Regular
        Total: 752

        De escola pública: 183 (24%)
        De escola privada: 569

        Feminino: 461 (61%)
        Masculino: 291

        Total de 244 escolas
        escolas públicas: 91 (37%)
        escolas privadas: 153
        Total de 127 cidades
        Total de 27 estados
        SP: 254
        CE: 101
        MG: 70
        RJ: 66
        PE: 65
        SC: 41
        MA: 26
        AM: 22
        PI: 18
        RN: 17
        DF: 10
        ES: 9
        PR: 8
        SE: 7
        PB: 7
        BA: 7
        AL: 4
        PA: 3
        MS: 3
        RS: 3
        MT: 3
        TO: 2
        RO: 2
        AP: 1
        RR: 1
        AC: 1
        GO: 1