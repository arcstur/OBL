import pandas as pd

from .exceptions import NonExistantColumn

# Pandas


def get_columns(df, columns_guess):
    col = {column: column for column in columns_guess}
    for column in col:
        if column not in df.columns:
            print(df.columns)
            value = input(f"Qual o nome certo da coluna {column}? (coloque 'N.A.' caso não exista) ")
            if value != "N.A.":
                col[column] = value
            else:
                raise NonExistantColumn()
    return col


def amount_of_per_participant_qnt(
    results_dict,
    series,
    range_span,
    quantity_name="",
    property_name_tuple=("inscrito", "inscritos"),
):
    tmp_sum = 0
    for i in range(len(range_span) - 1):
        qnt = 0
        start = range_span[i]
        end = range_span[i + 1] - 1

        for n in range(start, end + 1):
            if n in series:
                qnt += series[n]

        if start == end:
            results_dict[
                f"{quantity_name} com {start} {property_name_tuple[1 if end != 1 else 0]}"
            ] = qnt
        else:
            results_dict[
                f"{quantity_name} com {start}-{end} {property_name_tuple[1 if end != 1 else 0]}"
            ] = qnt

        tmp_sum += qnt

    results_dict[f"{quantity_name} com mais de {end} {property_name_tuple[1]}"] = (
        series.sum() - tmp_sum
    )

    return results_dict


# User input


def get_dataframe(filename):
    if filename.endswith(".csv"):
        df = pd.read_csv(filename)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(filename)
    else:
        raise TypeError("Apenas planilhas em .csv ou .xlsx (Excel) são permitidas")
    return df


def ask_new_adm_for_school(school_name):
    print(
        "A seguinte escola não possui valor em Administração (1=pública ou 2=privada). Digite o novo valor."
    )
    school_adm = input(f"{school_name}: ")
    while not (school_adm in {"pública", "privada", "1", "2"}):
        print('Deve ser "pública" (1) ou "privada" (2)')
        school_adm = input(f"{school_name}: ")

    if school_adm == "1":
        school_adm = "pública"
    if school_adm == "2":
        school_adm = "privada"

    return school_adm


# Math


def str_percentage(a, b):
    return f"{100*a/b:.0f}%"
