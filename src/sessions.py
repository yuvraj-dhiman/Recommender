import database
import time

def start_session(un):
    already = getsession_un(un)
    if already:
        add_event(already[0], "REACCESS", already[0])
        return already[0]
    tnow = int(time.time())
    id = str(tnow)+un
    success = database.insert_into(
        "sessions",
        ("id", "starttime", "username", "active"),
        (str(tnow)+un, tnow, un, True)
    )
    if success:
        add_event(id, "CREATE", id)
        return id
    return None

def getsession_un(un):
    rows = database.exec_select("SELECT * from sessions WHERE active=1 AND username=?", (un,))
    print(rows)
    if len(rows) == 1:
        return rows[0]
    return False

def getsession(id):
    rows = database.exec_select("SELECT * from sessions WHERE active=1 AND id=?", (id,))
    if len(rows) == 1:
        return rows[0]
    return None

def stop_session(id):
    add_event(id, "END_SESSION", id)
    curr = database.get_cursor()
    curr.execute("UPDATE sessions SET active=0 WHERE id=?", (id,))

def add_event(id, event, value):
    database.insert_into("events", ("id", "event", "value", "time"), (id, event, value, int(time.time())))

def get_events(session_id):
    return database.exec_select("SELECT * from events WHERE id=?", (session_id,))

