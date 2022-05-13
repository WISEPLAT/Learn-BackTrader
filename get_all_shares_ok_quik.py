# pip install opencv-python mysqlclient MetaTrader5 pandas pytz
# git clone https://github.com/WISEPLAT/SharesDataLoader

import datetime
from SharesDataLoader.DataQuik import DataQuik

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
from backtrader import Cerebro, TimeFrame

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # Классы
    classCode = "TQBR"
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK

    # получим данные по завтрашний день
    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)
    print(utc_till)

    load_data = DataQuik()

    # error with: classSecurities = ['BISV', 'DERZP', 'EM44', 'GAZC', 'GAZS', 'GAZT', 'GTSS', 'HIMC', 'KMTZ', 'KRKO', 'KSGR', 'KZMS', 'MFON', 'MORI', 'NPOF', 'RUSP', 'TRCN', 'TRFM', 'URKA']

    # ok
    classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'AVAN', 'BANE',
     'BANEP', 'BELU', 'BISV', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CIAN',
     'CNTL', 'CNTLP', 'DERZP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT', 'ELTZ', 'EM44', 'ENPG', 'ENRU', 'ETLN',
     'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GEMC',
     'GLTR', 'GMKN', 'GTRK', 'GTSS', 'HHRU', 'HIMC', 'HIMCP', 'HMSG', 'HYDR', 'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRGZ',
     'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ',
     'KMTZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KROT', 'KROTP', 'KRSB', 'KRSBP', 'KSGR', 'KTSB', 'KTSBP',
     'KUBE', 'KUZB', 'KZMS', 'KZOS', 'KZOSP', 'LENT', 'LIFE', 'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP', 'LSRG',
     'LVHK', 'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MFGS', 'MFGSP', 'MFON', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP',
     'MOEX', 'MORI', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT',
     'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB', 'NNSBP',
     'NPOF', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP', 'POGR',
     'POLY', 'POSI', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM', 'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB',
     'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RUSP', 'RZSB',
     'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN', 'SFTL', 'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS',
     'SNGSP', 'SPBE', 'STSB', 'STSBP', 'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB',
     'TGKBP', 'TGKD', 'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRCN', 'TRFM', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS',
     'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKA', 'URKZ', 'USBN', 'UTAR', 'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP',
     'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG', 'YKEN', 'YKENP', 'YNDX',
     'YRSB', 'YRSBP', 'ZILL', 'ZVEZ']

    prefix = classCode + '.'
    timeframe = "W1"
    how_many_bars = 70000

    classSecurities_ok = []

    for ticker in classSecurities:
        try:
            _ticker = classCode + '.' + ticker
            #data = load_data.GetShareDataFromQuik(qpProvider, _ticker, timeframe, utc_till, how_many_bars, remove_last_bar=False, upper_heading=False)
            #print(data)
            load_data.ExportToCsvFromQuik(qpProvider, _ticker, timeframe, utc_till, how_many_bars, remove_last_bar=False, export_dir=f'csv_quik_{timeframe}', prefix='', upper_heading=False)
            # create CSV file
            # load_data.ExportToCsvFromMetatrader(ticker=ticker, timeframe=timeframe, utc_till=utc_till,
            #                                     how_many_bars=how_many_bars, remove_last_bar=False,
            #                                     export_dir="csv_test_mt5", prefix=prefix, upper_heading=False)
            print(ticker, end=" ")
            classSecurities_ok.append(ticker)
        except:
            print("\n Error with ticker: ", ticker)

    print("\nDone.\n", classSecurities_ok)

    qpProvider.CloseConnectionAndThread()  # Закрытие соединения с Quik
