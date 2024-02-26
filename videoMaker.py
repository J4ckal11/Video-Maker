from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Optional: Run Chrome in headless mode
driver = webdriver.Chrome(options=options)
driver.get("https://www.reddit.com/r/AmItheAsshole/")

html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.END)

time.sleep(1)

posts = driver.find_elements(By.CSS_SELECTOR, '.w-full.m-0')
num = 2
postnum = 5

title = posts[postnum].get_attribute('aria-label')
link = posts[postnum].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('href')
print(title)
print(link)

driver.get(link)

paragraph = driver.find_element(By.XPATH, '//*[@class[contains(string(), "md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")]]').find_element(By.XPATH, './p[1]').get_attribute('innerHTML')
text = paragraph
while True:
    try:
        paragraph = driver.find_element(By.XPATH, '//*[@class[contains(string(), "md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")]]').find_element(By.XPATH, './p[' + str(num) + ']').get_attribute('innerHTML')
        text += paragraph
        num += 1
    except:
        break
print(text)

input()
