from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.tradingview.com/#signin"
chart_url = "https://www.tradingview.com/chart"
email = "DelTheFunkiestHomoSapien@gmail.com"
password = "BoomJohn_123"

PATH = "/Users/baldo/Applications/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get(url)

driver.set_window_position(0, 0)
driver.set_window_size(1300, 1200)

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
driver.find_element_by_id("header-toolbar-study-templates").click()
time.sleep(1)
driver.find_element_by_class_name("titleItem-2noQNU_F").click()

def get_emas():
    while True:
        time.sleep(2)
        price = driver.find_element_by_class_name("priceWrapper-3PT2D-PK").text
        ema_3 = driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-1].text
        ema_9 = driver.find_elements_by_class_name("valueValue-2KhwsEwE")[-2].text
        print(f"EMA3: {ema_3}")
        print(f"EMA9: {ema_9}")
        print(f"Price: {price}")
        if float(ema_3) - float(ema_9) > 0:
            print("BUY/HOLD")
        else:
            print("SELL/MONITOR")
        print("=============================")



time.sleep(2)
get_emas()


time.sleep(100)
driver.quit()
