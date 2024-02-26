from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from gtts import gTTS
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols
import re

gtts.tokenizer.symbols.SUB_PAIRS.append(
    ('AITA', 'am i the asshole')
)

def remove_emojis(text):
    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # Remove emojis from the text
    return emoji_pattern.sub(r'', text)

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Optional: Run Chrome in headless mode
driver = webdriver.Chrome(options=options)
driver.get("https://www.reddit.com/r/AmItheAsshole/")

html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.END)

time.sleep(1)

posts = driver.find_elements(By.CSS_SELECTOR, '.w-full.m-0')
num = 2
postnum = 2

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
text = remove_emojis(text)
print(text)

tts = gTTS(text)
tts.save('text.mp3')
