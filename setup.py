from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import selenium
from selenium.webdriver.common.keys import Keys
import os
import requests
import sys

username = f"{sys.argv[1]}"
password = f"{sys.argv[2]}"


def path():
    global chrome

    chrome = webdriver.Chrome('./chromedriver')


def url_name(url):
    chrome.get(url)
    sleep(4)


def login(username, your_password):
    log_but = chrome.find_element_by_class_name("L3NKy")
    sleep(2)
    log_but.click()
    sleep(2)

    usern = chrome.find_element_by_name("username")
    usern.send_keys(username)

    passw = chrome.find_element_by_name("password")
    passw.send_keys(your_password)
    passw.send_keys(Keys.RETURN)

    sleep(5.5)

    notn = chrome.find_element_by_class_name("yWX7d")
    notn.click()
    sleep(3)


def first_post():
    pic = chrome.find_element_by_class_name("kIKUG").click()
    sleep(2)


def save_multiple(img_name, elem, last_img_flag=False):
    sleep(1)
    l = elem.get_attribute('innerHTML')
    html = bs(l, 'html.parser')
    biglist = html.find_all('ul')
    biglist = biglist[0]
    list_images = biglist.find_all('li')
    if last_img_flag:
        user_image = list_images[-1]
    else:
        user_image = list_images[(len(list_images) // 2)]
    video = user_image.find('video')
    if video:
        link = video['poster']
    else:
        link = user_image.find('img')['src']
    response = requests.get(link)
    with open(img_name, 'wb') as f:
        f.write(response.content)


def nested_check():
    try:
        sleep(1)
        nes_nex = chrome.find_element_by_class_name('coreSpriteRightChevron  ')
        return nes_nex
    except selenium.common.exceptions.NoSuchElementException:
        return 0


# Function to save content of the current post
def save_content(class_name, img_name):
    sleep(0.5)

    try:
        pic = chrome.find_element_by_class_name(class_name)

    except selenium.common.exceptions.NoSuchElementException:
        print("Either This user has no images or you haven't followed this user or something went wrong")
        return

    html = pic.get_attribute('innerHTML')
    soup = bs(html, 'html.parser')
    link = soup.find('video')

    if link:
        link = link['poster']
    else:
        link = soup.find('img')['src']
    response = requests.get(link)
    with open(img_name, 'wb') as f:
        f.write(response.content)
    sleep(0.9)


def next_post():
    try:
        nex = chrome.find_element_by_class_name("coreSpriteRightPaginationArrow")
        return nex
    except selenium.common.exceptions.NoSuchElementException:
        return 0


def download_allposts():
    first_post()
    user_name = url.split("/")[-1]

    if (os.path.isdir(user_name) == False):
        os.mkdir(user_name)

    multiple_images = nested_check()

    if multiple_images:
        nescheck = multiple_images
        count_img = 0

        while nescheck:
            elem_img = chrome.find_element_by_class_name('rQDP3')
            save_multiple(user_name + '/img1.' + str(count_img) + ".jpg", elem_img)
            count_img += 1
            nescheck.click()
            nescheck = nested_check()
        
        save_multiple(user_name + '/img1.' + str(count_img) + ".jpg", elem_img, last_img_flag=1)
    else:
        save_content('_97aPb', user_name + '/img1' + ".jpg")
    c = 2

    while True:
        next_el = next_post()

        if next_el != False:
            next_el.click()
            sleep(1.3)

            try:
                multiple_images = nested_check()

                if multiple_images:
                    nescheck = multiple_images
                    count_img = 0

                    while nescheck:
                        elem_img = chrome.find_element_by_class_name('rQDP3')
                        save_multiple(user_name + '/img' + str(c) + '.' + str(count_img) + ".jpg", elem_img)
                        count_img += 1
                        nescheck.click()
                        nescheck = nested_check()
                    save_multiple(user_name + '/img' + str(c) + '.' + str(count_img) + ".jpg", elem_img, 1)
                else:
                    save_content('_97aPb', user_name + '/img' + str(c) + ".jpg")

            except selenium.common.exceptions.NoSuchElementException:
                print("Finished")
                return

        else:
            break

        c += 1


url = f"https://www.instagram.com/{sys.argv[3]}"
path()
sleep(1)
url_name(url)
login(username, password)
download_allposts()
chrome.close()
