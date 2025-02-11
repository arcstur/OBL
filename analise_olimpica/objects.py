import pandas as pd
from dataclasses import dataclass

from . import utils
from .exceptions import NonExistantColumn

DEFAULT_RANGE_SPAN = [1, 2, 3, 4, 5, 6, 11, 31, 51, 101]


class SchoolDict:
    @classmethod
    def from_file_array(cls, filename_array):
        df_array = []

        for filename in filename_array:
            print(f"Loading... {filename}")
            df = utils.get_dataframe(filename)
            df_array.append(df)

        return cls(df_array=df_array)

    @classmethod
    def from_file(cls, filename):
        df_array = [utils.get_dataframe(filename)]

        return cls(df_array=df_array)

    @classmethod
    def from_dataframe(cls, df):
        df_array = [df]

        return cls(df_array=df_array)

    @classmethod
    def from_school_dict_csv(cls, csv_file="school_dict.csv"):
        df = pd.read_csv(csv_file)

        school_dict = dict(df.itertuples(index=False))

        return cls(school_dict=school_dict)

    def __init__(
        self, school_dict=None, df_array=None, remove_empty_schools=True, load_dict=True
    ):
        if not (school_dict or df_array):
            raise ValueError("At least one of school_dict or df_array must be given")

        if school_dict:
            self.school_dict = school_dict

        if df_array:
            self.df_array = df_array

            if remove_empty_schools:
                self.remove_null_school()
            if load_dict:
                self.load_dict()

    def remove_null_school(self):
        for i, df in enumerate(self.df_array):
            new_df = df.dropna(subset=["Código INEP"])
            new_df = new_df[df["Código INEP"] != 0]
            self.df_array[i] = new_df

    def load_dict(self):
        self.school_dict = dict()
        empty_adm_name_list = []

        # ---
        # First run, saving non-empty
        for df in self.df_array:
            try:
                col = utils.get_columns(df, ("Código INEP", "Administração"))
            except NonExistantColumn:
                print("Skipping df with non-existant column")
                df.to_remove = True
                continue

            for index, row in df.iterrows():
                school_code, school_adm = (
                    row[col["Código INEP"]],
                    row[col["Administração"]],
                )

                if not (
                    pd.isnull(school_adm) or school_adm == ""
                ):  # if there is a value for administration
                    # Save to the dict, if it isn't already there
                    if school_code not in self.school_dict.keys():
                        self.school_dict[school_code] = school_adm

                    elif self.school_dict[school_code] != school_adm:
                        print(
                            f"{school_code} tem dois valores diferentes para administração."
                        )
                else:
                    # Append school name to the to-be-fixed school name list
                    empty_adm_name_list.append(school_code)

        # removing the ones with non-existant columns
        self.df_array = [
            df for df in self.df_array if not getattr(df, "to_remove", False)
        ]

        # ---
        # Second run, fixing schools with empty adm
        for df in self.df_array:
            col = utils.get_columns(df, ("Código INEP", "Administração"))

            # Get only schools left out by previous run
            df_empty_adm = df[df[col["Código INEP"]].isin(empty_adm_name_list)]

            for index, row in df_empty_adm.iterrows():
                school_code, school_adm = (
                    getattr(row, col["Código INEP"]),
                    getattr(row, col["Administração"]),
                )

                # If the school already has a value in the dict
                if school_code in self.school_dict.keys():
                    school_adm = self.school_dict[school_code]

                # If not, ask the user, and save in the dict
                else:
                    school_adm = utils.ask_new_adm_for_school(school_code)

                    self.school_dict[school_code] = school_adm

        # If there was a school name in the to-be-fixed name list
        if empty_adm_name_list:
            new_file = "school_dict.csv"
            df = pd.DataFrame(
                self.school_dict.items(),
                columns=["Código INEP", "Administração"],
            )
            df.to_csv(new_file, index=False)
            print()
            print(f"O dicionário de escolas atualizado foi salvo no arquivo {new_file}")
            input("Pressione Enter para continuar.")

    def is_public(self, school_code):
        if school_code in self.school_dict:
            return self.school_dict[school_code].lower() in {
                "state",
                "federal",
                "municipal",
                "pública",
                "publica",
            }

    def is_private(self, school_code):
        if school_code in self.school_dict:
            return self.school_dict[school_code].lower() in {"privada", "particular"}


