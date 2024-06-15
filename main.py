import pandas as pd
from analise_olimpica import objects, multiple

def main():
    df = pd.read_csv('Tabela_Escolas.csv', delimiter=';')
    school_dict_object = objects.SchoolDict.from_dataframe(df)

    main_df = pd.read_excel('20220105_GERAL2019-2020-2021.xlsx')
    multiple.analyse_multiple_exams(main_df, school_dict_object)

if __name__ == '__main__':
    main()
