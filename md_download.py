import os
import time
from bs4 import BeautifulSoup as bs
import requests
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def get_urls(base_url):
    response = requests.get(base_url, proxies = { "http": None, "https": None})

    soup = bs(response.content, "html.parser")
    menu_tag = soup.find_all(class_ = "uk-nav uk-nav-side")[1]

    urls = []
    titles = []
    levels = [0, 0, 0, 0]
    for li in menu_tag.find_all("div"):
        urls.append("http://www.liaoxuefeng.com" + li.a.get('href'))

        i = int(li['depth'])
        levels[i] += 1
        for c in range(i + 1, 4):
            levels[c] = 0
        titles.append('{:0=2d}.{}.{}{}'.format(levels[1], levels[2], levels[3], li.a.string))

    return urls, titles


def download_md(browser, url):
    # path='https://www.liaoxuefeng.com/wiki/1016959663602400/1017639890281664'
    browser.get(url)
    time.sleep(6)

    # 通过快捷键点击插件
    # pyautogui.click(800, 800)
    # pyautogui.hotkey('ctrl', 'q')

    # 通过定位图片点击简悦插件
    # image_path = os.environ.get("USERPROFILE") + r'\Desktop\a1.png'
    dirname, basename = os.path.split(os.path.realpath(__file__))
    image_path = os.path.join(dirname, "ext_icons.png")
    img_location = pyautogui.locateOnScreen(image = image_path, confidence = 0.5)
    image_location_point = pyautogui.center(img_location)
    x, y = image_location_point
    pyautogui.click(x, y)

    # 移动鼠标至三个点处
    anchor_button = browser.find_element(By.XPATH, '//*[@id="anchor"]')
    ActionChains(browser).move_to_element(anchor_button).perform()
    # 移动鼠标至动作标签页
    act_button = browser.find_element(By.XPATH, '/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-tabs/panel-tab[2]/span')
    ActionChains(browser).move_to_element(act_button).perform()
    # 点击导出为PDF
    # md_button = browser.find_element(By.XPATH, "/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-groups/panel-group[2]/action-bar/sr-opt-gp[2]/actions/action-item[3]")
    # 点击导出为Markdown
    md_button = browser.find_element(By.XPATH, "/html/div/sr-read/sr-rd-crlbar/fap/panel-bg/panel/panel-groups/panel-group[2]/action-bar/sr-opt-gp[2]/actions/action-item[5]")
    md_button.click()


# https://chromedriver.chromium.org/downloads
# file: chromedriver.exe  md5sum: 206b032735e207516d48e1354bcffe3e
options = webdriver.ChromeOptions()
profile_dir = os.environ.get("USERPROFILE") + r"\AppData\Local\Google\Chrome\User Data"
options.add_argument("--user-data-dir=" + profile_dir)
driver = webdriver.Chrome(chrome_options = options)

base_url = "https://www.liaoxuefeng.com/wiki/1252599548343744"
urls, titles = get_urls(base_url)

for url in urls:
    download_md(driver, url)

driver.close()
