import os.path
import pandas as pd
import numpy as np

timeFrame = "D1"
classCode = "TQBR"
csv_folder_find_anomalies = "csv"

# ok
classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB',
                       'AVAN', 'BANE', 'BANEP', 'BELU', 'BISV', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM',
                       'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CIAN', 'CNTL', 'CNTLP', 'DERZP', 'DIOD', 'DSKY', 'DVEC', 'DZRD',
                       'DZRDP', 'EELT', 'ELTZ', 'EM44', 'ENPG', 'ENRU', 'ETLN', 'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT',
                       'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GEMC', 'GLTR', 'GMKN', 'GTRK',
                       'GTSS', 'HHRU', 'HIMC', 'HIMCP', 'HMSG', 'HYDR', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRGZ', 'IRKT',
                       'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB',
                       'KMAZ', 'KMEZ', 'KMTZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KROT', 'KROTP', 'KRSB',
                       'KRSBP', 'KSGR', 'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZMS', 'KZOS', 'KZOSP', 'LENT', 'LIFE',
                       'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN',
                       'MDMG', 'MFGS', 'MFGSP', 'MFON', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MOEX',
                       'MORI', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS',
                       'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK',
                       'NMTP', 'NNSB', 'NNSBP', 'NPOF', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR',
                       'PIKK', 'PLZL', 'PMSB', 'PMSBP', 'POGR', 'POLY', 'POSI', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM',
                       'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ',
                       'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RUSP', 'RZSB', 'SAGO', 'SAGOP',
                       'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN', 'SFTL', 'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS',
                       'SNGSP', 'SPBE', 'STSB', 'STSBP', 'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG',
                       'TGKA', 'TGKB', 'TGKBP', 'TGKD', 'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRCN', 'TRFM',
                       'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS', 'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKA', 'URKZ', 'USBN',
                       'UTAR', 'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP', 'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO',
                       'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG', 'YKEN', 'YKENP', 'YNDX', 'YRSB', 'YRSBP',
                       'ZILL', 'ZVEZ']

#classSecurities = ['IRAO', 'RTKM', 'TRMK']
#classSecurities = ['TRMK']



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for secCode in classSecurities:
        file = f"{csv_folder_find_anomalies}\\{classCode}.{secCode}_{timeFrame}.csv"

        isFileExist = os.path.isfile(file)
        if not isFileExist:
            print(f"Файл {file} не найден")

        try:
            df = pd.read_csv(file, sep=",", index_col="datetime")
            # print(df)

            # df_p = df.pct_change()

            p_o_c = []
            p_h_l = []

            for i in range(1, len(df)):
                o = df["open"][i]
                h = df["high"][i]
                l = df["low"][i]
                c = df["close"][i]
                v = df["volume"][i]
                p_o_c.append(abs(o-c)/c)
                p_h_l.append(abs(h - l) / h)

            p1 = np.array(p_o_c)
            p2 = np.array(p_h_l)

            #print(p_o_c)

            p_sum1 = (p1 > 0.5).sum()
            p_sum2 = (p2 > 0.5).sum()

            if p_sum1:
                print(f"{secCode} : {p_sum1} : {p_sum2}")

        except:
            print("\n Error with ticker: ", secCode)

    print("\nDone.")