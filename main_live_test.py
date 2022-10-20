# git clone https://github.com/cia76/QuikPy
# git clone https://github.com/cia76/BackTraderQuik

from datetime import datetime, time
import backtrader as bt
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
from numpy import floor

from collections import defaultdict  # для списков в словарях


class LimitCancel(bt.Strategy):
    """
    Выставляем заявку на покупку на n% ниже цены закрытия
    Если за 1 бар заявка не срабатывает, то закрываем ее
    Если срабатывает, то закрываем позицию. Неважно, с прибылью или убытком
    """
    params = (  # Параметры торговой системы
        ('LimitPct', 3),    # Заявка на покупку на n% ниже цены закрытия
        ('all_step', 0),    # шаг цены
        ('all_lots', 0),    # лоты
        ('all_scale', 0),   # знаков после запятой
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        """Инициализация торговой системы"""
        self.isLive = False  # Сначала будут приходить исторические данные, затем перейдем в режим реальной торговли

        self.orders = defaultdict(list)     # ордера по тикерам

    def round_lots(self, ticker, fix_size=1):    # округление до лотов
        lot = self.p.all_lots[ticker]
        size = round(abs(fix_size) / lot) * lot
        return int(size)

    def round_step(self, val, decimal, step):  # округление до decimal после запятой
        # print("round_step: ", val, decimal, step)
        val = round(val / step) * step
        return floor((val * (10 ** decimal)) + 0.5) / (10 ** decimal)

    def next(self):
        """Получение следующего исторического/нового бара"""

        if not self.isLive:  # Если не в режиме реальной торговли
            return  # то выходим, дальше не продолжаем

        # if self.p.name != '':  # Если указали название торговой системы, то будем ждать прихода всех баров
        #     lastdatetimes = [bt.num2date(data.datetime[0]) for data in self.datas]  # Дата и время последнего бара каждого тикера
        #     if lastdatetimes.count(lastdatetimes[0]) != len(lastdatetimes):  # Если дата и время последних баров не идентичны
        #         return  # то еще не пришли все новые бары. Ждем дальше, выходим

        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
            ticker = data._dataname

            _close = data.close[0]  # текущий close
            _low = data.low[0]      # текущий low
            _high = data.high[0]    # текущий high
            _open = data.open[0]    # текущий open

            self.log(f'{ticker} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.{self.p.all_scale[ticker]}f}, High={data.high[0]:.{self.p.all_scale[ticker]}f}, Low={data.low[0]:.{self.p.all_scale[ticker]}f}, Close={data.close[0]:.{self.p.all_scale[ticker]}f}, Volume={data.volume[0]:.0f}',
                bt.num2date(data.datetime[0]))

            print(self.orders)

            if self.orders[ticker] and self.orders[ticker].status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
                return  # то ждем исполнения, выходим, дальше не продолжаем
            if not self.position:  # Если позиции нет
                if self.orders[ticker] and self.orders[ticker].status == bt.Order.Accepted:  # Если заявка не исполнена (принята брокером)
                    self.cancel(self.orders[ticker])  # то снимаем ее

                limitPrice = _close * (1 - self.p.LimitPct / 100)  # На n% ниже цены закрытия
                limitPrice = self.round_step(limitPrice, self.p.all_scale[ticker], self.p.all_step[ticker])

                print(f"{ticker} - На {self.p.LimitPct}% ниже {_close} == {limitPrice}")

                size = 1 * self.p.all_lots[ticker]
                # if ticker == "TQBR.SBER":
                #     limitPrice = 114.00
                #     self.orders[ticker] = self.buy(data, exectype=bt.Order.Limit, price=limitPrice, size=size)  # Лимитная заявка на покупку
                # if ticker == "TQBR.VTBR":
                #     limitPrice = 0.015755
                #     self.orders[ticker] = self.buy(data, exectype=bt.Order.Limit, price=limitPrice, size=size)  # Лимитная заявка на покупку

                self.orders[ticker] = self.buy(data, exectype=bt.Order.Limit, price=limitPrice, size=size)  # Лимитная заявка на покупку

            else:  # Если позиция есть
                self.orders[ticker] = self.close()  # Заявка на закрытие позиции по рыночной цене

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(dataStatus)  # Не можем вывести в лог, т.к. первый статус DELAYED получаем до первого бара (и его даты)
        self.isLive = dataStatus == 'LIVE'  # Режим реальной торговли

    def notify_order(self, order):
        """Изменение статуса заявки"""
        ticker = order.data._name

        if order.status in (bt.Order.Created, bt.Order.Submitted, bt.Order.Accepted):  # Если заявка создана, отправлена брокеру, принята брокером (не исполнена)
            self.log(f'Alive Status: {order.getstatusname()}. TransId={order.ref}')
        elif order.status in (bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected, bt.Order.Expired):  # Если заявка отменена, нет средств, заявка отклонена брокером, снята по времени (снята)
            self.log(f'Cancel Status: {order.getstatusname()}. TransId={order.ref}')
        elif order.status == bt.Order.Partial:  # Если заявка частично исполнена
            self.log(f'Part Status: {order.getstatusname()}. TransId={order.ref}')
        elif order.status == bt.Order.Completed:  # Если заявка полностью исполнена
            if order.isbuy():  # Заявка на покупку
                self.log(f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():  # Заявка на продажу
                self.log(f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            self.orders[ticker] = None  # Сбрасываем заявку на вход в позицию

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if trade.isclosed:  # Если позиция закрыта
            self.log(f'Trade Profit, Gross={trade.pnl:.2f}, NET={trade.pnlcomm:.2f}')


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    # open:
    # clientCode = 'XXX'  # Код клиента (присваивается брокером)
    # firmId = 'MC0139600000'  # Код фирмы (присваивается брокером) # Счет L01-00000F00
    # tradeAccountId = 'L01-00000F00'

    # finam:
    clientCode = '593458R8NYF'  # Код клиента (присваивается брокером)
    ClientCodeForOrders = 'FZQU251223A'  # Код клиента (присваивается брокером) # номер терминала @
    firmId = 'MC0061900000'  # Код фирмы (присваивается брокером) # Счет L01+00000F00
    tradeAccountId = 'L01+00000F00'

    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)

    broker = store.getbroker(use_positions=False, ClientCode=clientCode, ClientCodeForOrders=ClientCodeForOrders,
                             FirmId=firmId, TradeAccountId=tradeAccountId, LimitKind=2, CurrencyCode='SUR',
                             IsFutures=False)  # Брокер со счетом фондового рынка РФ

    cerebro = bt.Cerebro()  # Инициируем "движок" BackTrader
    cerebro.setbroker(broker)  # Устанавливаем брокера

    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK

    # cerebro.broker.setcash(10000)
    # cerebro.broker.setcommission(commission=0.0015)

    symbols = ('TQBR.SBER', 'TQBR.VTBR',)  # Кортеж тикеров

    all_lots = {}
    all_step = {}
    all_scale = {}

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
        all_step[ticker] = securityInfo['min_price_step']
        all_scale[ticker] = securityInfo['scale']

    print("lot_size: ", all_lots)
    print("min_price_step: ", all_step)
    print("all_scale: ", all_scale)

    # Добавляем торговую систему с лимитным входом в n%
    cerebro.addstrategy(LimitCancel, LimitPct=3, all_step=all_step, all_lots=all_lots, all_scale=all_scale)

    for ticker in symbols:
        data = store.getdata(dataname=ticker, timeframe=bt.TimeFrame.Minutes, compression=1,
                             fromdate=datetime(2022, 10, 20), sessionstart=time(7, 0),
                             LiveBars=True)  # Исторические и новые минутные бары за все время
        cerebro.adddata(data)  # Добавляем данные

    # cerebro.addsizer(bt.sizers.FixedSize, stake=10000)  # Кол-во акций для покупки/продажи
    cerebro.run()  # Запуск торговой системы
