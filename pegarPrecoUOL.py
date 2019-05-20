import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
from yahoofinancials import YahooFinancials
import sys
import eventlet
eventlet.monkey_patch()

dfCodigosNegociacao = pd.read_csv("consCod.csv", sep = ";")

dfCodigosNegociacao.drop(dfCodigosNegociacao.columns[[0,1,-1,-2]], axis=1, inplace = True)

queryurl = "http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=%s.SA&beginDay=1&beginMonth=1&beginYear=%s&endDay=5&endMonth=1&endYear=%s"
queryurl2 = "http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=%s.SA&beginDay=27&beginMonth=12&beginYear=%s&endDay=31&endMonth=12&endYear=%s"

# pegar preços
for indice, codigoNeg in dfCodigosNegociacao.iloc[:].iterrows():
    log = open("log" + "Preco", 'a', encoding = 'utf-8')
    print("i_" + str(codigoNeg['ano']) + "_" + codigoNeg['codigo'])
    try:    

        html = urlopen(queryurl % (codigoNeg['codigo'], codigoNeg['ano'], codigoNeg['ano']))
        res = BeautifulSoup(html.read(),"html5lib")
        tab = res.find("table", {"id":"tblInterday"})
        if tab:
            tab = res.find("table", {"id":"tblInterday"}).find("tbody").find_all("tr")
            abertura = tab[len(tab) - 1].find_all("td")[1].getText()

            html = urlopen(queryurl2 % (codigoNeg['codigo'], codigoNeg['ano'], codigoNeg['ano']))
            res = BeautifulSoup(html.read(),"html5lib")
            tab = res.find("table", {"id":"tblInterday"})
            if tab:
                tab = res.find("table", {"id":"tblInterday"}).find("tbody").find("tr")
                fechamento = tab.find_all("td")[1].getText()

                codigoNeg['open'] = abertura
                codigoNeg['close'] = fechamento
                dfCodigosNegociacao.at[indice, 'open'] = codigoNeg['open']
                dfCodigosNegociacao.at[indice, 'close'] = codigoNeg['close']
        log.write("ok_" + codigoNeg['codigo'] + "_" + str(codigoNeg['ano']) + '\n')
    except:
        log.write("erro_" + codigoNeg['codigo'] + "_" + str(codigoNeg['ano']) + "_" + str(sys.exc_info()[0]) + '\n')
    log.close()
dfCodigosNegociacao.to_csv("consCodUOL.csv", sep = ";", encoding = 'utf-8-sig')