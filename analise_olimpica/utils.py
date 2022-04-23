import pandas as pd

# Pandas

def get_columns(df, columns_guess):
    col = {column:column for column in columns_guess}
    for column in col:
        if column not in df.columns:
            print(df.columns)
            col[column] = input(f'Qual o nome certo da coluna {column}?')
    return(col)


# User input

def get_dataframe(filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(filename)
    else:
        raise TypeError("Apenas planilhas em .csv ou .xlsx (Excel) são permitidas")
    return df

def ask_new_adm_for_school(school_name):
    print('A seguinte escola não possui valor em Administração (1=pública ou 2=privada). Digite o novo valor.')
    school_adm = input(f'{school_name}: ')
    while not (school_adm in {'pública', 'privada', '1', '2'}):
        print('Deve ser "pública" (1) ou "privada" (2)')
        school_adm = input(f'{school_name}: ')

    if school_adm == '1': school_adm = 'pública'
    if school_adm == '2': school_adm = 'privada'

    return school_adm

# Formatting data

def amount_of_per_participant_qnt(results_dict, name, series, range_span):
    
    tmp_sum = 0
    for _range in range_span:
        qnt = 0
        for i in _range:
            if i in series:
                qnt += series[i]

        start, end = _range[0], _range[-1]
        if start == end:
            results_dict[f'{name} com {start} inscrito{"s" if end != 1 else ""}'] = qnt
        else:
            results_dict[f'{name} com {start}-{end} inscrito{"s" if end != 1 else ""}'] = qnt

        tmp_sum += qnt

    results_dict[f'{name} com mais de {range_span[-1][-1]} inscritos'] = series.sum() - tmp_sum

# Math

def str_porcentagem(a,b):
    return(f'({100*a/b:.0f}%)')