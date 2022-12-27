# git clone https://github.com/cia76/QuikPy
# git clone https://github.com/cia76/BackTraderQuik

from datetime import datetime
from backtrader import Cerebro, TimeFrame, Strategy, feeds
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
import backtrader as bt
import pandas as pd


class PrintStatusAndBars(Strategy):
    """
    - Отображает статус подключения
    - При приходе нового бара отображает его цены/объем
    - Отображает статус перехода к новым барам
    """
    params = (  # Параметры торговой системы
        ('name', ''),  # Название торговой системы
        ('symbols', ''),  # Список торгуемых тикеров. По умолчанию торгуем все тикеры
    )

    def log(self, data, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(data.datetime[0]) if dt is None else dt  # Заданная дата или дата последнего бара первого тикера ТС
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        """Инициализация торговой системы"""
        self.isLive = False  # Сначала будут приходить исторические данные

    def next(self):
        """
        Приход нового бара тикера
        """
        # if self.p.name != '':  # Если указали название торговой системы, то будем ждать прихода всех баров
        #     lastdatetimes = [bt.num2date(data.datetime[0]) for data in self.datas]  # Дата и время последнего бара каждого тикера
        #     if lastdatetimes.count(lastdatetimes[0]) != len(lastdatetimes):  # Если дата и время последних баров не идентичны
        #         return  # то еще не пришли все новые бары. Ждем дальше, выходим
        #     print(self.p.name)
        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
            if self.p.symbols == '' or data._dataname in self.p.symbols:  # Если торгуем все тикеры или данный тикер
                self.log(data, f'{data._name} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                     bt.num2date(data.datetime[0]))
                # if data._name == "_m60":
                #     print("M60")
                #     print("D1", bt.num2date(self.datas[1].datetime[0]))

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статсуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(f'{data._dataname} - {dataStatus}')  # Статус приходит для каждого тикера отдельно
        self.isLive = dataStatus == 'LIVE'  # В Live режим переходим после перехода первого тикера


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    # Несколько временнЫх интервалов, прямая загрузка
    symbol = 'TQBR.GAZP'
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)

    data = store.getdata(dataname=symbol, timeframe=TimeFrame.Minutes, compression=60, fromdate=datetime(2022, 12, 15),
                         name="_m60",
                         LiveBars=True)  # Исторические данные по малому временнОму интервалу (должен идти первым)
    # data = pd.read_csv("TQBR.SBER_H1.csv", sep=",", index_col='datetime')  # Считываем файл в DataFrame
    # data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M')  # Переводим индекс в формат datetime
    # data = feeds.PandasData(dataname=data, name="_m60")
    cerebro.adddata(data)  # Добавляем данные

    # cerebro.resampledata(data, timeframe=TimeFrame.Days, compression=1).plotinfo.plot = False

    data = store.getdata(dataname=symbol, timeframe=TimeFrame.Days, compression=1, fromdate=datetime(2022, 12, 15),
                         name="_d1",
                         LiveBars=True)  # Исторические данные по большому временнОму интервалу
    # data = pd.read_csv("TQBR.SBER_D1.csv", sep=",", index_col='datetime')  # Считываем файл в DataFrame
    # data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M')  # Переводим индекс в формат datetime
    # data = feeds.PandasData(dataname=data, name="_d1")
    cerebro.adddata(data)  # Добавляем данные

    cerebro.addstrategy(PrintStatusAndBars)  # Добавляем торговую систему

    cerebro.run()  # Запуск торговой системы
    # cerebro.plot()  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
