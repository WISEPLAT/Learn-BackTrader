from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
import Strategy2_FibonacciPivotPoint as ts  # Торговые системы

import functions

if __name__ == '__main__':  # Точка входа при запуске этого скрипта

    symbols = ('TQBR.AFKS', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH', 'TQBR.IRAO', 'TQBR.SIBN',)  # Кортеж тикеров        # 6 117 945.72  15min
    symbols = ('TQBR.AFKS', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH', 'TQBR.IRAO', 'TQBR.RTKM',)  # Кортеж тикеров        # 4 277 796.41  D1
    symbols = ('TQBR.AFKS', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH', )  # Кортеж тикеров                                 # 2 838 642.35  D1
    symbols = ('TQBR.GAZP', 'TQBR.AFKS',)  # Кортеж тикеров
    symbols = ('TQBR.GAZP', )  # Кортеж тикеров
    symbols = ('TQBR.GAZP', 'TQBR.AFKS',)  # Кортеж тикеров
    symbols = ('TQBR.AFKS', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH', )  # Кортеж тикеров
    symbols = ('TQBR.GAZP', 'TQBR.AFKS', )  # Кортеж тикеров
    #symbols = ('TQBR.GAZP',)  # Кортеж тикеров


    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    cerebro = Cerebro()  # Инициируем "движок" BackTrader # по дефолту берет максимум
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)

    syminfo_mintick, f_decimal, lots = functions.get_info_about_paper(qpProvider, symbols, show_log=True)

    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Minutes, compression=60, fromdate=datetime(2000, 1, 1), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data)  # Добавляем данные
        cerebro.resampledata(data, timeframe=TimeFrame.Days, compression=7).plotinfo.plot = False
        #cerebro.resampledata(data, timeframe=TimeFrame.Minutes, compression=1440).plotinfo.plot = False
        #cerebro.resampledata(data, timeframe=TimeFrame.Minutes, compression=120).plotinfo.plot = False
    # cerebro.addstrategy(ts.TestStrategy01, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    # cerebro.addstrategy(ts.TestStrategy01, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    cerebro.addstrategy(ts.TestStrategy04, name="All Tickers", lots=lots)  # Добавляем торговую систему по всем тикерам

    strategy_runs = cerebro.run()  # Запуск торговой системы
    # cerebro.plot()  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)

    print('Стоимость портфеля: %.2f' % cerebro.broker.getvalue())
    print('Свободные средства: %.2f' % cerebro.broker.get_cash())

    my_log = strategy_runs[0].my_logs
    functions.export_log_to_csv(my_log=my_log, export_dir="logs")

    qpProvider.CloseConnectionAndThread()  # Закрытие соединения с Quik

    cerebro.plot(style='candle')  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
