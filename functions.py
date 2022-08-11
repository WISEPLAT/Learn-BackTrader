import datetime, os
import pandas as pd

def calc_size(depo, lot, percent, ticker_price):
    """
    Функция расчета позиции
    depo - наш депозит
    lot - сколько акций в одном лоте
    percent - сколько денег тратим из депозита
    ticker_price - по какой цене считаем размер позиции
    """
    money = depo * percent / 100
    cost_lot = lot * ticker_price
    shares_can_buy = money / cost_lot
    size_mod = shares_can_buy * lot     # размер не кратный lot
    size = round(size_mod / lot) * lot    # размер кратный lot
    # print(money, cost_lot, shares_can_buy, size_mod, size)
    return size


def get_info_about_paper(qpProvider, symbols, show_log=False):
    """
    Функция получения информацию по бумагам:
    шаг цены, сколько лотов, кол-во десятичных знаков, процент
    """
    syminfo_mintick = f_decimal = lots = {}
    for symbol in symbols:
        _point = symbol.index('.')
        classCode = symbol[0:_point]  # Класс тикера
        secCode = symbol[_point+1:]  # Тикер +1 для точки

        securityInfo = qpProvider.GetSecurityInfo(classCode, secCode)["data"]

        if show_log:
            print(f'Информация о тикере {classCode}.{secCode} ({securityInfo["short_name"]}):')
            print('Валюта:', securityInfo['face_unit'])
            print('Кол-во десятичных знаков:', securityInfo['scale'])
            print('Лот:', securityInfo['lot_size'])
            print('Шаг цены:', securityInfo['min_price_step'])

        syminfo_mintick[symbol] = securityInfo['min_price_step']    # сохраняем Шаг цены в глобальной переменной syminfo_mintick
        f_decimal[symbol] = securityInfo['scale']                   # сохраняем Кол-во десятичных знаков в глобальной переменной f_decimal
        lots[symbol] = securityInfo['lot_size']                      # сохраняем Лот в глобальной переменной lot

    return syminfo_mintick, f_decimal, lots


def export_log_to_csv(my_log, export_dir):
    """
    Функция экспорта логов в csv файл
    """
    time_log = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    df = pd.DataFrame(my_log, columns=('TRADEDATE', 'TICKER', 'SIGNAL', 'S.PRICE', 'ORDER', 'O.PRICE',
                                               'SIZE', 'STATUS', 'COST', 'COMM', 'PNL', 'AMOUNT', 'DEPO', 'STRATEGY_NAME', 'INFO'))
    if not os.path.exists(export_dir): os.makedirs(export_dir)
    df.to_csv(os.path.join(export_dir, time_log+"_logs.csv"), index=False, encoding='utf-8', sep=";", decimal=".")

    # запись имени последнего лог файла
    with open(os.path.join(export_dir, 'last_log_filename.txt'), "w") as the_file:
        the_file.write(time_log+"_logs.csv")
