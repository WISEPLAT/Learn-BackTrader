# pip install opencv-python mysqlclient MetaTrader5 pandas pytz
# git clone https://github.com/WISEPLAT/SharesDataLoader
# pip install requests apimoex

import datetime
from SharesDataLoader.DataMetatrader import DataMetatrader

import requests
import apimoex
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    request_url = ('https://iss.moex.com/iss/engines/stock/'
                   'markets/shares/boards/TQBR/securities.json')
    arguments = {'securities.columns': ('SECID,'
                                        'REGNUMBER,'
                                        'LOTSIZE,'
                                        'SHORTNAME')}
    with requests.Session() as session:
        iss = apimoex.ISSClient(session, request_url, arguments)
        data = iss.get()
        df = pd.DataFrame(data['securities'])
    print(df)
    #df.info()
    df.reset_index(inplace=True)
    classSecurities = df['SECID'].to_numpy()
    print(classSecurities)

    exit(1)

    # получим данные по завтрашний день
    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)
    print(utc_till)

    load_data = DataMetatrader()
    load_data.ConnectToMetatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")

    # all 268
    classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'AVAN', 'BANE',
     'BANEP', 'BELU', 'BISV', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CIAN',
     'CNTL', 'CNTLP', 'DERZP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT', 'ELTZ', 'EM44', 'ENPG', 'ENRU', 'ETLN',
     'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GEMC',
     'GLTR', 'GMKN', 'GTRK', 'GTSS', 'HHRU', 'HIMC', 'HIMCP', 'HMSG', 'HYDR', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRGZ',
     'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ',
     'KMTZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KROT', 'KROTP', 'KRSB', 'KRSBP', 'KSGR', 'KTSB', 'KTSBP',
     'KUBE', 'KUZB', 'KZMS', 'KZOS', 'KZOSP', 'LENT', 'LIFE', 'LKOH', 'LNTA', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP',
     'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MFGS', 'MFGSP', 'MFON', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB',
     'MISBP', 'MOEX', 'MORI', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS',
     'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB',
     'NNSBP', 'NPOF', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP',
     'POGR', 'POLY', 'POSI', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM', 'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO',
     'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RUSP',
     'RZSB', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN', 'SFTL', 'SGZH', 'SIBN', 'SLEN', 'SMLT',
     'SNGS', 'SNGSP', 'SPBE', 'STSB', 'STSBP', 'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB',
     'TGKBP', 'TGKD', 'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRCN', 'TRFM', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS',
     'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKA', 'URKZ', 'USBN', 'UTAR', 'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP',
     'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG', 'YKEN', 'YKENP', 'YNDX',
     'YRSB', 'YRSBP', 'ZILL', 'ZVEZ']

    # error with: classSecurities = ['CIAN', 'DERZP' ,'EM44' ,'GTSS' ,'HMSG', 'KMTZ', 'KSGR', 'LENT', 'NPOF', 'POSI', 'RENI', 'SFTL', 'SPBE', 'TRFM', 'VEON-RX', 'YRSB']

    # ok
    classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'AVAN', 'BANE',
     'BANEP', 'BELU', 'BISV', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK',
     'CNTL', 'CNTLP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT', 'ELTZ', 'ENPG', 'ENRU', 'ETLN',
     'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GEMC',
     'GLTR', 'GMKN', 'GTRK', 'HHRU', 'HIMC', 'HIMCP', 'HYDR', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRGZ',
     'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ',
     'KOGK', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KROT', 'KROTP', 'KRSB', 'KRSBP', 'KTSB', 'KTSBP',
     'KUBE', 'KUZB', 'KZMS', 'KZOS', 'KZOSP', 'LIFE', 'LKOH', 'LNTA', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP',
     'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MFGS', 'MFGSP', 'MFON', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB',
     'MISBP', 'MOEX', 'MORI', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS',
     'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB',
     'NNSBP', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP',
     'POGR', 'POLY', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM', 'RDRB', 'RGSS', 'RKKE', 'RNFT', 'ROLO',
     'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RUSP',
     'RZSB', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN', 'SGZH', 'SIBN', 'SLEN', 'SMLT',
     'SNGS', 'SNGSP', 'STSB', 'STSBP', 'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB',
     'TGKBP', 'TGKD', 'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRCN', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS',
     'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKA', 'URKZ', 'USBN', 'UTAR', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP',
     'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG', 'YKEN', 'YKENP', 'YNDX',
     'YRSBP', 'ZILL', 'ZVEZ']

    for ticker in classSecurities:
        prefix = classCode + '.'
        timeframe = "W1"
        how_many_bars = 50000

        try:
            # create CSV file
            load_data.ExportToCsvFromMetatrader(ticket=ticker, timeframe=timeframe, utc_till=utc_till,
                                                how_many_bars=how_many_bars, remove_last_bar=False, export_dir="csv",
                                                prefix=prefix, upper_heading=False)
            print(ticker, end=" ")
        except:
            print("\n Error with ticker: ", ticker)

    print("\nDone.")
    load_data.DisconnectFromMetatrader5()
