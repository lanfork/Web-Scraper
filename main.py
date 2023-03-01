from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\Kimberly\\PycharmProjects\\web_Scrapper\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

# bck of person url  , i google busy streets    ???
# url = "https://www.google.com/search?q=people+facing+away+in+the+street&tbm=isch&chips=q:people+facing+away+in+the+street,online_chips:walking:CC4GE21MCYI%3D&hl=en&sa=X&ved=2ahUKEwjm99S4wpD7AhUDx1MKHe1lBDIQ4lYoAnoECAEQKQ&biw=759&bih=713"

# fnt of person url  , i googled someone standing in the street
# url = "https://www.google.com/search?q=someone+standing+in+the+street&sxsrf=ALiCzsZkKf2sB7_YfJfWIRJMHwBcnSEwaQ:1667434475039&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiv-se83ZD7AhXzk2oFHc1nDYoQ_AUoAXoECAIQAw&biw=1536&bih=745&dpr=2.5"
# side of person url  , i googled people walking to the side in street
# url = "https://www.google.com/search?q=people+walking+to+the+side+in+street&sxsrf=ALiCzsZyhBtP-CgBN4HZfvf7ECor249u5Q:1667433483312&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiJ9NXj2ZD7AhW1mmoFHSiACCYQ_AUoAXoECAEQAw&biw=1536&bih=745&dpr=2.5"

# balloon url       , i googled balloon
url = "https://www.google.com/search?q=balloon&tbm=isch&ved=2ahUKEwjg-uGb9Nr6AhUIEVMKHSHaDnQQ2-cCegQIABAA&oq=balloon&gs_lcp=CgNpbWcQAzIECCMQJzIECCMQJzIHCAAQsQMQQzIICAAQgAQQsQMyBwgAELEDEEMyBAgAEEMyCAgAEIAEELEDMgcIABCxAxBDMggIABCABBCxAzIICAAQgAQQsQM6BQgAEIAEUMQIWMQIYKUKaABwAHgAgAFwiAHfAZIBAzAuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=AtBGY-DxF4iizAKhtLugBw&bih=738&biw=1068"
wd.get(url)

image_urls = set()  # sets the url so there are no duplicates
max_images1 = 100  # the number of images we want to web scrape
skips = 0  # the number of mages it will skip while web scraping


def get_images_from_google(wd, delay, max_images, skips):
    i = 0

    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    while len(image_urls) + skips < max_images:

        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()

                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")

            for image in images:

                try:
                    image_content = requests.get(image.get_attribute('src')).content
                    image_file = io.BytesIO(image_content)
                    imaged = Image.open(image_file)
                    i += 1
                    print("Image made: " + str(i))

                    if image.get_attribute('src') in image_urls:
                        skips += 1
                        break
                    elif image.get_attribute('src') and 'http' in image.get_attribute('src'):
                        image_urls.add(image.get_attribute('src'))
                        print(f"Found {len(image_urls)}")
                except:  # if it cannot get images it will add to the max images while still skipping
                    if image.get_attribute('src') in image_urls:
                        break
                    elif image.get_attribute('src') and 'http' in image.get_attribute('src'):
                        print("Max Images " + str(max_images))
                        max_images += 1

    return image_urls


def download_image(download_path, url, file_name, max_images1=max_images1):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
            print("Success")

    except Exception as e:
        print(url)
        print('FAILED -', e)


urls = get_images_from_google(wd, 1, max_images1, skips=0)

for i, url1 in enumerate(urls):
    down_path = f'images/Balloons!/'  # change to wherever you want the images to
    # down_path = f'images/back_Of_Persons/'          # in same directory as main code
    # down_path = f'images/front_Of_Persons/'
    # down_path = f'images/side_Of_Persons/'

    download_image(down_path, url1, str(i) + ".jpg")

wd.quit()
