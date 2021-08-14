from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading

symbol = input("Input symbol: ")
url = "https://www.tradingview.com/symbols/" + symbol

# BTCCAD = "https://www.tradingview.com/symbols/BTCCAD/?exchange=CAPITALCOM"
# BTCUSD = "https://www.tradingview.com/symbols/BTCUSD"
# url = "https://www.tradingview.com"
PATH = "/Users/baldo/Applications/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get(url)
action = ActionChains(driver)

driver.set_window_position(0, 0)
driver.set_window_size(500, 500)

precision = 0.5
# In milliseconds


def symbol_price():
    while True:
        price = driver.find_element_by_class_name("tv-symbol-price-quote__value")
        print(symbol, " price: ", price.text)
        time.sleep(precision)


price_thread = threading.Thread(target=symbol_price)
price_thread.start()

technical_tab = driver.find_element_by_link_text("Technicals")
technical_tab.click()

oscillators = {"Relative Strength Index": None,
               "Stochastic": None,
               "Commodity Channel Index": None,
               "Average Directional Index": None,
               "Awesome Oscillator": None, "Momentum": None,
               "MACD Level": None, "Stochastic RSI Fast": None,
               "Williams Percent Range": None,
               "Bull Bear Power": None, "Ultimate Oscillator": None}

average_keys = [10, 20, 30, 50, 100, 200]
moving_averages = {"Ichmoku Cloud Base Line": None,
                   "Volume Weighted Moving Average": None,
                   "Hull Moving Average": None}

for key in average_keys:
    moving_averages["Exp_avg" + str(key)] = None
    moving_averages["Simple_avg" + str(key)] = None

time.sleep(100)
driver.quit()