class Exam:
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def fetch_data(self, school_dict_object):
        df = self.df

        col = utils.get_columns(
            df,
            (
                "Fractal ID",
                "Categoria",
                "Sexo",
                "Código INEP",
                "UF",
                "Cidade",
                "Fases",
                "Medalhas",
            ),
        )

        self.set_fractal_id = set(df[col["Fractal ID"]].unique())

        self.count_total = len(df)

        # Category
        self.value_counter_cat = df[col["Categoria"]].value_counts()

        # Sex
        self.value_counter_sexo = df[col["Sexo"]].value_counts()

        # Participants
        df_participants = df.dropna(subset=[col["Fases"]])
        self.participants_count_total = df_participants[col["Fases"]].count()
        self.participants_value_counter_sexo = df_participants[
            col["Sexo"]
        ].value_counts()

        # Medalists
        df_medalists = df.dropna(subset=[col["Medalhas"]])
        self.medalists_count_total = df_medalists[col["Medalhas"]].count()
        self.medalists_value_counter_sexo = df_medalists[col["Sexo"]].value_counts()

        # Cities and UF
        value_counter_city = df[col["Cidade"]].value_counts()

        self.city_amount_per_participant_qnt = (
            value_counter_city.value_counts().sort_values(ascending=False)
        )
        self.count_city = self.city_amount_per_participant_qnt.sum()

        self.value_counter_UF = df[col["UF"]].value_counts()
        self.count_UF = self.value_counter_UF.value_counts().sum()

        # Schools
        school_column_nonnull = df.dropna(subset=[col["Código INEP"]])[
            col["Código INEP"]
        ]

        # The doubel value counter gets the amount of schools per given quantity of participants
        value_counter_school = school_column_nonnull.value_counts()
        self.school_amount_per_participant_qnt = (
            value_counter_school.value_counts().sort_values(ascending=False)
        )

        self.set_school = set(school_column_nonnull)
        self.count_escola = len(self.set_school)

        # Participants in a private or public school
        self.count_public_participants, self.count_private_participants = 0, 0
        self.count_admnotinfo_participants = 0

        for school_code in school_column_nonnull:
            if school_dict_object.is_public(school_code):
                self.count_public_participants += 1
            elif school_dict_object.is_private(school_code):
                self.count_private_participants += 1
            else:
                self.count_admnotinfo_participants += 1

        # How many schools are public or private
        self.count_public_school, self.count_private_school = 0, 0
        self.count_admnotinfo_school = 0

        for school_code in self.set_school:
            if school_dict_object.is_public(school_code):
                self.count_public_school += 1
            elif school_dict_object.is_private(school_code):
                self.count_private_school += 1
            else:
                self.count_admnotinfo_school += 1

    def get_results_dict(self):
        self.results = dict()
        self.results["Total"] = self.count_total

        # Categories
        for cat, qnt in self.value_counter_cat.items():
            self.results[f"Inscritos: Categoria {cat}"] = qnt

        self.results["Inscritos de escola pública"] = self.count_public_participants
        self.results["Inscritos de escola privada"] = self.count_private_participants
        self.results["Inscritos de escola com adm. não info."] = (
            self.count_admnotinfo_participants
        )

        # Sex
        for sexo, qnt in self.value_counter_sexo.items():
            self.results[f"Inscritos: Sexo {sexo}"] = qnt
        # Girls ratio
        self.results[f"Inscritos: % de meninas"] = utils.str_percentage(
            self.value_counter_sexo["Feminino"], self.value_counter_sexo.sum()
        )

        # Participants
        self.results["Participantes"] = self.participants_count_total
        # Participants - Ratio
        self.results["% de participantes"] = utils.str_percentage(
            self.participants_count_total, self.count_total
        )
        # Participants - Sex
        for sexo, qnt in self.participants_value_counter_sexo.items():
            self.results[f"Participantes: Sexo {sexo}"] = qnt
        if "Feminino" in self.participants_value_counter_sexo:
            self.results[f"Participantes: % de meninas"] = utils.str_percentage(
                self.participants_value_counter_sexo["Feminino"],
                self.participants_value_counter_sexo.sum(),
            )

        # Medalists
        self.results["Medalhistas"] = self.medalists_count_total
        # Medalists - Sex
        for sexo, qnt in self.medalists_value_counter_sexo.items():
            self.results[f"Medalhistas: Sexo {sexo}"] = qnt
        if "Feminino" in self.medalists_value_counter_sexo:
            self.results[f"Medalhistas: % de meninas"] = utils.str_percentage(
                self.medalists_value_counter_sexo["Feminino"],
                self.medalists_value_counter_sexo.sum(),
            )

        # Schools
        self.results["Escolas"] = self.count_escola
        self.results["Escolas públicas"] = self.count_public_school
        self.results["Escolas privadas"] = self.count_private_school
        self.results["Escolas com adm. não info."] = self.count_admnotinfo_school
        self.results["Razão inscritos/escolas"] = (
            f"{(self.count_total/self.count_escola)}"
        )

        range_span = DEFAULT_RANGE_SPAN
        utils.amount_of_per_participant_qnt(
            self.results, self.school_amount_per_participant_qnt, range_span, "Escolas"
        )

        # Cities
        self.results["Cidades"] = self.count_city
        self.results["Razão inscritos/cidades"] = (
            f"{(self.count_total/self.count_city)}"
        )

        utils.amount_of_per_participant_qnt(
            self.results, self.city_amount_per_participant_qnt, range_span, "Cidades"
        )

        # UF
        self.results["Estados"] = self.count_UF
        for estado, qnt in self.value_counter_UF.items():
            self.results[f"Estado {estado}"] = qnt

        return self.results

    def store_data(self):
        df = pd.DataFrame(self.results.items(), columns=["Nome", "Valor"])
        df.to_excel(f"data_{self.name}.xlsx", index=False)

@dataclass
class ExamFile:
    filename: str
    olympiad: str
    year: int
