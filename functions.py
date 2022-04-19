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
    print(money, cost_lot, shares_can_buy, size_mod, size)
    return int(size), int(shares_can_buy)
