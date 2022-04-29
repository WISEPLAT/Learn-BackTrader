from datetime import datetime, time
import backtrader as bt
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp

import functions


class LimitCancel(bt.Strategy):
    """
    Выставляем заявку на покупку на n% ниже цены закрытия
    Если за 1 бар заявка не срабатывает, то закрываем ее
    Если срабатывает, то закрываем позицию. Неважно, с прибылью или убытком
    """
    params = (  # Параметры торговой системы
        ('LimitPct', 2),  # Заявка на покупку на n% ниже цены закрытия
        ('Depo', 0),
        ('Lot', 0),
        ('Percent', 2),
    )

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def __init__(self):
        """Инициализация торговой системы"""
        self.isLive = False  # Сначала будут приходить исторические данные, затем перейдем в режим реальной торговли
        self.order = None  # Заявка на вход/выход из позиции

    def next(self):
        """Получение следующего исторического/нового бара"""
        print("close:", self.data.close[0])
        if not self.isLive:  # Если не в режиме реальной торговли
            return  # то выходим, дальше не продолжаем
        if self.order and self.order.status == bt.Order.Submitted:  # Если заявка не исполнена (отправлена брокеру)
            return  # то ждем исполнения, выходим, дальше не продолжаем
        if not self.position:  # Если позиции нет
            if self.order and self.order.status == bt.Order.Accepted:  # Если заявка не исполнена (принята брокером)
                self.cancel(self.order)  # то снимаем ее
            #limitPrice = self.data.close[0] * (1 - self.p.LimitPct / 100)  # На n% ниже цены закрытия
            limitPrice = 0.017075   # VTBR
            #limitPrice = 0.021075  # VTBR
            #limitPrice = 117.07     # SBER

            size, lots_can_buy = functions.calc_size(depo=self.p.Depo, lot=self.p.Lot, percent=self.p.Percent, ticker_price=limitPrice)
            print(size, lots_can_buy)
            # 126582.27848101266 12.658227848101266  => 126582 12
            # close: # 121.36 1000.0 1177.7 0.8491126772522714 8.491126772522714 10
            # close: 0.018605 # 1000.0 177.75 5.625879043600563 56258.79043600563 60000
            #exit(1) # for real trade please remove it )))

            self.order = self.buy(exectype=bt.Order.Limit, price=limitPrice, size=size)  # Лимитная заявка на покупку
            #self.order = self.sell(exectype=bt.Order.Limit, price=limitPrice, size=10000)  # Лимитная заявка на покупку
            print("Real trade: open position")
        else:  # Если позиция есть
            #self.order = self.close()  # Заявка на закрытие позиции по рыночной цене
            print("Real trade: close position")

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(dataStatus)  # Не можем вывести в лог, т.к. первый статус DELAYED получаем до первого бара (и его даты)
        self.isLive = dataStatus == 'LIVE'  # Режим реальной торговли

    def notify_order(self, order):
        """Изменение статуса заявки"""
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
            self.order = None  # Сбрасываем заявку на вход в позицию

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
    clientCodeTerminal = 'FZQU251223A'  # Код клиента (присваивается брокером) # номер терминала @
    firmId = 'MC0061900000'  # Код фирмы (присваивается брокером) # Счет L01+00000F00
    tradeAccountId = 'L01+00000F00'

    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # qpProvider = QuikPy(Host='<Ваш IP адрес>')  # Вызываем конструктор QuikPy с подключением к удаленному компьютеру с QUIK

    classCode = 'TQBR'  # Класс тикера
    secCode = 'VTBR'  # Тикер
    #secCode = 'SBER'  # Тикер

    limitKind = 2

    # Данные тикера
    securityInfo = qpProvider.GetSecurityInfo(classCode, secCode)["data"]
    print(f'Информация о тикере {classCode}.{secCode} ({securityInfo["short_name"]}):')
    print('Валюта:', securityInfo['face_unit'])
    print('Кол-во десятичных знаков:', securityInfo['scale'])
    print('Лот:', securityInfo['lot_size'])
    print('Шаг цены:', securityInfo['min_price_step'])

    lot = securityInfo['lot_size']

    # берем позиции по бумагам
    depoLimits = qpProvider.GetAllDepoLimits()['data']  # Все лимиты по бумагам (позиции по инструментам)
    # {'firmid': 'MC0061900000', 'openlimit': 0.0, 'currentlimit': 0.0, 'wa_position_price': 0.02011,
    # 'currentbal': 20000.0, 'limit_kind': 2, 'locked_buy_value': 0.0, 'locked_sell': 0.0, 'openbal': 20000.0,
    # 'locked_sell_value': 0.0, 'awg_position_price': 0.02011, 'locked_buy': 0.0, 'sec_code': 'VTBR',
    # 'trdaccid': 'L01+00000F00', 'client_code': '593458R8NYF'}
    accountDepoLimits = [depoLimit for depoLimit in depoLimits  # Бумажный лимит
                         if depoLimit['client_code'] == clientCode and  # Выбираем по коду клиента
                         depoLimit['firmid'] == firmId and  # Фирме
                         depoLimit['limit_kind'] == limitKind and  # Дню лимита
                         depoLimit['currentbal'] != 0]  # Берем только открытые позиции по фирме и дню
    for firmKindDepoLimit in accountDepoLimits:  # Пробегаемся по всем позициям
        secCode = firmKindDepoLimit["sec_code"]  # Код тикера
        entryPrice = float(firmKindDepoLimit["wa_position_price"])
        #classCode = qpProvider.GetSecurityClass(classCodes, secCode)['data']
        lastPrice = float(
            qpProvider.GetParamEx(classCode, secCode, 'LAST')['data']['param_value'])  # Последняя цена сделки
        # if classCode == 'TQOB':  # Для рынка облигаций
        #     lastPrice *= 10  # Умножаем на 10
        print(f'- Позиция {classCode}.{secCode} {firmKindDepoLimit["currentbal"]} @ {entryPrice:.2f}/{lastPrice:.2f}')


    cerebro = bt.Cerebro()  # Инициируем "движок" BackTrader

    symbol = f'{classCode}.{secCode}'

    cerebro.addstrategy(LimitCancel, LimitPct=1, Depo=2000, Lot=lot, Percent=50)  # Добавляем торговую систему с лимитным входом в n%
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)
    # broker = store.getbroker(use_positions=False)  # Брокер со счетом по умолчанию (срочный рынок РФ)
    broker = store.getbroker(use_positions=False, ClientCode=clientCode, ClientCodeTerminal=clientCodeTerminal, FirmId=firmId, TradeAccountId=tradeAccountId, LimitKind=2, CurrencyCode='SUR', IsFutures=False)  # Брокер со счетом фондового рынка РФ
    cerebro.setbroker(broker)  # Устанавливаем брокера
    data = store.getdata(dataname=symbol, timeframe=bt.TimeFrame.Minutes, compression=1,
                         fromdate=datetime(2022, 4, 18), sessionstart=time(7, 0), LiveBars=True)  # Исторические и новые минутные бары за все время
    cerebro.adddata(data)  # Добавляем данные
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10000)  # Кол-во акций для покупки/продажи
    cerebro.run()  # Запуск торговой системы
