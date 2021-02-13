FROM python:3.7

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils default-jdk

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Copy local code to the container image.
COPY . /EasyHigh
WORKDIR /EasyHigh

# Install Python dependencies.
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev -vvv

# Config config file.
RUN cp config.ini.example config.ini
RUN sed -r '/account_name/ c account_name = $steam_account_name' config.ini > config.ini
RUN sed -r '/password/ c password = $steam_password' config.ini > config.ini

# Download selenium driver
RUN wget https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
