﻿#!/usr/bin/python3
# -*- coding: utf-8 -*-

#  empresas-demons.py
#
#  Copyright (C) 2015 Caian Benedicto <caianbene@gmail.com>
#
#  This file is part of bovespa-tools
#
#  bovespa-tools is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  Asparagus is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import tprinting

import datetime
import math
import time
import argparse
import sys

###############################################################################
# Alguma definições
###############################################################################

#baseurl = "http://www.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoDemonstrativosFinanceiros.aspx"
baseurl = "http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoDemonstrativosFinanceiros.aspx"
queryurl = baseurl + "?codigoCvm=%s&idioma=pt-br"

matext = '.mat'

anoddid = 'ctl00_contentPlaceHolderConteudo_cmbAno'
itrdocid = 'ctl00_contentPlaceHolderConteudo_rptDocumentosITR_ctl%02d_lnkDocumento'
dfpdocid = 'ctl00_contentPlaceHolderConteudo_rptDocumentosDFP_ctl%02d_lnkDocumento'
#grupoid1 = 'ctl00_cphPopUp_cmbGrupo_cmbGrupo'
grupoid1 = 'cmbGrupo'
grupoval1 = {
    'i' : 'DFs Individuais',
    'c' : 'DFs Consolidadas'
}
#quadroid1 = 'ctl00_cphPopUp_cmbQuadro_cmbQuadro'
quadroid1 = 'cmbQuadro'
quadroval1 = {
    'bpa' : 'Balanço Patrimonial Ativo',
    'bpp' : 'Balanço Patrimonial Passivo',
    'dre' : 'Demonstração do Resultado',
    'dfc' : 'Demonstração do Fluxo de Caixa'
}
#formframeid = 'ctl00_cphPopUp_iFrameFormulariosFilho'
formframeid = 'iFrameFormulariosFilho'

datefmt = '%d/%m/%Y'

clicktimeout = 1
timeoutsleep = 1

headerxpath = "//table[@id='ctl00_cphPopUp_tbDados']//tr[1]//td"
tablexpath = "//table[@id='ctl00_cphPopUp_tbDados']//td"

#asserttitle1 = '| Empresas Listadas | BM&FBOVESPA'
asserttitle1 = 'Untitled Page'
asserttitle2 = 'ENET - Formulário de Referência'
assertheader = (
    ' Conta ',
    ' Descrição '
)

###############################################################################
# Seleciona um item de uma caixa drop-down
###############################################################################

def clickDropDownItem(ddid, text, driver):
    
    #dropimg = driver.find_element_by_id("%s_Image" % str(ddid))
    dropimg = driver.find_element_by_id("%s" % str(ddid))
    
    assert dropimg is not None
    
    # dropimg.click()
    driver.execute_script("arguments[0].click();", dropimg)

    dropitem = None
    # for i in driver.find_elements_by_xpath(("//*[@id='%s_DropDown']//*" % str(ddid))):
    for i in driver.find_elements_by_xpath(("//*[@id='%s']//*" % str(ddid))):
        if i.text == str(text):
            dropitem = i
            break

    assert dropitem is not None
    assert dropitem.is_displayed() is True
    
    dropitem.click()

###############################################################################
# Calcula o trimeste e ano anteriores a uma data
###############################################################################

