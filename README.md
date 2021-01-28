# EasyHighTibia
EasyHigh facilitate the analysis of player activity in a Tibia war team. 
It was done thinking about the use of Zenobra Pune, a guild of Tibia. 

Searching by the TeamSpeak description of a player, the EasyHigh search data about all the 
player's characters in differents sources and joins that in a single page.

It was made using *flask*, *selenium* and *requests*.

## TeamSpeak description
The search based in my team's pattern TeamSpeak description, so, needs to follow this pattern:

    {player's name} - Main: {character's name} | {world}: {character's name} | {world}: {character's name} ... | Reg: {leader name}

## Sources:
- [TibiaRing](http://www.tibiaring.com/)
- [GuildStats](https://guildstats.eu/)
- [TibiaData](https://tibiadata.com/)

# Instalation

## Requiriments
```
- Python 3.7+
- poetry
- Selenium
```

### Install poetry env
```
poetry install
```

### Download Chrome driver
 
```
https://sites.google.com/a/chromium.org/chromedriver/downloads
```
Unzip and copy `chromedriver` to project's root folder.

### Setting credentials
Create an `config.ini` file:
```
cp config.ini.example config.ini
```
Set *account name* and *password* of a Steam account in `config.ini`.
The account must have steam guard **disabled**.

> TibiaRing requires a login to show all character history.

### Running
Active the poetry's shell:
```
poetry shell
```
Set the `FLASK_APP` environment variable.

- Windows:
    ```
    export FLASK_APP=main.py
    ```
- Linux/Mac:
    ```
    set FLASK_APP=main.py
    ```
and, finally, run flask app.
```
flask run
```