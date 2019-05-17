import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
from yahoofinancials import YahooFinancials
import sys

baseurl = "http://bvmf.bmfbovespa.com.br/pt-br/mercados/acoes/empresas/ExecutaAcaoConsultaInfoEmp.asp"
queryurl = baseurl + "?codCvm=%s"

codcvm = pd.read_csv("codcvm.csv", sep = ";")

colunas = ['cvm', 'codigo']
dfCodigosNegociacao = pd.DataFrame(columns=colunas)

for indice, row in codcvm.iloc[:].iterrows():

    html = urlopen(queryurl % row["cvm"])

    res = BeautifulSoup(html.read(),"html5lib")

    for link in res.find_all("a", {"class":"LinkCodNeg"}):
        cdNeg = link.getText()
        dfCodigosNegociacao.loc[cdNeg] = [row["cvm"], cdNeg]
        
dfCodigosNegociacao.to_csv("codnegociacao.csv", sep = ";", encoding = 'utf-8-sig')

dfConsolidado = pd.read_csv("CONSOLIDADO.csv", sep = ";")

for c in dfConsolidado.columns:
    print(c)

dfCons = dfConsolidado.loc[:,["ano", "cvm", "Volume", "1", "1.01.01", "1.01.02", "1.02.01.01", "1.02.01.02", "1.02.01.03", "2.01.04", "2.01.02", "2.02.01", "3.05"]]

for c in dfConsolidado.columns:
    print(c)

dfCodigosNegociacao = dfCodigosNegociacao.merge(dfCons, how='inner', on = 'cvm')

dfCons["cvm"]
dfCodigosNegociacao["cvm"] = pd.to_numeric(dfCodigosNegociacao["cvm"])

dfCodigosNegociacao.to_csv("consCod.csv", sep = ";", encoding = 'utf-8-sig')

# pegar preços
log = open("log" + "Preco", 'a', encoding = 'utf-8')
for indice, codigoNeg in dfCodigosNegociacao.iloc[:1].iterrows():
    try:    
        ticker = codigoNeg['codigo'] + '.SA'
        yahoo_financials = YahooFinancials(ticker)

        abertura = yahoo_financials.get_historical_price_data(str(codigoNeg['ano']) + '-01-02', str(codigoNeg['ano']) + '-01-05', 'daily')
        fechamento = yahoo_financials.get_historical_price_data(str(codigoNeg['ano']) + '-12-29', str(int(codigoNeg['ano']) + 1) + '-01-01', 'daily')

        codigoNeg['open'] = abertura[ticker]['prices'][0]['close']
        codigoNeg['close'] = fechamento[ticker]['prices'][len(fechamento[ticker]['prices'])-1]['close']
        log.write("ok_" + ticker + "_" + str(codigoNeg['ano']) + "_" + str(sys.exc_info()[0]) + '\n')
    except:
        log.write("erro_" + ticker + "_" + str(codigoNeg['ano']) + "_" + str(sys.exc_info()[0]) + '\n')
log.close()