import pandas as pd
import empresas_demons as ep
import sys

empresas = pd.read_csv('empresas.csv', sep=";")

# empresas[["Nome de Pregão", "Código CVM"]]
# empresas.iloc[:,[1,3]]

for ano in range(2016, 2017):
    for indice, row in empresas.iloc[:,[1,3]].iterrows():
        try:
            ep.main(str(ano) + "_" + str(row[1]) + "_CBPA_" + row[0], row[1], 4, ano, 'DFs Consolidadas', 'Balanço Patrimonial Passivo', "P11")
        except:
            print()
        # print(str(ano) + "_" + str(row[1]) + "_CBPA_" + row[0])

#empresas[empresas['Nome de Pregão'].str.strip() == 'IGB S/A']
#empresas['Nome de Pregão'].str.strip()

#empresas[364:365]