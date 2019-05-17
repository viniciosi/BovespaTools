import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
from yahoofinancials import YahooFinancials
import sys
import eventlet
eventlet.monkey_patch()

dfCodigosNegociacao = pd.read_csv("consCod.csv", sep = ";")

# pegar preços
for indice, codigoNeg in dfCodigosNegociacao.iloc[:1000].iterrows():
    log = open("log" + "Preco", 'a', encoding = 'utf-8')
    print("i_" + str(codigoNeg['ano']) + "_" + codigoNeg['codigo'])
    try:    
        ticker = codigoNeg['codigo'] + '.SA'
        yahoo_financials = YahooFinancials(ticker)

        with eventlet.Timeout(3):
            abertura = yahoo_financials.get_historical_price_data(str(codigoNeg['ano']) + '-01-02', str(codigoNeg['ano']) + '-01-05', 'daily')
        fechamento = yahoo_financials.get_historical_price_data(str(codigoNeg['ano']) + '-12-29', str(int(codigoNeg['ano']) + 1) + '-01-01', 'daily')

        codigoNeg['open'] = abertura[ticker]['prices'][0]['close']
        codigoNeg['close'] = fechamento[ticker]['prices'][len(fechamento[ticker]['prices'])-1]['close']
        dfCodigosNegociacao.at[indice, 'open'] = codigoNeg['open']
        dfCodigosNegociacao.at[indice, 'close'] = codigoNeg['close']
        log.write("ok_" + ticker + "_" + str(codigoNeg['ano']) + '\n')
    except:
        log.write("erro_" + ticker + "_" + str(codigoNeg['ano']) + "_" + str(sys.exc_info()[0]) + '\n')
    log.close()
dfCodigosNegociacao.to_csv("consCod1.csv", sep = ";", encoding = 'utf-8-sig')