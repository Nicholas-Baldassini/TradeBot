from selenium import webdriver
import Email
import time

url = "https://www.tradingview.com/#signin"
chart_url = "https://www.tradingview.com/chart"
password = "AgainWithTheMaestro123"
email = "bottrader00002@gmail.com"

MAC_PATH = "/Users/baldo/Applications/chromedriver"
WIN_PATH = "C:\Program Files (x86)\CHROMEWEBDRIVER\chromedriver"
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
index_to_seconds = [60, 180, 5 * 60, 15 * 60, 30 * 60, 45 * 60, 60 * 60, 120 * 60, 180 * 60]
# index from the above comment corresponds the amount in seconds ^^^
time_interval = 1
time.sleep(0.5)
driver.find_elements_by_class_name("item-2IihgTnv")[time_interval].click()
time.sleep(0.5)



def get_EMA(wait=False, length=2):
    """
    If wait=True, the ema is taken over a time of length to give a more accurate reading and get rid of
    instantaneous spikes that may throw off the count
    """
    if wait:
        ema_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
        ema_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)
        time.sleep(length)
        ema2_3 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text)
        ema2_9 = float(driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text)

        return ((ema_3 - ema_9) + (ema2_3 - ema2_9))/2
    else:
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
    print("Searching for negative EMA's...")
    print("===============================")
    negative_EMAS = []
    for e in driver.find_elements_by_class_name("wrap-1a1_EyKG"):
        try:
            # Not all elements ae coins in the watchlist, so im cheating with
            # this try/except :)
            e.click()
            time.sleep(3)
            print(e.text.split("\n")[0], get_EMA())
            if get_EMA() < 0.05:
                # 0.5 SHOULD BE A RATIO TO EACH COIN NOT A HARD CODED 0.5
                # ----------------------------------------------------
                print("Negative EMA: ", e.text.split("\n")[0])
                negative_EMAS.append(e.text.split("\n")[0])
        except:
            continue
    print("Finished searching for negative EMA's")
    print("Negative EMA's: ", negative_EMAS)
    print("===============================")
    return negative_EMAS


def look_for_changing_EMAS():
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
                    # 0.5 SHOULD BE A RATIO TO EACH COIN NOT A HARD CODED 0.5
                    # ----------------------------------------------------
                    light_side.append(e.text.split("\n")[0])
        except:
            continue
    print("Finished searching for changing EMA's")
    print("Changed EMA's: ", light_side)
    print("===============================")
    return light_side

def get_MACD():
    macd = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[3]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]")
    # [bar number, line #1, line #2]
    return float(macd.text.replace(chr(8722), '-'))


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

            holding.clear()
        else:
            print("No purchases found.")

def MACD_test_buy():
    """
    Get time from the website, every time a new minute happens gather MACD information and determine buy/sell
    """
    macd_time_interval = 3 * 60
    macd_length = 3
    macd = get_MACD()
    # The macd the moment we find a positive ema
    # Now check the next "macd_length" macd's to check if they are all increasing values to buy
    print("Checking MACD:  ", macd)

    prev_macd = macd
    for _ in range(macd_length):
        time.sleep(macd_time_interval)
        # Change the second amount to the time interval we are on so we get new macd
        next_macd = get_MACD()
        if next_macd < 0:
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
    # If we reach this point, there has been a successful increasing MACD


def MACD_hold_sell(stop_loss=5):
    """
    From here, we bought the coin already, we now analyze the MACD for n consistent negative MACD's to indidicate a
    sell signal or a stop_loss, either sell the coin if the coin dips below the stop_loss or n negative MACD's
    """

time.sleep(2)


time.sleep(100)
driver.quit()
