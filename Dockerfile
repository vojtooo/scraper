#The Flask application container will use python:3.10-alpine as the base image
FROM python:3.8.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Chrome and ChromeDriver for Selenium
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg wget curl unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* && \
    CHROME_VERSION=$(google-chrome --product-version) && \
    wget -q --continue -P /chromedriver "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/ && \
    rm -rf /chromedriver

# Set display port as an environment variable
ENV DISPLAY=:99

#This command will create the working directory for our Python Flask application Docker image
WORKDIR /code
#This command will copy the dependencies and libraries in the requirements.txt to the working directory
COPY requirements.txt /code
#This command will install the dependencies in the requirements.txt to the Docker image
RUN python -m pip install -r requirements.txt --no-cache-dir
#This command will copy the files and source code required to run the application
COPY . /code
RUN chmod +x /code/data_prep.sh
RUN chmod +x /code/wait-for-it.sh
# Check if pd_scraped_properties.pkl file exists, if not install chromium and perform scraping
# RUN test -f pd_scraped_properties.pkl || (RUN apt-get update && apt-get -y install chromium-driver && python scrape_sreality.py)
#This command will start the Python Flask application Docker container
CMD python app.py
EXPOSE 8080