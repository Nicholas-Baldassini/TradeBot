from selenium import webdriver
import Email
import time

url = "https://www.tradingview.com/#signin"
chart_url = "https://www.tradingview.com/chart"
password = "AgainWithTheMaestro123"
email = "bottrader00002@gmail.com"

PATH = "/Users/baldo/Applications/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get(url)
driver.set_page_load_timeout(5)

driver.set_window_position(0, 0)
driver.set_window_size(1300, 1200)

# Signing into account
driver.find_elements_by_class_name("tv-social__title")[2].click()
driver.find_element_by_name("username").send_keys(email)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("tv-button__loader").click()
time.sleep(2)

# Clicks the top sorted coin, change index to view other coins
# Starts at 2
index = 2
driver.find_element_by_xpath(f"/html/body/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[{index}]").click()
time.sleep(1.5)
driver.find_element_by_class_name("tv-goto-chart-button").click()
time.sleep(1)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2.5)

# Enable indicator template for EMA's
driver.find_element_by_id("header-toolbar-study-templates").click()
time.sleep(1)
driver.find_element_by_class_name("titleItem-2noQNU_F").click()
driver.find_element_by_id("header-toolbar-intervals").click()


"""
0 = 1 min
1 = 3 min
2 = 5 min
3 = 15 min
4 = 30 min
5 = 45 min
6 = 1 hour
7 = 2 hour
8 = 3 hour
9 = 4 hour
"""
time_interval = 6
time.sleep(0.5)
driver.find_elements_by_class_name("item-2IihgTnv")[time_interval].click()
time.sleep(0.5)


symbol_holder = {}
symbol_sorted = []
def update_watchlist():
    global symbol_holder
    global symbol_sorted
    symbol_holder = {}
    symbol_sorted = []
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        stonk = e.text.split("\n")
        # stonk = ["BTC", "643423.34", "-453.43", "2.98%"
        if not stonk[-1][0].isnumeric():
            stonk[-1] = stonk[-1].replace(chr(8722), '-')
        symbol_sorted.append(float(stonk[-1][:-1]))
        symbol_holder[float(stonk[-1][:-1])] = stonk[0]
    symbol_sorted.sort(reverse=True)


def get_EMA():
    ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
    ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)
    return ema_3 - ema_9


def find_possible_coins():
    """
    This functions finds all the coins that are currently falling, we only want
    to be looking at coins that are currently falling so then the moment that
    they begin to rise we can buy instead of buying already rising coins and
    risk purchasing at peaks, with this method we are guaranteed to sell at
    higher prices than purchasing
    """
    print("Searching for negative EMA's")
    negative_EMAS = []
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        try:
            # Not all elements ae coins in the watchlist, so im cheating with
            # this try/except :)
            e.click()
            time.sleep(3)
            EMA = get_EMA()
            print(e.text.split("\n")[0], EMA)
            print("Ema:" , get_EMA())
            if EMA < 0.05:
                # 0.5 SHOULD BE A RATIO TO EACH COIN NOT A HARD CODED 0.5
                # ----------------------------------------------------
                print("Negative: ", e.text.split("\n")[0])
                negative_EMAS.append(e.text.split("\n")[0])
        except:
            continue
    print("Finished searching for negative EMA's")
    print("Negative EMA's: ", negative_EMAS)
    print("===============================")
    return negative_EMAS


def look_for_changing_EMAS():
    """
    This function searchs through the negative EMA coins and checks if their
    new EMA value has just become positive, if it does this implies a climb about
    to take place and should imply a correct buy signal, this method ensures we
    do we not buy during peaks and only buy during plateau's or dips.
    """

    negative = find_possible_coins()
    print("Looking for changing EMA's")
    time.sleep(5) # change to 30 sec
    light_side = []
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        try:
            if e.text.split("\n")[0] in negative:
                e.click()
                time.sleep(3)
                if get_EMA() > 0:
                    # 0.5 SHOULD BE A RATIO TO EACH COIN NOT A HARD CODED 0.5
                    # ----------------------------------------------------
                    light_side.append(e.text.split("\n")[0])
        except:
            continue
    print("Finished searching for changing EMA's")
    print("Changed EMA's: ", light_side)
    print("===============================")
    return light_side


