from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import WebScrap as WB


class coin:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.price = None
        self.EMA = None
        # self.ema_small = None
        # self.ema_big = None
        self.macd = None
        self.hold = None

    def __str__(self):
        return f"{self.symbol}: {self.price}\n ========"

action = ActionChains(WB.driver)
chart = WB.driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]")


action.key_down(Keys.CONTROL)
action.perform()

for e in WB.driver.find_elements_by_class_name("wrap-1a1_EyKG"):
    chart.click()
    time.sleep(1)

action.key_up(Keys.CONTROL)
action.perform()

WB.driver.close()
WB.driver.switch_to.window(WB.driver.window_handles[0])
time.sleep(5)

coin_symbols = [e.text.split("\n")[0] for e in WB.driver.find_elements_by_class_name("wrap-1a1_EyKG")]
coins = {}
for ind, tab in enumerate(WB.driver.window_handles):
    WB.driver.switch_to.window(tab)
    time.sleep(1)
    if WB.driver.title == "429 Too Many Requests":
        WB.driver.refresh()
        time.sleep(2)
    WB.click_on_watchlist(coin_symbols[ind])
    coins[coin_symbols[ind]] = coin(coin_symbols[ind])
    time.sleep(0.5)


while True:
    for tab in WB.driver.window_handles:
        WB.driver.switch_to.window(tab)
        tab_symbol = WB.get_symbol()
        c = coins[tab_symbol]
        c.price = WB.get_price()
        c.EMA = WB.get_EMA()
        c.macd = WB.get_MACD()

    for c in coins.values(): print(c)
