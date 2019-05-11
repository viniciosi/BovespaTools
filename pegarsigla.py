import pandas as pd
from selenium import webdriver
import sys

empresas = pd.read_csv('revisao.csv', sep=";")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path=r"C:\Users\vinicio_si\Downloads\chromedriver.exe", chrome_options=chrome_options)

for indice, row in empresas.iloc[:601,].iterrows():

    log = open("log" + "VOL1", 'a', encoding = 'utf-8')

    try:

        outfile = str(row[0]) + "_" + str(row[1]) + "_VOLU_" + row[2].replace("/", "")

        driver.get("http://bvmf.bmfbovespa.com.br/sig/FormConsultaEmpresa.asp?strIdioma=P&strDtReferencia=12/%s" % row[0])

        campo_busca = driver.find_element_by_id("txtNomeSocEmissora")
        cmdBuscar = driver.find_element_by_id("cmdBuscar")

        campo_busca.send_keys(row[2])
        cmdBuscar.click()

        if (len(driver.find_elements_by_xpath("//a[@class='linkBusca']")) == 4 
                    or 0==0):
            # segue

            sigla = driver.find_elements_by_xpath("//font[@face='Arial']")[12].text

            driver.get("http://bvmf.bmfbovespa.com.br/sig/FormConsultaNegociacoes.asp?strTipoResumo=RES_NEGOCIACOES&strSocEmissora=%s&strDtReferencia=12/%s&strIdioma=P&intCodNivel=1&intCodCtrl=100" % (sigla, row[0]))

            volume = driver.find_elements_by_xpath("//td[@class='linhabcbold']")[3].text

            f = open(outfile, 'wt', encoding = 'utf-8')
            f.write(volume)
            f.close()

            print("ok_" + outfile)
            log.write("ok_" + outfile + '\n')

        else:
            # problema
            print("erroN_" + outfile, "mais que uma empresa")
            log.write("erroN_" + outfile + "_mais que uma empresa" + '\n')

    except:
        print("erroF_" + outfile, sys.exc_info()[0])
        log.write("erroF_" + outfile + "_" + str(sys.exc_info()[0]) + '\n')

    log.close()

driver.close()