from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
import Strategy3 as ts  # Торговые системы

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    symbols = ('TQBR.GAZP', ) #'TQBR.VTBR', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.LKOH', 'TQBR.GMKN',)  # Кортеж тикеров
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)
    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Days, compression=1,
                             fromdate=datetime(2000, 1, 1), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data)  # Добавляем данные
    #cerebro.addstrategy(ts.PrintStatusAndBars, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    #cerebro.addstrategy(ts.PrintStatusAndBars, name="One Ticker", symbols=('TQBR.GAZP',))  # Добавляем торговую систему по одному тикеру
    #cerebro.addstrategy(ts.PrintStatusAndBars, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    cerebro.addstrategy(ts.PrintStatusAndBars, name="All Tickers")  # Добавляем торговую систему по всем тикерам

    #cerebro.run()  # Запуск торговой системы
    #cerebro.plot()  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)

    # finam:
    clientCode = '593458R8NYF'  # Код клиента (присваивается брокером)
    clientCodeTerminal = 'FZQU251223A'  # Код клиента (присваивается брокером) # номер терминала @
    firmId = 'MC0061900000'  # Код фирмы (присваивается брокером) # Счет L01+00000F00
    tradeAccountId = 'L01+00000F00'

    limitKind = 2

    some_data = store.GetPositions(clientCode, firmId, limitKind, True)
    print(some_data)

    print("positions: ", store.positions)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
