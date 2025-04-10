import os

from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv

load_dotenv()

smtp_address = os.environ["SMTP_ADDRESS"]
my_email = os.environ["EMAIL_ADDRESS"]
password = os.environ["EMAIL_PASSWORD"]

URL = "https://www.amazon.in/Lenovo-Tab-M11-Octa-Core-Processor/dp/B0CY1S314G?crid=233JHJ6RI27Z8&dib=eyJ2IjoiMSJ9.xaS28HEQNJQqI6Gb3sM5Pjwle3lVTTYkI7SnPwO3q0Y2E9FxEMuQhHJp0XIaqz2m1KFVz8boHLtTu5H8gKXgwfg7fvk2aF-ILo8Ze727O0MchZZExyc1ph7fS2Mcu3NJmw3BAtzkAXaKKnUXkWr-53TxJB6L1aVj0K200omYQNUSIoeaykOCJeZ3n8GW-WZvLlzlVUaPFn5Kfmn8ryvpTmLpZFn-54iJ_B_ziJBK2wg.2rdrNSaHM1lmXmjzGkQOfmWLvPYUKdF1LDmt-UJuG2k&dib_tag=se&keywords=tablet&qid=1737612964&sprefix=tablet%2Caps%2C368&sr=8-7&th=1"

Practice_url ="https://appbrewery.github.io/instant_pot/"

response = requests.get(url=URL)
amazon_webpage = response.text

soup = BeautifulSoup(amazon_webpage, "html.parser")

price = soup.find(name="span", class_="a-price-whole").getText()
title = soup.find(id="productTitle").getText().strip()

price_number=(price.split(".")[0]).replace(',','')
float_price = float(price_number)
print(float_price)
print(title)


if float_price < 12000.0:
    message = f"{title} is on sale for {price_number}!!"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=smtp_address,
                            msg= f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8"))
