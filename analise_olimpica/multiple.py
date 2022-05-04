import pandas as pd 
from collections import Counter

from . import objects, utils

def analyse_multiple_exams(main_df, school_dict_object, analyse_year=True):

    col = utils.get_columns(main_df, ('Ano', 'Olimpíada', 'Fractal ID'))

    main_exam = objects.Exam('Geral', main_df)
    main_exam.fetch_data(school_dict_object)
    keys = main_exam.get_results_dict().keys()

    # results dataframe
    results_df = pd.DataFrame(index=keys)

    # results for the year comparison
    year_results_df = pd.DataFrame()

    # results dictionary for the olympiad comparison
    oly_results_df = pd.DataFrame()
    # a dictionary is needed so that we don't have to loop over olympiads again 
    oly_results_dict = {}

    # count number for the range_span
    max_number_oly = len(main_df[col['Olimpíada']].unique())
    max_number_year = len(main_df[col['Ano']].unique())

    for year in main_df[col['Ano']].unique():

        year_df = main_df.loc[main_df[col['Ano']] == year]

        year_fractal_id_sets = []

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

            # add the new unique Fractal IDs
            year_fractal_id_sets += exam.set_fractal_id

            # add to the oly_results_dictionary
            oly_results_dict.setdefault(oly, [])
            oly_results_dict[oly] += exam.set_fractal_id

        # count how many repeating FIDs (how many appear 1 time, 2 times, ...)
        series = pd.DataFrame({'FID': year_fractal_id_sets})['FID'].value_counts().value_counts()
        
        year_dict = utils.amount_of_per_participant_qnt({}, series, range_span=[i+1 for i in range (max_number_oly+1)],  quantity_name='alunos', property_name_tuple=('inscrição', 'inscrições'))

        for key, value in year_dict.items():
            year_results_df.loc[key, year] = value

    # ------
    # Compare olympiads yearly
    # ------
    for oly in main_df[col['Olimpíada']].unique():

        oly_sets = oly_results_dict[oly]
        series = pd.DataFrame({'FID': oly_sets})['FID'].value_counts().value_counts()

        oly_dict = utils.amount_of_per_participant_qnt({}, series, range_span=[i+1 for i in range (max_number_year+1)],  quantity_name='alunos', property_name_tuple=('ano de inscrição', 'anos de inscrição'))

        for key, value in oly_dict.items():
            oly_results_df.loc[key, oly] = value


    # ------
    # Writing
    # ------

    writer = pd.ExcelWriter('super_data.xlsx')
    
    results_df.to_excel(writer, sheet_name='Geral')
    year_results_df.to_excel(writer, sheet_name='Comparação_Anual')
    oly_results_df.to_excel(writer, sheet_name='Comparação_Olímpica')

    writer.save()