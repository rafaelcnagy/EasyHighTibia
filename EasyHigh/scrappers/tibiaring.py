import time
from datetime import datetime

from parsel import Selector
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from models import Character, Frag

from config import STEAM_ACCOUNT, STEAM_PASSWORD, SELENIUM_PATH


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

    html = driver.page_source
    sel = Selector(html)

    if sel.xpath('//div[@id="gworld"]'):
        row = sel.xpath(f'//div[@id="gworld"]//tr[td[2]="{name}"]')
        char.ranking_position = row.xpath('./td[1]/text()').extract_first()
        char.points = row.xpath('./td[3]/text()').extract_first()

    if sel.xpath('//div[@id="mtChar"]/div[2]/text()'):
        char.traded = True
        char.trade_info = '\n'.join(sel.xpath('//div[@id="mtChar"]/div[2]/text()').extract())

    if sel.xpath('//*[contains(@class, "table chartable")]'):
        char.kills = get_kills(sel, name)
        char.deaths = get_deaths(sel, name)

    char.frags.extend(char.kills)
    char.frags.extend(char.deaths)
    char.frags.sort(key=lambda x: x.date, reverse=True)

    return char


def initialize_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("user-data-dir=selenium")

        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=SELENIUM_PATH)
    except Exception as e:
        driver = webdriver.Chrome(executable_path=SELENIUM_PATH)

    driver.get('https://www.tibiaring.com')

    if driver.find_elements_by_xpath('//a[@class="LinkHot b" and text()="Login"]'):
        login(driver)
    return driver


def get_kills(sel, name):
    table = sel.xpath('//*[contains(@class, "table chartable")]')

    kills = list()
    target_column_index = get_column_index(table)

    for row in table.xpath(f'.//tr[td[{target_column_index}]/a/text()="{name}"]'):
        date = row.xpath(".//td[1]/text()").extract_first()
        target_name = row.xpath(".//td[2]//text()").extract_first()
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

        frag = Frag(date, target_name, target_level, frag_type, is_kill=True)
        frag.add_killer(name, char_level)
        kills.append(frag)

    return kills


def get_deaths(sel, name):
    table = sel.xpath('//*[contains(@class, "table chartable")]')

    deaths = list()
    last_death = None
    target_column_index = get_column_index(table)

    for row in table.xpath(f'.//tr[td[2]/a/text()="{name}"]'):
        date = row.xpath(".//td[1]/text()").extract_first()
        killer_name = row.xpath(f".//td[{target_column_index}]//text()").extract_first()
        killer_level = row.xpath(f".//td[{target_column_index+1}]/text()").extract_first()

        if row.xpath('@class') != 'h':
            if last_death and last_death.killers:
                deaths.append(last_death)

            target_level = row.xpath(".//td[3]/text()").extract_first()

            frag_type_css = row.xpath(f".//td[{target_column_index}]/@class").extract_first()
            if frag_type_css.startswith('CSC s'):
                frag_type = 'justified'
            elif frag_type_css.startswith('CSC k'):
                frag_type = 'injustified'
            else:
                frag_type = 'other'

            date = datetime.strptime(date, '%Y-%m-%d %H:%M')

            last_death = Frag(date, name, target_level, frag_type, is_kill=False)

        if killer_level and killer_name != name:
            last_death.add_killer(killer_name, killer_level)

    if last_death and last_death.killers:
        deaths.append(last_death)

    return deaths


def get_column_index(table):
    qtd_columns = len(table.xpath('.//th').extract())
    if qtd_columns == 7:
        return 5
    elif qtd_columns == 5:
        return 4
    else:
        raise NotImplementedError