def lastPeriod(date):
    year = date.year
    trimester = ((date.month-1) // 3)
    if trimester == 0:
        year -= 1
        trimester = 4
    return (trimester, year)

###############################################################################
# Calcula o trimeste e ano atuais de uma data
###############################################################################

def currentPeriod(date):
    year = date.year
    trimester = ((date.month-1) // 3)+1
    return (trimester, year)

###############################################################################
# Procura um documento de demonstracao
###############################################################################

def getReportDocElem(docfmt, trimester, year, driver):
    itritem = None
    i = 0

    while True:
        e = driver.find_elements_by_id(docfmt % i)
        i += 1

        if len(e) == 0:
            break

        assert len(e) == 1

        idate = e[0].text.split(' ')[0]
        idate = datetime.datetime.strptime(idate, datefmt)

        t, y = currentPeriod(idate)

        if trimester == t and year == y:
            itritem = e[0]
            break

    return itritem

###############################################################################
# Carrega trimestres menores que 4
###############################################################################

def getTri1To3Table(cvm, trimester, year, grupo, quadro):

    # Cria um driver do Firefox (mude pro seu navegador), abre a 
    # página de query e verifica se está na página certa

    #driver = webdriver.Firefox()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=r"C:\Users\vinicio_si\Downloads\chromedriver.exe", chrome_options=chrome_options)
    
    driver.get(queryurl % str(cvm))

    #assert driver.title == asserttitle1

    # Seleciona o ano do periodo

    clickDropDownItem(anoddid, year, driver)
    
    # Procura o link do documento para o periodo

    itritem = getReportDocElem(itrdocid, trimester, year, driver)

    assert itritem is not None

    itritem.click()
    
    # Muda para a nova janela 

    infowin = driver.window_handles[-1]
    driver.switch_to_window(infowin)

    # assert driver.title == asserttitle2

    # Seleciona a DRE individual

    clickDropDownItem(grupoid1, grupo, driver)
    
    clickDropDownItem(quadroid1, quadro, driver)
    
    # Muda para o frame do resultado

    frame = driver.find_element_by_id(formframeid)

    assert frame is not None

    driver.switch_to_frame(frame)

    # Lê o cabeçalho da tabela, o conteúdo e salva os links com o código CVM
    
    for i in range(clicktimeout):

        header = [elem.text.replace('\n','') for 
                  elem in 
                  driver.find_elements_by_xpath((headerxpath))]
        
        if len(header) != 0:
            break
        
        time.sleep(timeoutsleep)

    table = [elem.text for 
             elem in 
             driver.find_elements_by_xpath((tablexpath))]

    # Fecha todas as janelas

    handles = list(driver.window_handles)
    for w in handles:
        driver.switch_to_window(w)
        driver.close()

    # Valida os cabeçalhos, dados da tabela e links

    assert len(header) >= len(assertheader) + 1

    for i in range(len(assertheader)):
        assert header[i] == assertheader[i]

    # Garante que o terceiro campo do demonstrativo é o periodo atual

    p0 = header[2].strip().split(' ')[0].strip()
    p1 = header[2].strip().split(' ')[-1].strip()
    
    p0 = datetime.datetime.strptime(p0, datefmt)
    p1 = datetime.datetime.strptime(p1, datefmt)
    
    t0, y0 = currentPeriod(p0)
    t1, y1 = currentPeriod(p1)

    assert trimester == t0
    assert trimester == t1
    assert year == y0
    assert year == y1

    # Garante que o terceiro campo do demonstrativo se estende desde o T1 até o atual
    
    if trimester > 1:
        p0 = header[3].strip().split(' ')[0].strip()
        p1 = header[3].strip().split(' ')[-1].strip()
        
        p0 = datetime.datetime.strptime(p0, datefmt)
        p1 = datetime.datetime.strptime(p1, datefmt)
        
        t0, y0 = currentPeriod(p0)
        t1, y1 = currentPeriod(p1)
        
        assert 1 == t0
        assert trimester == t1
        assert year == y0
        assert year == y1

    assert len(table) % len(header) == 0

    # Monta a tabela pulando os len(header) primeiros campos que são o cabeçalho
    
    table2 = [table[k:k+len(header)] for k in range(len(header),len(table),len(header))]

    # Reformata o cabeçalho

    header2 = list(header)
    
    for i in range(2,len(header2)):
        p0 = header2[i].strip().split(' ')[0].strip()
        p1 = header2[i].strip().split(' ')[-1].strip()
        
        p0 = datetime.datetime.strptime(p0, datefmt)
        p1 = datetime.datetime.strptime(p1, datefmt)
        
        t0, y0 = currentPeriod(p0)
        t1, y1 = currentPeriod(p1)
        
        if t0 == t1 and y0 == y1:
            header2[i] = 'T%d/%d' % (t0,y0)
        else:
            header2[i] = 'T%d/%d - T%d/%d' % (t0,y0,t1,y0)

    return (header2, table2)

###############################################################################
# Carrega o quarto trimestre (resultado anual)
###############################################################################

def getTri4Table(cvm, year, grupo, quadro, driver):

    # Cria um driver do Firefox (mude pro seu navegador), abre a 
    # página de query e verifica se está na página certa

    #driver = webdriver.Firefox()

    driver.get(queryurl % str(cvm))

    #assert driver.title == asserttitle1

    # Seleciona o ano do periodo

    clickDropDownItem(anoddid, year, driver)

    # Procura o link do documento para o periodo

    itritem = getReportDocElem(dfpdocid, 4, year, driver)

    assert itritem is not None

    itritem.click()

    # Muda para a nova janela 

    infowin = driver.window_handles[-1]
    driver.switch_to_window(infowin)
    time.sleep(0.3)
    # assert driver.title == asserttitle2

    # Seleciona a DRE individual
    clickDropDownItem(grupoid1, grupo, driver)
    clickDropDownItem(quadroid1, quadro, driver)
    # Muda para o frame do resultado

    frame = driver.find_element_by_id(formframeid)

    assert frame is not None

    driver.switch_to_frame(frame)
    time.sleep(0.3)

    # Lê o cabeçalho da tabela, o conteúdo e salva os links com o código CVM
    
    for i in range(clicktimeout):

        header = [elem.text.replace('\n','') for 
                  elem in 
                  driver.find_elements_by_xpath((headerxpath))]
        
        if len(header) != 0:
            break
        
        time.sleep(timeoutsleep)

    table = [elem.text for 
             elem in 
             driver.find_elements_by_xpath((tablexpath))]

    # Fecha todas as janelas

    handles = list(driver.window_handles)
    for w in handles:
        driver.switch_to_window(w)
        driver.close()

    # Valida os cabeçalhos, dados da tabela e links

    assert len(header) >= len(assertheader) + 1

    for i in range(len(assertheader)):
        assert header[i] == assertheader[i]

    # Garante que o terceiro campo do demonstrativo se estende desde o T1 até T4

    p0 = header[2].strip().split(' ')[0].strip()
    p1 = header[2].strip().split(' ')[-1].strip()

    p0 = datetime.datetime.strptime(p0, datefmt)
    p1 = datetime.datetime.strptime(p1, datefmt)

    t0, y0 = currentPeriod(p0)
    t1, y1 = currentPeriod(p1)

    # assert t0 == 1
    assert t1 == 4
    assert year == y0
    assert year == y1

    assert len(table) % len(header) == 0

    # Monta a tabela pulando os len(header) primeiros campos que são o cabeçalho

    table2 = [table[k:k+len(header)] for k in range(len(header),len(table),len(header))]

    # Reformata o cabeçalho

    header2 = list(header)

    for i in range(2,len(header2)):
        p0 = header2[i].strip().split(' ')[0].strip()
        p1 = header2[i].strip().split(' ')[-1].strip()
        
        p0 = datetime.datetime.strptime(p0, datefmt)
        p1 = datetime.datetime.strptime(p1, datefmt)
        
        t0, y0 = currentPeriod(p0)
        t1, y1 = currentPeriod(p1)
        
        if t0 == t1 and y0 == y1:
            header2[i] = 'T%d/%d' % (t0,y0)
        else:
            header2[i] = 'T%d/%d - T%d/%d' % (t0,y0,t1,y0)

    return (header2, table2)

def getNumAcoes(cvm, year, grupo, quadro, driver):

    numAcoes = None
    numDocumento = None
    tpDocumento = None

    driver.get(queryurl % str(cvm))

    # Seleciona o ano do periodo

    clickDropDownItem(anoddid, year, driver)

    # Procura o link do documento para o periodo

    itritem = getReportDocElem(dfpdocid, 4, year, driver)

    assert itritem is not None
    
    numDocumento = itritem.get_attribute('href').split('=')[1].split('&')[0]
    tpDocumento = itritem.get_attribute('href').split('=')[2].split('\'')[0]

    itritem.click()
    
    # Muda para a nova janela 

    infowin = driver.window_handles[-1]
    driver.switch_to_window(infowin)
    time.sleep(3)
    # assert driver.title == asserttitle2

    # Seleciona a DRE individual
    clickDropDownItem(grupoid1, grupo, driver)
    clickDropDownItem(quadroid1, quadro, driver)
    # Muda para o frame do resultado

    frame = driver.find_element_by_id(formframeid)

    assert frame is not None

    driver.switch_to_frame(frame)
    time.sleep(3)

    # Lê o cabeçalho da tabela, o conteúdo e salva os links com o código CVM
    
    numAcoes = driver.find_elements_by_xpath("//div[@id='UltimaTabela']//table[1]//tr[5]//td[2]")[0].text

    # Fecha todas as janelas

    handles = list(driver.window_handles)
    for w in handles:
        driver.switch_to_window(w)
        driver.close()

    return (numAcoes, numDocumento, tpDocumento)

def getProventos(cvm, year, grupo, quadro, numDoc, tpDoc, driver):
    queryurl2 = "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento=%s&CodigoTipoInstituicao=%s"
    driver.get(queryurl2 % (str(numDoc), str(tpDoc)))

    # Seleciona a DRE individual
    clickDropDownItem(grupoid1, grupo, driver)
    clickDropDownItem(quadroid1, quadro, driver)

    time.sleep(3)

    frame = driver.find_element_by_id(formframeid)
    assert frame is not None

    driver.switch_to_frame(frame)

    time.sleep(3)

    header = [elem.text for
                elem in 
                driver.find_elements_by_xpath("(//div[@class='tabelaSemBorda'])[1]//span[@class='labelOld']")]
    
    header2 = list(header)

    table = [elem.text for
                elem in
                driver.find_elements_by_xpath("//div[@class='tabelaSemBorda']//span[@class='semBordaEsquerda']")]

    table2 = [table[k:k+len(header)] for k in range(0,len(table),len(header))]
    # Fecha todas as janelas

    handles = list(driver.window_handles)
    for w in handles:
        driver.switch_to_window(w)
        driver.close()

    return (header2, table2)

###############################################################################
# Rotina principal
###############################################################################

def main(outfile, cvm, trimester, year, grupo, val, log, numDoc, tpDoc):
    
    if trimester < 4:
        header2, table2 = getTri1To3Table(cvm, trimester, year, grupo, val)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(executable_path=r"C:\Users\vinicio_si\Downloads\chromedriver.exe", chrome_options=chrome_options)
        
        log = open("log" + log, 'a', encoding = 'utf-8')

        try:

            if grupo == 'Dados da Empresa' and val == 'Composição do Capital':
                numAcoes, numDocumento, tpDocumento = getNumAcoes(cvm, year, grupo, val, driver)

                f = open(outfile, 'wt', encoding = 'utf-8')
                f.write(numAcoes)
                f.close()

                log.write("ok_" + outfile + "_" + numDocumento + "_" + tpDocumento + '\n')
            elif grupo == 'Dados da Empresa' and val == 'Proventos em Dinheiro':
                header2, table2 = getProventos(cvm, year, grupo, val, numDoc, tpDoc, driver)

                tprinting.writeTable(outfile, header2, table2)

                log.write("ok_" + outfile + "_" + str(numDoc) + "_" + str(tpDoc) + '\n')
            else:                    

                header2, table2 = getTri4Table(cvm, year, grupo, val, driver)

                # Imprime a tabela

                if outfile.endswith(matext):
                    tprinting.writeMat(outfile, header2, table2)
                else:
                    tprinting.writeTable(outfile, header2, table2)
                log.write("ok_" + outfile + '\n')
            log.close()
            print("ok_" + outfile)
        except:
            log.write("erro_" + outfile + "_" + str(sys.exc_info()[0]) + '\n')
            log.close()
            print("erroN_" + outfile, sys.exc_info()[0])
            driver.close()
            print()

###############################################################################
# Ponto de entrada do script
###############################################################################

if __name__ == '__main__':

    # Parsing dos argumentos de entrada

    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default='demonstrativoPetro.txt', help='arquivo de saida')
    parser.add_argument('--cvm', type=int, default=[9512], nargs=1, help='Codigo CVM da empresa')
    parser.add_argument('--tri', type=int, default=4, help='Trimestre')
    parser.add_argument('--year', type=int, default=2018, help='Ano')
    parser.add_argument('--mode', type=str, default='cbpa', help='Modo')
    args = parser.parse_args()

    assert args.cvm is not None

    # Calcula o periodo atual e o anterior

    ltri, lyear = lastPeriod(datetime.datetime.today())
    ctri, cyear = currentPeriod(datetime.datetime.today())

    # Ajusta o periodo de busca

    if args.tri <= 0 and args.year <= 0:
        tri = ltri
        year = lyear
    elif args.tri <= 0:
        tri = ctri
        year = args.year
    elif args.year <= 0:
        tri = args.tri
        year = cyear
    else:
        tri = args.tri
        year = args.year

    assert tri > 0
    assert tri <= 4

    # Ajusta o modo de busca

    grupo = grupoval1[args.mode[0]]
    quadro = quadroval1[args.mode[1:]]

    main(args.out, args.cvm[0], tri, year, grupo, quadro)
