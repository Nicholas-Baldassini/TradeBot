import time
import Email
# Must manually end program as driver.quit() function is missing

stop_loss = 0.1
# Sell if 10% of coin is lost


def start():
    import WebScrap as W

    while True:
        print("TIME: ", W.get_time())
        possible_coins = W.look_for_changing_EMAS()

        if possible_coins:
            symbol = possible_coins[0]
            assert W.click_on_watchlist(symbol)
            # Currently only the first coin to be spotted to hold will be held, any
            # other coins that are a good buy will be discarded
            print(f"Analyzing:  {symbol}", "Starting MACD test...", end="\n")

            Email.send_email(Email.boom, "POSSIBLE PURCHASE GO TO COMPUTER")

            if W.MACD_test_buy():
                # Start while loop with W.MACD_HOLD_SELL() to keep holding until
                # MACD decreases or stop loss
                print(f"Purchase {symbol} and hold!!!!")
                m = f"""
                Buy: {symbol}
                Price: {W.get_price()}
                Time: {W.get_time()}
                """
                Email.send_email(Email.boom, " Buy")

        else:
            print("No possible purchases found, restarting...")
        time.sleep(10)


if __name__ == "__main__":
    start()



