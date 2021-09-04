import time
import Email
from random import randint
# Must manually end program as driver.quit() function is missing


def start():
    import WebScrap as W
    W.boot_up()
    W.analyzing()

    # while True:
    #     print("TIME: ", W.get_time())
    #     possible_coins = W.look_for_changing_EMAS()
    #
    #     if possible_coins:
    #         symbol = possible_coins[randint(0, len(possible_coins) - 1)]
    #         assert W.click_on_watchlist(symbol)
    #         # Currently only the first coin to be spotted to hold will be held, any
    #         # other coins that are a good buy will be discarded
    #         print(f"Analyzing:  {symbol}", "Starting MACD test...", end="\n")
    #
    #         # Email.send_email(Email.boom, f"\tCurrently analyzing {symbol} MACD at : {W.get_time()}")
    #
    #         if W.MACD_test_buy():
    #             # Start while loop with W.MACD_HOLD_SELL() to keep holding until
    #             # MACD decreases or stop loss
    #             print(f"Purchase {symbol} and hold!!!!")
    #             m = f"""\t
    #             Buy: {symbol}
    #             \tprice: {W.get_price()}
    #             Time: {W.get_time()}
    #             """
    #             print(f"Price: {W.get_price()}", f"Time: {W.get_time()}", sep="\n")
    #             Email.send_email([Email.boom], m)
    #             W.MACD_hold_and_sell()
    #             print("==================", f"SELL ALERT:  {symbol}", "==================", sep="\n")
    #             m = f"""\t
    #             Sell: {symbol}
    #             \tprice: {W.get_price()}
    #             Time: {W.get_time()}
    #             """
    #             Email.send_email([Email.boom], m)
    #     else:
    #         print("No possible purchases found, restarting...")
    #     time.sleep(10)


if __name__ == "__main__":
    start()



