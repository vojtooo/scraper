# Import libraries
import os
import psycopg2
from flask import Flask, render_template

# Define app
app = Flask(__name__)

# Define connection
def get_db_connection():
    conn = psycopg2.connect(host='db',
                            database='sreality',
                            user="postgres",
                            password="pass")
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM flats_sell;') # flats_sell is the name of the table
    properties = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', properties=properties)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)