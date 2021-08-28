from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import InformationExtract as IE


url = "https://www.tradingview.com/#signin"
password = IE.Email_Password[0]
email = IE.Email_Sender[0]

MAC_PATH = IE.Driver_Path[1]
WIN_PATH = IE.Driver_Path[0]

driver = webdriver.Chrome(WIN_PATH)
driver.get(url)
driver.set_page_load_timeout(5)

driver.set_window_position(0, 0)
driver.set_window_size(1300, 1200)

# Signing into account
driver.find_elements_by_class_name("tv-social__title")[2].click()
driver.find_element_by_name("username").send_keys(email)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("tv-button__loader").click()
time.sleep(2.5)


# time.sleep(1.5)
# driver.find_element_by_class_name("tv-goto-chart-button").click()
# time.sleep(1)
# driver.switch_to.window(driver.window_handles[-1])
# time.sleep(2.5)

# # Enable indicator template for EMA's
# driver.find_element_by_id("header-toolbar-study-templates").click()
# time.sleep(1)
# driver.find_element_by_class_name("titleItem-2noQNU_F").click()
# driver.find_element_by_id("header-toolbar-intervals").click()


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
# index_to_seconds = [60, 180, 5 * 60, 15 * 60, 30 * 60, 45 * 60, 60 * 60, 120 * 60, 180 * 60]
# # index from the above comment corresponds the amount in seconds ^^^
# time_interval = 3
# time.sleep(0.5)
# driver.find_elements_by_class_name("item-2IihgTnv")[time_interval].click()
# time.sleep(0.5)


def get_time() -> str:
    t = time.localtime()
    return time.strftime("%H:%M:%S", t)


def get_symbol() -> str:
    return driver.find_element_by_class_name("title-2ahQmZbQ").text


def get_EMA(wait=False, length=2):
    """
    If wait=True, the ema is taken over a time of length to give a more accurate reading and get rid of
    instantaneous spikes that may throw off the count
    """

    # FIX THE SCRAPE DATA, if indicators change than the ema wont be scraped correctly, because of indices
    if wait:
        ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
        ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)
        time.sleep(length)
        ema2_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
        ema2_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)

        return ((ema_3 - ema_9) + (ema2_3 - ema2_9))/2
    else:
        ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[9].text)
        ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[8].text)
    return ema_3 - ema_9


def get_MACD():
    macd = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[3]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]")
    # [bar number, line #1, line #2]
    return float(macd.text.replace(chr(8722), '-'))


def click_on_watchlist(coin: str) -> bool:
    """
    Click on the desired coin on the watchlist to bring up its chart
    """
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        if e.text.split("\n")[0] == coin:
            e.click()
            print("Clicked on ", coin)
            time.sleep(2)
            return True
    print(f"Could not find {coin} to click in watchlist")
    return False


def get_price():
    return float(driver.find_element_by_class_name("highlight-2GhssDiZ").text)


def find_possible_coins() -> list:
    """
    This functions finds all the coins that are currently falling, we only want
    to be looking at coins that are currently falling so then the moment that
    they begin to rise we can buy instead of buying already rising coins and
    risk purchasing at peaks, with this method we are guaranteed to sell at
    higher prices than purchasing
    """
    print("Searching for negative EMA's...")
    print("===============================")
    time.sleep(2)
    negative_EMAS = []
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        try:
            # Not all elements ae coins in the watchlist, so im cheating with
            # this try/except :)
            driver.execute_script("arguments[0].scrollIntoView();", e)
            time.sleep(0.5)
            e.click()
            time.sleep(3)
            print(e.text.split("\n")[0], get_EMA())
            if get_EMA() < -0.005:
                # If this happens, then the EMA3 < EMA9 -> downtrend
                print("Negative EMA: ", e.text.split("\n")[0])
                negative_EMAS.append(e.text.split("\n")[0])
        except:
            pass
            #continue
    print("Finished searching for negative EMA's")
    print("Negative EMA's: ", negative_EMAS)
    print("===============================")
    return negative_EMAS


def look_for_changing_EMAS() -> list:
    """
    This function searches through the negative EMA coins and checks if their
    new EMA value has just become positive, if it does this implies a climb about
    to take place and should imply a correct buy signal, this method ensures we
    do we not buy during peaks and only buy during plateau's or dips.
    """

    negative = find_possible_coins()
    print("Looking for changing EMA's...")
    print("=============================")
    time.sleep(5)  # change to 30 sec
    light_side = []
    # Open up a tab for each coin in the light side then analyze if they they pass the MACD test
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        try:
            if e.text.split("\n")[0] in negative:
                e.click()
                time.sleep(3)
                if get_EMA() > 0.05:
                    light_side.append(e.text.split("\n")[0])
        except:
            continue
    print("Finished searching for changing EMA's")
    print("Changed EMA's: ", light_side)
    print("===============================")
    return light_side


def MACD_test_buy() -> bool:
    """
    Get time from the website, every interval, update MACD information and determine buy/sell
    """
    macd_time_interval = index_to_seconds[time_interval] - 5 * 60
    macd_length = 3
    macd = get_MACD()
    # The macd the moment we find a positive ema
    # Now check the next "macd_length" macd's to check if they are all increasing values to buy
    print("Checking MACD:  ", macd)

    prev_macd = macd
    for ind in range(macd_length):
        time.sleep(macd_time_interval)
        # Change the second amount to the time interval we are on so we get new macd
        next_macd = get_MACD()
        if next_macd < 0 and ind:
            # The "and ind" allows for the first and second MACD's to be negative but still
            print("NEGATIVE MACD")
            return False
        elif next_macd > prev_macd:
            print(f"Increasing MACD: {next_macd}, continuing to analyze...")
            prev_macd = next_macd
        elif next_macd <= prev_macd:
            print("DECREASING MACD, Failure", next_macd)
            return False
        else:
            print("You fucked up you should not be here")
            raise Exception

    return True
    # If we reach this point, there has been a successful increasing MACD and we purchase


def MACD_hold_and_sell(stoploss=0.002, n=4):
    """
    From here, we bought the coin already, we now analyze the MACD for n consistent negative MACD's to indidicate a
    sell signal or a stop_loss, either sell the coin if the coin dips below the stop_loss or n negative MACD's

    Will either sell if stop loss or n decreasing MACD's in a row

    This function will run for as long as we should hold, send email after function call is over
    """

    # TODO Test implementing stop loss on multithreading approach to update on smaller interval than the MACD

    sell_point = (1 - stoploss) * get_price()
    print(f"Initial sell point: {sell_point}")

    macd_time_interval = index_to_seconds[time_interval]  - 5 * 60
    # macd_time_interval = 60
    prev_macd = get_MACD()
    prev_price = get_price()
    decreasing_macds = 0

    while decreasing_macds < n and get_price() >= sell_point:
        time.sleep(macd_time_interval)
        next_macd = get_MACD()
        next_price = get_price()
        if next_macd < 0:
            print("Sell the fucking stock its tanking")
            break
        elif next_macd < prev_macd:
            decreasing_macds += 1
            print("Decreased MACD: ", prev_macd, next_macd)
        elif next_macd > prev_macd:
            decreasing_macds = 0
            print("Increased MACD: ", prev_macd, next_macd, sep=" ")

        if next_price > prev_price:
            sell_point = (1 - stoploss) * get_price()
            print("Stop loss increased: ", sell_point)

        prev_price = next_price
        prev_macd = next_macd
    print("Sell conditions met", f"n = {decreasing_macds}", f"Sell Point: {sell_point}", f"Price: {get_price()}", sep="\n")

# time.sleep(5 * 60)
# driver.quit()