def hold(coin: str):
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        if coin == e.text.split("\n")[0]:
            print("Found :", coin)
            e.click()
            time.sleep(4)
            symbol = e.text.split("\n")[0]
            price = e.text.split("\n")[1]
            t = time.localtime()
            buy_time = time.strftime("%H:%M:%S", t)
            print("=======")
            print("SENT PURCHASE EMAIL")
            print("=======")
            m = f"""
            \t
            BUY:  {symbol}\n
            Price:  ${price}
            Time:  {buy_time} EST
            EMA:  {round(get_EMA(), 6)}
            """
            Email.send_email(Email.boom, m)
            time.sleep(10)
            while get_EMA() > 0:
                # Keep holding
                print("Keep holding: ", symbol)
                print("Price: ", e.text.split("\n")[1])
                time.sleep(15)
            print("SENT SELL EMAIL")
            t = time.localtime()
            sell_time = time.strftime("%H:%M:%S", t)
            sell_price = "Not Found"
            for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
                if coin == e.text.split("\n")[0]:
                    sell_price = e.text.split("\n")[1]
            m = f"""
            \t
            Sell:  {symbol}\n
            Price:  ${sell_price}
            Time:  {sell_time} EST
            EMA:  {round(get_EMA(), 6)}
            """
            Email.send_email(Email.boom, m)

def find_coins_to_buy():
    holding = []
    # Currently only the first coint to be spotted to hold will be held, any
    # other coins that are a good buy will be discarded
    while True:
        print("Looking for possible purchases....")
        t = time.localtime()
        local_time = time.strftime("%H:%M:%S", t)
        print("Time: ", local_time)
        coins = look_for_changing_EMAS()
        if coins:
            print("Found a possible coin: ", holding)
            holding.extend(coins)
            hold(holding[0])
            holding.clear()
        else:
            print("No purchases found.")



time.sleep(2)
find_coins_to_buy()
# def get_emas():
#     while True:
#         time.sleep(10)
#         update_watchlist()
#         for crypto in symbol_sorted:
#             for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
#                 try:
#                     e.text.split("\n")[0]
#                 except:
#                     continue
#                 if e.text.split("\n")[0] == symbol_holder[crypto]:
#                     """
#                     At this point we have found a suitable crypto to analyze
#                     We now compute if this symbol is in a BUY/HOLD state or a
#                     SELL/MONITOR state, we continue looping if SELL and we
#                     continue refreshing and computing if on BUY
#                     """
#                     e.click()
#                     time.sleep(3)
#                     print("Analyzing ", {e.text.split('\n')[0]})
#                     bought = False
#                     ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
#                     ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)
#                     symbol = e.text.split("\n")[0]
#                     price = e.text.split("\n")[1]
#                     t = time.localtime()
#                     l_time = time.strftime("%H:%M:%S", t)
#
#                     while ema_3 - ema_9 > 0.05:
#                         # Stay on this crypto
#                         symbol = e.text.split("\n")[0]
#                         price = e.text.split("\n")[1]
#                         t = time.localtime()
#                         l_time = time.strftime("%H:%M:%S", t)
#                         ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
#                         ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)
#
#                         print("BUY/HOLDING")
#                         print(symbol, ": ", price)
#                         print("EMA DIFF: ", ema_3 - ema_9)
#                         print(f"Time: {l_time}")
#                         print("=================")
#                         if not bought:
#                             print("=======")
#                             print("SENT PURCHASE EMAIL")
#                             print("=======")
#                             m = f"""
#                             \t
#                             BUY:  {symbol}\n
#                             Price:  ${price}
#                             Time:  {l_time} EST
#                             EMA:  {round(ema_3 - ema_9, 6)}
#                             """
#                             Email.send_email(Email.boom, m)
#                             # Send Email to buy the symbol
#                             bought = True
#                         time.sleep(10)
#                     print("SELL/MONITOR")
#                     print("============")
#                     if bought:
#                         print("=======")
#                         print("SENT SELL EMAIL")
#                         print("=======")
#                         m = f"""
#                             \t
#                             SELL:  {symbol}\n
#                             Price:  ${price}
#                             Time:  {l_time} EST
#                             EMA:  {round(ema_3 - ema_9, 6)}
#                             """
#                         Email.send_email(Email.boom, m)
#                         # Send Email to sell the symbol and maybe some emojis for the celebration
#                         bought = False
#                     else:
#                         print(e.text.split("\n")[0], " is falling, don't buy")
#
#
# time.sleep(5)
# get_emas()


time.sleep(100)
driver.quit()
