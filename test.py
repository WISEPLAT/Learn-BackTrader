# pip install pandas

import pandas as pd
import os

timeFrame = "D1"
classCode = "TQBR"
csv_folder_quik = "csv_quik"
csv_folder_meta = "csv_meta"
csv_folder_export = "csv_ok"

if not os.path.exists(csv_folder_export): os.makedirs(csv_folder_export)

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

# classSecurities = ['GAZP']

classSecurities_for_quik = []
classSecurities_for_meta = []

for secCode in classSecurities:
    file_quik = f'{csv_folder_quik}\\{classCode}.{secCode}_{timeFrame}.csv'
    file_meta = f'{csv_folder_meta}\\{classCode}.{secCode}_{timeFrame}.csv'
    file_export = f'{csv_folder_export}\\{classCode}.{secCode}_{timeFrame}.csv'

    isFileExists_quik = os.path.isfile(file_quik)  # Существует ли файл
    if not isFileExists_quik:  # Если файл не существует
        print(f'Файл {file_quik} не найден')

    isFileExists_meta = os.path.isfile(file_meta)  # Существует ли файл
    if not isFileExists_meta:  # Если файл не существует
        print(f'Файл {file_meta} не найден')

    try:
        df_quik = pd.read_csv(file_quik, sep=',')  # Считываем файл в DataFrame
        df_meta = pd.read_csv(file_meta, sep=',')  # Считываем файл в DataFrame
        df_quik["datetime"] = pd.to_datetime(df_quik["datetime"])
        df_meta["datetime"] = pd.to_datetime(df_meta["datetime"])
        #print(df_quik, df_meta, "\n----------------------------------------------------------------------------------------")

        date_quik = df_quik["datetime"][0]
        date_meta = df_meta["datetime"][0]
        if date_quik <= date_meta:
            classSecurities_for_quik.append(secCode)
            os.system(f"copy {file_quik} {file_export}")
        else:
            classSecurities_for_meta.append(secCode)
            os.system(f"copy {file_meta} {file_export}")
        print(f"ticker: {secCode}, quik: {date_quik}, meta: {date_meta}")

    except:
        print("Error with ticker: ", secCode)
        if isFileExists_quik:
            classSecurities_for_quik.append(secCode)
            os.system(f"copy {file_quik} {file_export}")
        if isFileExists_meta:
            classSecurities_for_meta.append(secCode)
            os.system(f"copy {file_meta} {file_export}")

print(f"Total tickers from quik: {len(classSecurities_for_quik)}", classSecurities_for_quik)
print(f"Total tickers from meta: {len(classSecurities_for_meta)}", classSecurities_for_meta)
