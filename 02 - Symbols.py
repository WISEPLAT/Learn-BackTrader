from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
import Strategy as ts  # Торговые системы
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)
    #cerebro.broker.set_fundmode(True)  # the default is 100

    symbols = ('TQBR.SBER', 'TQBR.GAZP', 'TQBR.LKOH', 'TQBR.GMKN',)  # Кортеж тикеров

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
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Minutes, compression=15, fromdate=datetime(2021, 10, 4), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data, name=symbol)  # Добавляем данные
    #cerebro.addstrategy(ts.TestStrategy01, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    #cerebro.addstrategy(ts.TestStrategy01, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    cerebro.addstrategy(ts.TestStrategy01, name="All Tickers", lots=all_lots)  # Добавляем торговую систему по всем тикерам

    cerebro.run()  # Запуск торговой системы

    print('Стоимость портфеля: %.2f' % cerebro.broker.getvalue())
    print('Свободные средства: %.2f' % cerebro.broker.get_cash())

    cerebro.plot(style='candle')  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)

    # Выход
    qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
