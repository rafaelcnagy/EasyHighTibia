def search_date(char, driver):
    driver.get(f'https://guildstats.eu/character?nick={char.name}#tab2')
    char.online_time = driver.find_element_by_xpath('//table[@id="myTable"]//td[2]').text
    return char
