import pandas as pd
import empresas_demons as ep
import sys

empresas = pd.read_csv('revisao.csv', sep=";")

# empresas[["Nome de Pregão", "Código CVM"]]
# empresas.iloc[:,[1,3]]

for indice, row in empresas.iloc[601:1201,].iterrows():
    try:
        ep.main(str(row[0]) + "_" + str(row[1]) + "_CPRO_" + row[2].replace("/", ""), row[1], 4, row[0], 'Dados da Empresa', 'Proventos em Dinheiro', "PR12", row[3], row[4])
    except:
        print()
        print("erroF_" + str(sys.exc_info()[0]) + "_" + str(row[0]) + "_" + str(row[1]) + "_CPRO_" + row[2])

#empresas[empresas['Nome de Pregão'].str.strip() == 'IGB S/A']
#empresas['Nome de Pregão'].str.strip()

#empresas[249:250]
#ep.main(str(2010) + "_" + str(16284) + "_CBPA_" + '524', 16284, 4, 2010, 'DFs Consolidadas', 'Balanço Patrimonial Ativo', "R122")