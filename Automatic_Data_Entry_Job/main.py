from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

google_sheets_link="Your google sheet link"

zillow_clone_link="Your zillow clone link"

response = requests.get(zillow_clone_link)
zillow_webpage = response.text

soup = BeautifulSoup(zillow_webpage, "html.parser")

houses_info = soup.select(".StyledPropertyCardDataWrapper a")
houses_links = [link["href"] for link in houses_info]

houses_address = soup.select(".StyledPropertyCardDataWrapper address")
house_address = [address.getText().strip().replace("|", ",").replace("#", "") for address in houses_address]
print(house_address)

prices = soup.select(".StyledPropertyCardDataWrapper span")
price = [price.getText().replace("/mo", "").replace("+", "") for price in prices]
# print(price)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(google_sheets_link)

time.sleep(5)

for i in range(len(houses_links)):
    address = driver.find_element(By.XPATH, value="//input[@class='whsOnd zHQkBf' and @aria-labelledby='i1 i4']")
    address.send_keys(house_address[i])

    price_form = driver.find_element(By.XPATH, value="//input[@class='whsOnd zHQkBf' and @aria-labelledby='i6 i9']")
    price_form.send_keys(price[i])

    house_link_form = driver.find_element(By.XPATH, value="//input[@class='whsOnd zHQkBf' and @aria-labelledby='i11 i14']")
    house_link_form.send_keys(houses_links[i])

    time.sleep(2)

    submit_button = driver.find_element(By.XPATH, value="//span[@class='l4V7wb Fxmcue']")
    submit_button.click()

    submit_another_response = driver.find_element(By.LINK_TEXT, value="Submit another response")
    submit_another_response.click()
    time.sleep(2)
    
driver.quit()
