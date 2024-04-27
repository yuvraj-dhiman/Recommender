import sqlite3
import numpy as np
import io

CONN = None

def get_cursor():
    global CONN
    if CONN is None:
        CONN = sqlite3.connect("news-recommender.db", check_same_thread=False)
    return CONN.cursor()

def commit():
    global CONN
    if CONN is not None:
        CONN.commit()

def insert_into(tblname, keys, values):
    cur = get_cursor()
    try:
        pld = "(" + ", ".join(["?" for _ in keys]) + ")"
        cur.execute(f"""INSERT INTO {tblname} {keys} VALUES {pld}""", values)
        cur.close()
        commit()
        return True
    except BaseException as e:
        print(e)
        return False

def exec_select(query, vals):
    cur = get_cursor()
    return cur.execute(query, vals).fetchall()
    

