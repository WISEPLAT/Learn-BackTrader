# pip install opencv-python mysqlclient MetaTrader5 pandas pytz
# git clone https://github.com/WISEPLAT/SharesDataLoader

import datetime
from SharesDataLoader.DataMetatrader import DataMetatrader

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # Классы
    classCode = "TQBR"
    classInfo = qpProvider.GetClassInfo(classCode)['data']  # Информация о классе
    print(f'- Класс {classCode} ({classInfo["name"]}), Тикеров {classInfo["nsecs"]}')
    # Инструменты. Если выводить на экран, то занимают много места. Поэтому, закомментировали
    classSecurities = qpProvider.GetClassSecurities(classCode)['data'][:-1].split(
        ',')  # Список инструментов класса. Удаляем последнюю запятую, разбиваем значения по запятой
    print(f'  - Тикеры ({classSecurities})')

    # получим данные по завтрашний день
    utc_till = datetime.datetime.now() + datetime.timedelta(days=1)
    print(utc_till)

    print("Закомментируйте эту строку для запуска загрузки!"); exit(1)

    load_data = DataMetatrader()
    load_data.ConnectToMetatrader5(path=f"C:\Program Files\FINAM MetaTrader 5\terminal64.exe")

    # all 267
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

    # error with: classSecurities = ['CIAN', 'DERZP' ,'EM44' ,'GTSS' ,'HMSG', 'KMTZ', 'KSGR', 'LENT', 'NPOF', 'POSI', 'RENI', 'SFTL', 'SPBE', 'TRFM', 'VEON-RX', 'YRSB']

    # ok
    classSecurities = ['ABRD', 'ACKO', 'AFKS', 'AFLT', 'AGRO', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB',
                       'AVAN', 'BANE', 'BANEP', 'BELU', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ',
                       'CHKZ', 'CHMF', 'CHMK', 'CNTL', 'CNTLP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT',
                       'ELTZ', 'ENPG', 'ENRU', 'ETLN', 'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZP',
                       'GCHE', 'GEMA', 'GEMC', 'GLTR', 'GMKN', 'GTRK', 'HHRU', 'HIMCP', 'HYDR', 'IGST', 'IGSTP',
                       'INGR', 'IRAO', 'IRGZ', 'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE',
                       'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KMAZ', 'KMEZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKOP', 'KROT',
                       'KROTP', 'KRSB', 'KRSBP', 'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZOS', 'KZOSP', 'LIFE',
                       'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN',
                       'MDMG', 'MFGS', 'MFGSP', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MOEX', 'MRKC',
                       'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT', 'MTLR',
                       'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB',
                       'NNSBP', 'NSVZ', 'NVTK', 'OGKB', 'OKEY', 'OMZZP', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB',
                       'PMSBP', 'POGR', 'POLY', 'PRMB', 'QIWI', 'RASP', 'RAVN', 'RBCM', 'RDRB', 'RGSS',
                       'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB',
                       'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RZSB', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SBER', 'SBERP',
                       'SELG', 'SFIN', 'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'STSB', 'STSBP',
                       'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TCSG', 'TGKA', 'TGKB', 'TGKBP', 'TGKD',
                       'TGKDP', 'TGKN', 'TNSE', 'TORS', 'TORSP', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS', 'UKUZ',
                       'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP',
                       'VKCO', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'YAKG',
                       'YKEN', 'YKENP', 'YNDX', 'YRSBP', 'ZILL', 'ZVEZ']

    # classSecurities = ['ROSN', 'SBER', 'GAZP', 'VTBR']
    #
    # classSecurities = ['IRAO', 'RTKM', 'TRMK']

    prefix = classCode + '.'
    timeframe = "MN1"
    how_many_bars = 70000

    for ticker in classSecurities:
        try:
            # create CSV file
            load_data.ExportToCsvFromMetatrader(ticker=ticker, timeframe=timeframe, utc_till=utc_till,
                                                how_many_bars=how_many_bars, remove_last_bar=False,
                                                export_dir=f"csv_meta_{timeframe}", prefix=prefix, upper_heading=False)
            print(ticker, end=" ")
        except:
            print("\n Error with ticker: ", ticker)

    print("\nDone.")
    load_data.DisconnectFromMetatrader5()

    qpProvider.CloseConnectionAndThread()  # Закрытие соединения с Quik
