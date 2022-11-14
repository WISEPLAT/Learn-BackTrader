from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


def OnTransReply(data):
    """Обработчик события ответа на транзакцию пользователя"""
    print('OnTransReply')
    print(data['data'])  # Печатаем полученные данные

def OnOrder(data):
    """Обработчик события получения новой / изменения существующей заявки"""
    print('OnOrder')
    print(data['data'])  # Печатаем полученные данные

def OnTrade(data):
    """Обработчик события получения новой / изменения существующей сделки
    Не вызывается при закрытии сделки
    """
    print('OnTrade')
    print(data['data'])  # Печатаем полученные данные

def OnFuturesClientHolding(data):
    """Обработчик события изменения позиции по срочному рынку"""
    print('OnFuturesClientHolding')
    print(data['data'])  # Печатаем полученные данные

def OnDepoLimit(data):
    """Обработчик события изменения позиции по инструментам"""
    print('OnDepoLimit')
    print(data['data'])  # Печатаем полученные данные

def OnDepoLimitDelete(data):
    """Обработчик события удаления позиции по инструментам"""
    print('OnDepoLimitDelete')
    print(data['data'])  # Печатаем полученные данные

if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # qpProvider = QuikPy(Host='<Ваш IP адрес>')  # Вызываем конструктор QuikPy с подключением к удаленному компьютеру с QUIK
    qpProvider.OnTransReply = OnTransReply  # Ответ на транзакцию пользователя. Если транзакция выполняется из QUIK, то не вызывается
    qpProvider.OnOrder = OnOrder  # Получение новой / изменение существующей заявки
    qpProvider.OnTrade = OnTrade  # Получение новой / изменение существующей сделки
    qpProvider.OnFuturesClientHolding = OnFuturesClientHolding  # Изменение позиции по срочному рынку
    qpProvider.OnDepoLimit = OnDepoLimit  # Изменение позиции по инструментам
    qpProvider.OnDepoLimitDelete = OnDepoLimitDelete  # Удаление позиции по инструментам

    clientCode = '593458R8NYF'  # Код клиента (присваивается брокером)
    tradeAccountId = 'L01+00000F00'

    # symbols = ('TQBR.SBER', 'TQBR.VTBR',)  # Кортеж тикеров
    symbols = ('TQBR.SBER',)  # Кортеж тикеров
    # symbols = ('TQBR.VTBR', )  # Кортеж тикеров

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


    # Новая Тейк-профит заявка
    ticker = "TQBR.SBER"
    classCode = 'TQBR'  # Код площадки
    secCode = 'SBER'  # Код тикера
    TransId = 12345  # Номер транзакции
    price = 111.11  # Цена входа/выхода
    quantity = 1  # Кол-во в лотах

    StopSteps = 1  # Размер проскальзывания в шагах цены
    slippage = float(qpProvider.GetSecurityInfo(classCode, secCode)['data'][
                         'min_price_step']) * StopSteps  # Размер проскальзывания в деньгах
    if slippage.is_integer():  # Целое значение проскальзывания мы должны отправлять без десятичных знаков
        slippage = int(slippage)  # поэтому, приводим такое проскальзывание к целому числу
    transaction = {  # Все значения должны передаваться в виде строк
        'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
        'CLIENT_CODE': clientCode,  # Код клиента. Для фьючерсов его нет
        'ACCOUNT': tradeAccountId,  # Счет
        'ACTION': 'NEW_STOP_ORDER',  # Тип заявки: Новая стоп заявка
        'STOP_ORDER_KIND': 'TAKE_PROFIT_STOP_ORDER',  # Новая Тейк-профит заявка
        'SPREAD': f"{all_step[ticker]:.{all_scale[ticker]}f}",
        'SPREAD_UNITS': 'PRICE_UNITS',
        'OFFSET': f"{all_step[ticker]:.{all_scale[ticker]}f}",
        'OFFSET_UNITS': 'PRICE_UNITS',
        'CLASSCODE': classCode,  # Код площадки
        'SECCODE': secCode,  # Код тикера
        'OPERATION': 'B',  # B = покупка, S = продажа
        'QUANTITY': str(quantity),  # Кол-во в лотах
        'STOPPRICE': str(price),  # Стоп цена исполнения
        'EXPIRY_DATE': 'GTC'}  # Срок действия до отмены
    rez = qpProvider.SendTransaction(transaction)["data"]
    print(f'Новая стоп заявка отправлена на рынок: {rez}')

    # {'exchange_code': '', 'time': 129, 'price': 0.0, 'class_code': 'TQBR', 'date_time': {'month': 11, 'sec': 29, 'mcs': 493103, 'week_day': 0, 'hour': 0, 'min': 1, 'year': 2022, 'ms': 493, 'day': 13},
    # 'first_ordernum': 0, 'uid': 386140, 'gate_reply_time': {'month': 1, 'sec': 0, 'mcs': 0, 'week_day': 1, 'hour': 0, 'min': 0, 'year': 1601, 'ms': 0, 'day': 1}, 'flags': 2359297, 'status': 3,
    # 'client_code': '593458R8NYF', 'trans_id': 12345, 'error_source': 0, 'firm_id': 'MC0061900000', 'error_code': 0, 'account': 'L01+00000F00',
    # 'result_msg': 'Стоп-заявка N [1003033172] зарегистрирована.', 'brokerref': '593458R8NYF', 'server_trans_id': 31856, 'sec_code': 'SBER', 'balance': 0.0, 'quantity': 1.0, 'order_num': 1003033172}

    # classCode = 'SPBFUT'  # Код площадки
    # secCode = 'SiH2'  # Код тикера
    # TransId = 12345  # Номер транзакции
    # price = 77000  # Цена входа/выхода
    # quantity = 1  # Кол-во в лотах

    # Новая лимитная/рыночная заявка
    # transaction = {  # Все значения должны передаваться в виде строк
    #     'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #     'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
    #     'ACCOUNT': 'SPBFUT00PST',  # Счет
    #     'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
    #     'CLASSCODE': classCode,  # Код площадки
    #     'SECCODE': secCode,  # Код тикера
    #     'OPERATION': 'S',  # B = покупка, S = продажа
    #     'PRICE': str(price),  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена в зависимости от направления. Для остальных рыночных заявок цена = 0
    #     'QUANTITY': str(quantity),  # Кол-во в лотах
    #     'TYPE': 'L'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
    # print(f'Новая лимитная/рыночная заявка отправлена на рынок: {qpProvider.SendTransaction(transaction)["data"]}')

    # Удаление существующей лимитной заявки
    # orderNum = 1234567890123456789  # 19-и значный номер заявки
    # transaction = {
    #     'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #     'ACTION': 'KILL_ORDER',  # Тип заявки: Удаление существующей заявки
    #     'CLASSCODE': classCode,  # Код площадки
    #     'SECCODE': secCode,  # Код тикера
    #     'ORDER_KEY': str(orderNum)}  # Номер заявки
    # print(f'Удаление заявки отправлено на рынок: {qpProvider.SendTransaction(transaction)["data"]}')

    # # Новая стоп заявка
    # StopSteps = 10  # Размер проскальзывания в шагах цены
    # slippage = float(qpProvider.GetSecurityInfo(classCode, secCode)['data']['min_price_step']) * StopSteps  # Размер проскальзывания в деньгах
    # if slippage.is_integer():  # Целое значение проскальзывания мы должны отправлять без десятичных знаков
    #     slippage = int(slippage)  # поэтому, приводим такое проскальзывание к целому числу
    # transaction = {  # Все значения должны передаваться в виде строк
    #     'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #     'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
    #     'ACCOUNT': 'SPBFUT00PST',  # Счет
    #     'ACTION': 'NEW_STOP_ORDER',  # Тип заявки: Новая стоп заявка
    #     'CLASSCODE': classCode,  # Код площадки
    #     'SECCODE': secCode,  # Код тикера
    #     'OPERATION': 'B',  # B = покупка, S = продажа
    #     'PRICE': str(price),  # Цена исполнения
    #     'QUANTITY': str(quantity),  # Кол-во в лотах
    #     'STOPPRICE': str(price + slippage),  # Стоп цена исполнения
    #     'EXPIRY_DATE': 'GTC'}  # Срок действия до отмены
    # print(f'Новая стоп заявка отправлена на рынок: {qpProvider.SendTransaction(transaction)["data"]}')

    # Удаление существующей лимитной заявки
    # orderNum = 1234567890123456789  # 19-и значный номер заявки
    # transaction = {
    #     'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #     'ACTION': 'KILL_ORDER',  # Тип заявки: Удаление существующей заявки
    #     'CLASSCODE': classCode,  # Код площадки
    #     'SECCODE': secCode,  # Код тикера
    #     'ORDER_KEY': str(orderNum)}  # Номер заявки
    # print(f'Удаление заявки отправлено на рынок: {qpProvider.SendTransaction(transaction)["data"]}')

    # Удаление существующей стоп заявки
    # orderNum = 1234567  # Номер заявки
    # transaction = {
    #     'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #     'ACTION': 'KILL_STOP_ORDER',  # Тип заявки: Удаление существующей заявки
    #     'CLASSCODE': classCode,  # Код площадки
    #     'SECCODE': secCode,  # Код тикера
    #     'STOP_ORDER_KEY': str(orderNum)}  # Номер заявки
    # print(f'Удаление стоп заявки отправлено на рынок: {qpProvider.SendTransaction(transaction)["data"]}')

    input('Enter - отмена\n')  # Ждем исполнение заявки
    qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
