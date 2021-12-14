'''
Author: Ross Lamont
Program: This program is a simple web scraper that boots open chrome and uses information from the inspect element
to catalog and download images from google.
Date: 6/11/2021


'''





import time


from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io

from PIL import Image

PATH = 'C:\\Users\\rossl\\OneDrive\\Documents\\chrome scraper\\chromedriver.exe'

wd = webdriver.Chrome(PATH)


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script('window.scroll(0, document.body.scrollHeight);')
        time.sleep(delay)
    url ='https://www.google.com/search?q=star+citizen&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj81L67kJ30AhUNa8AKHVo8DqUQ_AUoA3oECAEQBQ&biw=929&bih=932&dpr=1'
    wd.get(url)
    image_urls = set()
    skips = 0
    while len(image_urls) + skips < max_images:
        scroll_down(wd)
        thumbnail = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')
        for img in thumbnail[len(image_urls) + skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
        images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')
        for image in images:
            if image.get_attribute('src') in image_urls:
                max_images += 1
                skips += 1
                break

            if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                image_urls.add(image.get_attribute('src'))
                print('found image')
                print(f'Found{len(image_urls)}')
    return image_urls






def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')
        print('success')
    except Exception as e:
        print('failed -', e)


urls = get_images_from_google(wd, 0, 10)
for i, url in enumerate(urls):
    download_image('/\\img', url, str(i) + '.jpg')
wd.quit()
