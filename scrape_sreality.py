# Import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from sqlalchemy import create_engine

# set number of properties required
NUM_PROPERTIES_REQUIRED = 50 # 0

if __name__ == '__main__':
    
    properties_list = []    
    page_num = 1
    enough_properties = False

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')  ### optional

    # Create a webdriver instance with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    while not enough_properties:
        # Define URL
        base_url = "https://www.sreality.cz/hledani/prodej/byty?strana=" + str(page_num)
        driver.get(base_url)
        time.sleep(3)
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down until no more content is loaded
        while True:
            # scrolling once code
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # giving time to load
            time.sleep(3)  # wait for content to load

            # checking new height of webpage
            new_height = driver.execute_script("return document.body.scrollHeight")

            # defining the break condition to stop the execution at the end of the webpage
            if new_height == last_height:
                break
            last_height = new_height

        # Initialize BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Parse the page source and find all properties
        properties = soup.find_all("div", class_="property ng-scope")
        print("INFO: Number of newly discovered properties", len(properties))

        # For each property
        for property in properties:
            property_description = property.find("a", class_="title")
            # Get parameters
            property_title = property_description.find("span", class_="name ng-binding").text
            property_url = "https://www.sreality.cz" + property_description["href"]
            imgs_list = [img["src"] for img in property.find_all("img")]
            properties_list.append([property_title, property_url, imgs_list, imgs_list[0]])

        # Break if we have enough properties listed
        if len(properties_list) >= NUM_PROPERTIES_REQUIRED:
            enough_properties = True
            break

        page_num += 1
    print("INFO: sreality scraped.")

    # Convert list into a pandas dataframe
    df = pd.DataFrame(properties_list, columns=['PropertyTitle', 'PropertyURL', 'PropertyImgs', 'PropertySampleImage'])

    # Save pandas dataframe as a pickle file (which is processable by fill_database.py)
    df.to_pickle("./pd_scraped_properties.pkl")
    print("INFO: sreality data saved as pickle.")

    # Connect to the Postgresql database and fill the flats_sell table
    engine = create_engine('postgresql+psycopg2://postgres:pass@db:5432/sreality')
    df.to_sql('flats_sell', engine, if_exists='replace')
    print("INFO: sreality data sent to database")

    driver.quit()

