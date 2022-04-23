import pandas as pd 

from . import objects, utils

def analyse_multiple_exams(main_file, school_dict_object):

    main_df = utils.get_dataframe(main_file)

    main_exam = objects.Exam('Geral', main_df)

    main_exam.fetch_data(school_dict_object)
    keys = main_exam.get_results_dict().keys()

    results_df = pd.DataFrame(index=keys)

    col = utils.get_columns(main_df, ('Ano', 'Olimpíada'))

    for year in main_df[col['Ano']].unique():

        year_df = main_df.loc[main_df[col['Ano']] == year]

        for oly in year_df[col['Olimpíada']].unique():
            name = f'{year}_{oly}'
            print(f'Analysing {name}...')

            oly_df = year_df.loc[year_df[col['Olimpíada']] == oly]

            exam = objects.Exam(name, df=oly_df)
            exam.fetch_data(school_dict_object)
            results = exam.get_results_dict()

            for key in results_df.index:
                if key in results:
                    results_df.loc[key, name] = results[key]
                else:
                    results_df.loc[key, name] = 0

    results_df.to_excel('super_data.xlsx')
            