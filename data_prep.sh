if [ -e /code/pd_scraped_properties.pkl ];
  then python fill_database.py;
  else python scrape_sreality.py;
fi
