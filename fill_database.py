# Import libraries
import pandas as pd
from sqlalchemy import create_engine

# Load data from the pickle file created by scrape_sreality.py
df = pd.read_pickle("pd_scraped_properties.pkl")
# print(df)

# Connect to the Postgresql database and fill the flats_sell table
engine = create_engine('postgresql+psycopg2://postgres:pass@db:5432/sreality')
df.to_sql('flats_sell', engine, if_exists='replace')
print("INFO: existing sreality data sent to database")