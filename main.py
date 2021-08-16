import time
import threading


precision = 0.5
# In milliseconds

ema_low = []
ema_high = []




def value_func(buy: float, sell: float, amount: float):
    """
    Calculates net change on `amount` based on the buying price and selling
    price

    Amount is in Canadian$

    >>> value_func(43560, 45360, 5000)
        5206.61157
    >>> value_func(100, 200, 50)
        100
    """
    coin_amount = buy / amount
    # Amount of coins you own in that currency (BTC, ETH, LTC...)

    closing_amount = coin_amount * sell
    # Amount of your own currency you own based off the closing amount and
    # amount of coin_amount you own (CAD, USD, EUR...)

    return closing_amount


# def symbol_price():
#     while True:
#         price = driver.find_element_by_class_name("tv-symbol-price-quote__value")
#         print(symbol, " price: ", price.text)
#         time.sleep(precision)


price_thread = threading.Thread(target=symbol_price)
price_thread.start()



def update_ema(lower: list, higher: list):
    """
    Scrape and store ema information, should be threaded
    """
    lower_ema = None
    higher_ema = None
    # Information scraped ^

    outlier_constant = 10

    if len(lower) > outlier_constant:
        lower.pop(0)
        lower.append(lower_ema)
        higher.pop(0)
        higher.append(higher_ema)


def buy_sell_signals(lower: list, higher: list):
    """
    Computes buy sell signals
    """
    safety = 90
    # safety is the percent of emas that follow the trend
    pass


def buy_sell_action(signal: bool, amount):
    """
    Make a purchase based on the buy_sell_signals function

    True: BUY
    False: SELL

    Possible to include a spectrum of buying/selling: Only sell 50% of current
    amount because of unpredictability instead of the whole amount...
    """
    pass
    # Make the necessary selenium action calls on fee free website for trading


time.sleep(100)
driver.quit()


