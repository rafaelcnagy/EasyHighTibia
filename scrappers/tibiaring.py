import time
from datetime import datetime

from parsel import Selector
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from models import Character, Frag

from config import STEAM_ACCOUNT, STEAM_PASSWORD


def login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(lambda _driver: _driver.find_element_by_xpath('//a[@class="LinkHot b" and text()="Login"]'))

    login_button = driver.find_element_by_xpath('//a[@class="LinkHot b" and text()="Login"]')
    ActionChains(driver).move_to_element(login_button).perform()
    
    driver.find_element_by_xpath('//*[@onclick="document.location = \'/tr/steam/login.php\'"]').click()
    driver.find_element_by_id("steamAccountName").send_keys(STEAM_ACCOUNT)
    driver.find_element_by_id("steamPassword").send_keys(STEAM_PASSWORD)
    driver.find_element_by_id("imageLogin").click()
    wait = WebDriverWait(driver, 10)
    wait.until(lambda _driver: _driver.current_url.startswith("https://www.tibiaring.com"))


def search_char(char: Character, driver):
    name = char.name

    url = f'https://www.tibiaring.com/char.php?c={name.replace(" ", "+")}&lang=pt'
    driver.get(url)
    if driver.find_elements_by_id('CookieAlertClose'):
        driver.find_element_by_id('CookieAlertClose').click()
    try:
        while True:
            driver.find_element_by_xpath('//*[@class="LinkStd lgnel gra"]').click()
            time.sleep(.2)
    except Exception as e:
        pass

    if driver.find_elements_by_xpath('//div[@id="gworld"]'):
        row = driver.find_element_by_xpath(f'//div[@id="gworld"]//tr[td[2]="{name}"]')
        char.ranking_position = row.find_element_by_xpath('./td[1]').text
        char.points = row.find_element_by_xpath('./td[3]').text

    if driver.find_elements_by_xpath('//*[contains(@class, "table chartable")]'):
        html = driver.page_source
        char.kills = get_kills(html, name)
        char.deaths = get_deaths(html, name)

    return char


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://www.tibiaring.com')

    if driver.find_elements_by_xpath('//a[@class="LinkHot b" and text()="Login"]'):
        login(driver)
    return driver


def get_kills(html, name):
    table = Selector(html).xpath('//*[contains(@class, "table chartable")]')

    kills = list()
    target_column_index = get_column_index(table)

    for row in table.xpath(f'.//tr[td[{target_column_index}]/a/text()="{name}"]'):
        date = row.xpath(".//td[1]/text()").extract_first()
        target_name = row.xpath(".//td[2]/text()").extract_first()
        target_level = row.xpath(".//td[3]/text()").extract_first()
        char_level = row.xpath(f".//td[{target_column_index+1}]/text()").extract_first()

        frag_type_css = row.xpath(f".//td[{target_column_index}]/@class").extract_first()
        if frag_type_css.startswith('CSC s'):
            frag_type = 'justified'
        elif frag_type_css.startswith('CSC k'):
            frag_type = 'injustified'
        else:
            frag_type = 'other'

        if row.xpath('@class').extract_first() == 'h' or target_name == name:
            continue

        date = datetime.strptime(date, '%Y-%m-%d %H:%M')

        # print(f'{name}({char_level}) killed {target_name}({target_level}) at {date}')
        frag = Frag(date, target_name, target_level, frag_type)
        frag.add_killer(name, char_level)
        kills.append(frag)

    print(f'{name}: {len(kills)} kills')
    return kills


def get_deaths(html, name):
    table = Selector(html).xpath('//*[contains(@class, "table chartable")]')

    deaths = list()
    last_death = None
    target_column_index = get_column_index(table)

    for row in table.xpath(f'.//tr[td[2]/a/text()="{name}"]'):
        date = row.xpath(".//td[1]/text()").extract_first()
        killer_name = row.xpath(f".//td[{target_column_index}]/text()").extract_first()
        killer_level = row.xpath(f".//td[{target_column_index+1}]/text()").extract_first()

        if row.xpath('@class') != 'h':
            if last_death and last_death.killers:
                deaths.append(last_death)
                # print(f'{name}({last_death.target.level}) dead by {",".join([f"{killer.name}({killer.level})" for killer in last_death.killers])} at {date}')

            target_level = row.xpath(".//td[3]/text()").extract_first()

            frag_type_css = row.xpath(f".//td[{target_column_index}]/@class").extract_first()
            if frag_type_css.startswith('CSC s'):
                frag_type = 'justified'
            elif frag_type_css.startswith('CSC k'):
                frag_type = 'injustified'
            else:
                frag_type = 'other'

            date = datetime.strptime(date, '%Y-%m-%d %H:%M')

            last_death = Frag(date, name, target_level, frag_type)

        if killer_level and killer_name != name:
            last_death.add_killer(killer_name, killer_level)

    if last_death and last_death.killers:
        deaths.append(last_death)
        # print(f'{name}({last_death.target.level}) dead by {",".join([f"{killer.name}({killer.level})" for killer in last_death.killers])} at {date}')

    print(f'{name}: {len(deaths)} deaths')

    return deaths


def get_column_index(table):
    qtd_columns = len(table.xpath('.//th').extract())
    if qtd_columns == 7:
        return 5
    elif qtd_columns == 5:
        return 4
    else:
        raise NotImplementedError
