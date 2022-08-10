# pip install pandas

import pandas as pd
import os
import numpy as np

timeFrame = "D1"
classCode = "TQBR"
csv_folder_find_anomalies = "csv_meta_fix"


# ok
classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB',
                   'AVAN', 'BANE', 'BANEP', 'BELU', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ',
                   'CHKZ', 'CHMF', 'CHMK', 'CIAN', 'CNTL', 'CNTLP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT',
                   'ELTZ', 'ENPG', 'ENRU', 'ETLN', 'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZP',
                   'GCHE', 'GEMA', 'GEMC', 'GLTR', 'GMKN', 'GTRK', 'HHRU', 'HIMCP', 'HMSG', 'HYDR', 'IGST', 'IGSTP',
                   'INGR', 'IRAO', 'IRGZ', 'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE',
                   'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKOP', 'KROT',
                   'KROTP', 'KRSB', 'KRSBP', 'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZOS', 'KZOSP', 'LENT', 'LIFE',
                   'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN',
                   'MDMG', 'MFGS', 'MFGSP', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MOEX', 'MRKC',
                   'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT', 'MTLR',
                   'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB',
                   'NNSBP', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB',
                   'PMSBP', 'POGR', 'POLY', 'POSI', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM', 'RDRB', 'RENI', 'RGSS',
                   'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB',
                   'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RZSB', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP',
                   'SELG', 'SFIN', 'SFTL', 'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'SPBE', 'STSB', 'STSBP',
                   'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB', 'TGKBP', 'TGKD',
                   'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS', 'UKUZ',
                   'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR', 'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP',
                   'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG',
                   'YKEN', 'YKENP', 'YNDX', 'YRSB', 'YRSBP', 'ZILL', 'ZVEZ']

#classSecurities = ['TRMK']

for secCode in classSecurities:
    file = f'{csv_folder_find_anomalies}\\{classCode}.{secCode}_{timeFrame}.csv'

    isFileExists = os.path.isfile(file)  # Существует ли файл
    if not isFileExists:  # Если файл не существует
        print(f'Файл {file} не найден')

    try:
        df = pd.read_csv(file, sep=',', index_col="datetime")  # Считываем файл в DataFrame
        #df["datetime"] = pd.to_datetime(df["datetime"])
        #print(df, "\n----------------------------------------------------------------------------------------")

        #print(df, len(df))

        # df_p = df.pct_change()
        # print(df_p)
        p_o_c = []
        p_h_l = []

        for i in range(1, len(df)):
            o = df["open"][i]
            c = df["close"][i]
            h = df["high"][i]
            l = df["low"][i]
            p_o_c.append(abs(o-c)/c)
            p_h_l.append(abs(h - l) / l)


        p1 = np.array(p_o_c)
        p2 = np.array(p_h_l)

        #print((p1 > 1).sum())
        #print((p2 > 1).sum())
        p_sum1 = (p1 > 0.5).sum()
        p_sum2 = (p1 > 0.5).sum()
        if p_sum1:
            print(f"{secCode} : {p_sum1} : {p_sum2}")


    except:
        print("Error with ticker: ", secCode)

