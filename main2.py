from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
import StrategySMA_EMA_3 as ts  # Торговые системы

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)

    symbols = ('TQBR.AFKS', 'TQBR.SBER', 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH', )  # Кортеж тикеров
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)
    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Days, compression=1, fromdate=datetime(2000, 1, 1), LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data)  # Добавляем данные
    # cerebro.addstrategy(ts.TestStrategy01, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    # cerebro.addstrategy(ts.TestStrategy01, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    cerebro.addstrategy(ts.TestStrategy01, name="All Tickers")  # Добавляем торговую систему по всем тикерам

    cerebro.run()  # Запуск торговой системы
    # cerebro.plot()  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)

    print('Стоимость портфеля: %.2f' % cerebro.broker.getvalue())
    print('Свободные средства: %.2f' % cerebro.broker.get_cash())

    cerebro.plot(style='candle')  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
