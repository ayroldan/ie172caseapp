import apps.dbconnect as db
from datetime import datetime

def addfewgenres():

    sqlcode = """ INSERT INTO genres (
        genre_name,
        genre_modified_on
    )
    VALUES (%s, %s)"""

    db.modifydatabase(sqlcode, ['Action', datetime.now()])
    db.modifydatabase(sqlcode, ['Horror', datetime.now()])

    print('Done!')

sql_resetgenres = """
    TRUNCATE TABLE genres RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetgenres, [])
addfewgenres()

# Get Query from database
sql = 'SELECT * FROM genres'
values = []
colnames = ['id', 'name', 'mod_on', 'del_ind']

print(db.querydatafromdatabase(sql, values, colnames))
