import pandas as pd

dfFinal = pd.read_csv("consCodUOL.csv", sep = ";")

dfFinal.drop(dfFinal.columns[[0,3]], axis=1, inplace = True)

dfConsolidadp = pd.read_csv("CONSOLIDADO.csv", sep = ";")

dfFinal = dfFinal.merge(dfConsolidadp.loc[:,["cvm", "ano", "QtdAcoes", "Volume"]], on = ["cvm", "ano"], how = "inner")

for c in ['1', '1.01.01', '1.01.02', '1.02.01.01',
       '1.02.01.02', '1.02.01.03', '2.01.04', '2.01.02', '2.02.01', '3.05',
       'QtdAcoes']:
    dfFinal[c] = pd.to_numeric(dfFinal[c].str.replace(".", ""))

dfFinal["open"] = pd.to_numeric(dfFinal["open"].str.replace(".", "").str.replace(",", "."))
dfFinal["close"] = pd.to_numeric(dfFinal["close"].str.replace(".", "").str.replace(",", "."))

dfFinal["EBIT"] = dfFinal["3.05"]
dfFinal["ROIC"] = dfFinal["EBIT"] / (dfFinal["1"] - dfFinal["2.01.02"] - dfFinal["1.01.01"])
dfFinal["EV"] = dfFinal["QtdAcoes"] * dfFinal["open"]
dfFinal["DVIDALIQUIDA"] = dfFinal["2.01.04"] + dfFinal["2.02.01"] - dfFinal["1.01.01"] - dfFinal["1.01.02"] - dfFinal["1.02.01.01"] - dfFinal["1.02.01.02"] - dfFinal["1.02.01.03"]

dfFinal.to_csv("dfFinalUOL.csv", sep = ";", encoding = "utf-8-sig")