from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
import Strategy2_FibonacciPivotPoint_v2 as ts  # Торговые системы

import matplotlib
import matplotlib.pyplot as plt

def default_colors(color='white', size=6, background="#101622", grid="0.4"):
    matplotlib.use('Agg')
    plt.style.use('fivethirtyeight')
    plt.rcParams["figure.figsize"] = (10, 6)

    plt.rcParams['lines.linewidth'] = 0.5
    plt.rcParams['lines.color'] = "0.5"

    plt.rcParams["font.size"] = size
    plt.rcParams['axes.labelsize'] = size
    plt.rcParams['ytick.labelsize'] = size
    plt.rcParams['xtick.labelsize'] = size

    #plt.rcParams['text.color'] = color
    plt.rcParams['text.color'] = "gray"
    plt.rcParams['axes.labelcolor'] = color
    plt.rcParams['xtick.color'] = color
    plt.rcParams['ytick.color'] = color


    plt.rcParams['axes.grid.axis'] = 'both'
    plt.rcParams['grid.linewidth'] = 0.1
    plt.rcParams['grid.color'] = grid
    plt.rcParams['axes.edgecolor']="0.2"
    plt.rcParams['axes.linewidth'] = 0      # "0.5"

    plt.rcParams['figure.facecolor'] = background
    plt.rcParams['axes.facecolor'] = background

    plt.rcParams["savefig.dpi"] = 120
    dpi = plt.rcParams["savefig.dpi"]
    width = 700
    height = 1200
    plt.rcParams['figure.figsize'] = height / dpi, width / dpi
    plt.rcParams["savefig.facecolor"] = background
    plt.rcParams["savefig.edgecolor"] = background


    plt.rcParams['legend.fontsize'] = size + 2
    plt.rcParams['legend.title_fontsize'] = size + 2
    plt.rcParams['legend.labelspacing'] = 0.25
    plt.rcParams['image.cmap'] = 'tab10'

    plt.ioff()

default_colors()

## https://community.backtrader.com/topic/2640/how-to-output-plots-in-a-dark-theme/3
# https://community.backtrader.com/topic/3286/dark-night-mode-for-chart/5

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
    symbols = ('TQBR.GAZP',)  # Кортеж тикеров


    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    cerebro = Cerebro()  # Инициируем "движок" BackTrader # по дефолту берет максимум
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)

    syminfo_mintick, f_decimal, lots = functions.get_info_about_paper(qpProvider, symbols, show_log=True)

    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Minutes, compression=15, fromdate=datetime(2000, 1, 1), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data)  # Добавляем данные
        cerebro.resampledata(data, timeframe=TimeFrame.Days, compression=1).plotinfo.plot = False
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

    cerebro.plot(
        #loc='grey',  # changes color for 'line on close' plot otherwise it will plot black on black
        grid=False,  # the default gridlines didn't look good w/ dark background
        style='candle',
        loc='yellow',
        locbg='red',
        locbgother='darkred',)  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
