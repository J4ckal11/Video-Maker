from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Optional: Run Chrome in headless mode
driver = webdriver.Chrome(options=options)
driver.get("https://www.reddit.com/r/AmItheAsshole/")

posts = driver.find_elements(By.CSS_SELECTOR, '.w-full.m-0')
postnum = 2
while True:
    if posts:
        title = posts[postnum].get_attribute('aria-label')
        link = posts[postnum].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('href')
        print(title)
        print(link)
        break
    else:
        pass

    time.sleep(0.1)
driver.get(link)
input(done)
