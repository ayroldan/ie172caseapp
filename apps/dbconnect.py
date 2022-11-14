import psycopg2
import pandas as pd

def getdblocation():
    # Define your connection details
    db = psycopg2.connect(
        # Get your credentials from the pgadmin. More details below.
        host='localhost',
        database='172casedb',
        user='postgres',
        port=5432,
        password='accessdenied'
    )
    # return the connection details
    return db


def modifydatabase(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()


def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows
