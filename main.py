from analise_olimpica import objects, multiple

def main():
    school_dict_object = objects.SchoolDict.from_school_dict_csv()

    multiple.analyse_multiple_exams('20220105_GERAL2019-2020-2021.csv', school_dict_object)

if __name__ == '__main__':
    main()
