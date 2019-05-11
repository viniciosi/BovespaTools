import os
import pandas as pd

def getDemonstrativos(tipo):

    arquivos = os.listdir(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo)

    df_demonstrativos = pd.DataFrame()

    for arquivo in arquivos:
        # print(arquivo)

        demonstrativo = pd.read_csv(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo + "\\" + arquivo, sep=";")

        # demonstrativo.head()
        # demonstrativo.describe()
        # demonstrativo.dtypes
        # demonstrativo.columns

        demonstrativo.columns = ['conta', 'descr', 'valores', '2017', '2016'][:len(demonstrativo.columns)]
        demonstrativo.drop(columns = ['descr', '2017', '2016'][:len(demonstrativo.columns)-2], inplace = True)
        demonstrativo['conta'] = demonstrativo['conta'].str.strip()
        demonstrativo['valores'] = demonstrativo['valores'].str.strip()

        # demonstrativo[demonstrativo.columns[0:3]]
        # demonstrativo[['conta', 'valores']]

        demonstrativo = demonstrativo.set_index('conta').T

        demonstrativo['ano'] = arquivo.split('_')[0]
        demonstrativo['cvm'] = arquivo.split('_')[1]
        demonstrativo['empresa_descr'] = arquivo.split('_')[3]

        df_demonstrativos = pd.concat([df_demonstrativos, demonstrativo])

    df_demonstrativos.to_csv(tipo + '.csv', sep = ';')

def getProventos():

    tipo = "CPRO"
    
    arquivos = os.listdir(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo)

    df_demonstrativos = pd.DataFrame()

    for arquivo in arquivos:
        # print(arquivo)

        demonstrativo = pd.read_csv(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo + "\\" + arquivo, sep=";")

        # demonstrativo.head()
        # demonstrativo.describe()
        # demonstrativo.dtypes
        # demonstrativo.columns

        demonstrativo.columns = ['Evento', 'Aprovação', 'Início Pagamento', 'Espécie de Ação', 'Classe de Ação', 'Provento por Ação (Reais/Ação)']
        demonstrativo['Espécie de Ação'] = demonstrativo['Espécie de Ação'].str.strip()
        demonstrativo['Provento por Ação (Reais/Ação)'] = demonstrativo['Provento por Ação (Reais/Ação)'].str.strip()

        demonstrativo['ano'] = arquivo.split('_')[0]
        demonstrativo['cvm'] = arquivo.split('_')[1]
        demonstrativo['empresa_descr'] = arquivo.split('_')[3]

        df_demonstrativos = pd.concat([df_demonstrativos, demonstrativo])

    df_demonstrativos.to_csv(tipo + '.csv', sep = ';')

def getQtdOuVolume(tipo):

    arquivos = os.listdir(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo)

    df_demonstrativos = pd.DataFrame()

    for arquivo in arquivos:
        # print(arquivo)

        if tipo == "VOLU":
            cabecalho = ["Volume"]
        else:
            cabecalho = ["QtdAcoes"]

        demonstrativo = pd.read_csv(r"C:\Users\vinicio_si\Documents\demonstrativos\\" + tipo + "\\" + arquivo, sep=";", names = cabecalho)

        # demonstrativo.head()
        # demonstrativo.describe()
        # demonstrativo.dtypes
        # demonstrativo.columns

        demonstrativo['ano'] = arquivo.split('_')[0]
        demonstrativo['cvm'] = arquivo.split('_')[1]
        demonstrativo['empresa_descr'] = arquivo.split('_')[3]

        df_demonstrativos = pd.concat([df_demonstrativos, demonstrativo])

    df_demonstrativos.to_csv(tipo + '.csv', sep = ';')


#Consolidado Balanço Patrimonial Ativo
getDemonstrativos("CBPA")
#Consolidado Balanço Patrimonial Passivo
getDemonstrativos("CBPP")
#Consolidado Demonstrativo de Resultados
getDemonstrativos("CDRE")
#Proventos e Dividendos
getProventos()
#Qtd de Acoes
getQtdOuVolume("CQTA")
#Volume
getQtdOuVolume("VOLU")

cbpa = pd.read_csv("CBPA.csv", sep=";")
cbpp = pd.read_csv("CBPP.csv", sep=";")
cdre = pd.read_csv("CDRE.csv", sep=";")
cqta = pd.read_csv("CQTA.csv", sep=";")
volu = pd.read_csv("VOLU.csv", sep=";")

consolidado = pd.merge(cbpa, cbpp, how='left', on = ['ano', 'cvm'])
consolidado = pd.merge(consolidado, cdre, how='left', on = ['ano', 'cvm'])
consolidado = pd.merge(consolidado, cqta, how='left', on = ['ano', 'cvm'])
consolidado = pd.merge(consolidado, volu, how='left', on = ['ano', 'cvm'])

consolidado.to_csv("CONSOLIDADO.csv", sep = ';')