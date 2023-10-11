## DockerSrealityScraper

***
#### Task specification 

Use scrapy framework to scrape the first 500 items (title, image url) from sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker compose command so that I can just run "docker-compose up" in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.
***
#### Solution description

The Docker image has three services:
1. ```db``` runs the PostgreSQL database
2. ```init-db``` fills the database with either new or existing data (based on existence of ```pd_scraped_properties.pkl```) 
3. ```web``` runs the webserver

The solution is divided into three parts:
1. ```scrape_sreality.py``` scrapes the sreality website, sends the data about the first 500 flats to sell to the PostgreSQL database and saves the data in ```pd_scraped_properties.pkl``` (to avoid repetitive scraping).
2. ```fill_database.py``` takes the scraped data file ```pd_scraped_properties.pkl``` and puts it into a PostgreSQL database
3. ```app.py``` runs a simple Flask webserver that shows the scraped data on a website

The solution is able to run using ```docker compose up```
***
#### Sources of help
- [data-scrapping-from-a-lazy-loading-website](https://www.kaggle.com/code/gauravrai2000/data-scrapping-from-a-lazy-loading-website)
- [create-a-sql-table-from-pandas-dataframe-using-sqlalchemy](https://www.geeksforgeeks.org/create-a-sql-table-from-pandas-dataframe-using-sqlalchemy/)
- [how-to-use-a-postgresql-database-in-a-flask-application](https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application)
- [containerize-a-redis-flask-app-with-docker-compose](https://sweetcode.io/containerize-a-redis-flask-app-with-docker-compose/)
- [build-a-flask-app-using-docker-compose](https://www.tutorialspoint.com/build-a-flask-app-using-docker-compose)
- [dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)
- [ChatGPT](https://chat.openai.com/)
- [wait-for-it](https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh)

