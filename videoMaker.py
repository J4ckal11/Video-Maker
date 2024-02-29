from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from gtts import gTTS
from gtts.tokenizer import pre_processors
import gtts.tokenizer.symbols
from moviepy.editor import *
import re
import os
import time
import random

gtts.tokenizer.symbols.SUB_PAIRS.append(
    ('AITA', 'am i the asshole')
)


def remove_emojis(string):
    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # Remove emojis from the text
    return emoji_pattern.sub(r'', string)


def only_alphabets(string):
    # Define the regex pattern for alphabetic characters
    alphabet_pattern = re.compile(r'[^a-zA-Z\s]')
    # Replace non-alphabetic characters with an empty string
    return alphabet_pattern.sub('', string)


videonum = input("How many videos would you like?\n")

postnum = 2
savedpostnum = 0

while not savedpostnum >= int(videonum):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.reddit.com/r/AmItheAsshole/")

    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)

    time.sleep(1.5)

    posts = driver.find_elements(By.CSS_SELECTOR, '.w-full.m-0')
    num = 2

    title = posts[postnum].get_attribute('aria-label')
    print(title)

    directory = "posts/" + only_alphabets(title) + "/"

    try:
        os.makedirs(directory)
        link = posts[postnum].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].get_attribute('href')
        driver.get(link)
        paragraph = driver.find_element(By.XPATH,
                                        '//*[@class[contains(string(), "md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")]]').find_element(
            By.XPATH, './p[1]').get_attribute('innerHTML')
        text = paragraph
        while True:
            try:
                paragraph = driver.find_element(By.XPATH,
                                                '//*[@class[contains(string(), "md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")]]').find_element(
                    By.XPATH, './p[' + str(num) + ']').get_attribute('innerHTML')
                text += paragraph
                num += 1
            except:
                break
        text = remove_emojis(text)
        savedpostnum += 1
        f = open(directory + "text.txt", "w")
        f.write(title + "\n" + text)
        f.close()
        tts = gTTS(title + text)
        tts.save(directory + 'text.mp3')

        randomFile = random.choice(os.listdir("videos"))

        video = VideoFileClip("videos/" + randomFile)
        audio = AudioFileClip(directory + 'text.mp3')

        videoDuration = int(video.duration)
        audioDuration = int(audio.duration)

        startTime = random.randint(0, videoDuration)
        endTime = startTime + audioDuration

        if endTime > videoDuration:
            startTime -= endTime - videoDuration
            endTime = startTime + audioDuration

        clip = video.subclip(startTime, endTime)
        clip.audio = audio
        clip.write_videofile(directory + "clip.mp4")
    except OSError as error:
        pass

    postnum += 1

print("Done")
