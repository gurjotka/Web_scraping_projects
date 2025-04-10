from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL = "http://orteil.dashnet.org/experiments/cookie/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=URL)

cookie_click = driver.find_element(By.ID, value="cookie")
items_name = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items_name]

timeout = time.time() + 5
five_min = time.time() + 60 * 5

while True:
    cookie_click.click()

    if time.time() > timeout :
        items = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        items_price = []
        for item in items:
            item_text = item.text
            if item_text != '':
                cost = int(item_text.split(" - ")[1].replace(",", ""))
                items_price.append(cost)

        upgrades_dict = {}
        for n in range(len(items_price)):
            upgrades_dict[items_price[n]] = item_ids[n]

        money = driver.find_element(by=By.ID, value="money").text
        if "," in money:
            money = money.replace(",", "")

        cookie_count = int(money)

        affordable_updates={}
        for cost, id in upgrades_dict.items():
            print(upgrades_dict)
            if cookie_count > cost:
                affordable_updates[cost] = id

        highest_price_affordable = max(affordable_updates)
        # print(highest_price_affordable)
        upgrade_purchase_id = affordable_updates[highest_price_affordable]

        driver.find_element(By.ID, value=upgrade_purchase_id).click()



        timeout = time.time() + 15

    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break




driver.quit()