from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
import Strategy2_ROC_KC_UpDownTrend as ts  # Торговые системы
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp

import functions

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)
    #cerebro.broker.set_fundmode(True)  # the default is 100

    symbols = ('TQBR.AFKS', 'TQBR.AFLT', 'TQBR.ALRS', 'TQBR.CBOM', 'TQBR.CHMF', 'TQBR.DSKY', 'TQBR.ENPG', 'TQBR.FEES',
               'TQBR.FIVE', 'TQBR.FIXP', 'TQBR.FLOT', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.HHRU', 'TQBR.HYDR', 'TQBR.LKOH',
               'TQBR.MAGN', 'TQBR.MGNT', 'TQBR.MOEX', 'TQBR.MTSS', 'TQBR.NLMK', 'TQBR.NVTK', 'TQBR.OZON', 'TQBR.PHOR',
               'TQBR.PIKK', 'TQBR.PLZL', 'TQBR.POLY', 'TQBR.ROSN', 'TQBR.RTKM', 'TQBR.SBER', 'TQBR.SNGS', 'TQBR.TATN',
               'TQBR.TCSG', 'TQBR.VKCO', 'TQBR.VTBR', 'TQBR.TATNP', 'TQBR.TRNFP', 'TQBR.SBERP', 'TQBR.SNGSP',
               'TQBR.AKRN', 'TQBR.SIBN', 'TQBR.LSRG', 'TQBR.RASP', 'TQBR.BSPB', 'TQBR.MTLRP', 'TQBR.RTKMP',)
    symbols = ('TQBR.SBER', 'TQBR.GAZP', 'TQBR.LKOH', 'TQBR.GMKN',)  # Кортеж тикеров
    symbols = ('TQBR.SBER', 'TQBR.LKOH', )  # Кортеж тикеров
    symbols = ('TQBR.SBER', )

    all_lots = {}

    for ticker in symbols:
        # Данные тикера
        part_symbol = ticker.split(".")
        classCode = part_symbol[0]  # Класс тикера
        secCode = part_symbol[1]  # Тикер

        # Данные тикера
        securityInfo = qpProvider.GetSecurityInfo(classCode, secCode)["data"]
        print(f'Информация о тикере {classCode}.{secCode} ({securityInfo["short_name"]}):')
        print('Валюта:', securityInfo['face_unit'])
        print('Кол-во десятичных знаков:', securityInfo['scale'])
        print('Лот:', securityInfo['lot_size'])
        print('Шаг цены:', securityInfo['min_price_step'])

        all_lots[ticker] = securityInfo['lot_size']

    print(all_lots)


    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)
    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Days, compression=1, fromdate=datetime(2001, 10, 4), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data, name=symbol)  # Добавляем данные
    #cerebro.addstrategy(ts.TestStrategy01, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    #cerebro.addstrategy(ts.TestStrategy01, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    cerebro.addstrategy(ts.TestStrategy01, name="All Tickers", lots=all_lots)  # Добавляем торговую систему по всем тикерам

    strategy_runs = cerebro.run()  # Запуск торговой системы

    print('Стоимость портфеля: %.2f' % cerebro.broker.getvalue())
    print('Свободные средства: %.2f' % cerebro.broker.get_cash())

    my_log = strategy_runs[0].my_logs
    functions.export_log_to_csv(my_log=my_log, export_dir="logs")

    qpProvider.CloseConnectionAndThread()  # Закрытие соединения с Quik

    cerebro.plot(style='candle')  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
