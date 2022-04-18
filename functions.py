def calc_size(depo, lot, percent, ticker_price):
    """
    Функция расчета позиции
    depo - наш депозит
    lot - сколько акций в одном лоте
    percent - сколько денег тратим из депозита
    ticker_price - по какой цене считаем размер позиции
    """
    money = depo * percent / 100
    cost_lot = lot *ticker_price
    shares_can_buy = money / cost_lot
    size = shares_can_buy * lot     # размер не кратный lot
    size = int(size / lot) * lot    # размер кратный lot
    return int(size), int(shares_can_buy)
