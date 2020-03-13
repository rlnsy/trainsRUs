from flask import Flask
from db import poll_db

app = Flask(__name__)

@app.route('/')
def hello():
    db_connection = poll_db(app)
    # create a psycopg2 cursor that can execute queries
    cursor = db_connection.cursor()
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from trains""")
    db_connection.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return str(rows)


if __name__ == "__main__":
    poll_db(app)
    app.run(host="0.0.0.0") # TODO change to env variable
