import pandas as pd
import glob

# Lista todos os nomes de arquivos .xlsx
xlsx_file_names = glob.glob('*.xlsx')

# Para cada um, converte para CSV
for f in xlsx_file_names:
    pd.read_excel(f).to_csv(f.replace('xlsx', 'csv'), index=None, header=True)