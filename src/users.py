import articles
import database
import sessions
import numpy as np

class User:
    def __init__(self, name, un, pw, prefs=None, n=0) -> None:
        self.name = name
        self.un = un
        self.pw = pw
        self.n = n
        self.prefs = np.zeros(25) if prefs is None else np.frombuffer(prefs).copy()

    def into_database(self):
        return database.insert_into(
            "users",
            ("name", "username", "pass", "prefs", "n"),
            (self.name, self.un, self.pw, self.prefs.tobytes(), self.n)
        )
    
    def update_database(self):
        cur = database.get_cursor()
        cur.execute("""UPDATE users 
SET name=?, pass=?, prefs=?, n=?
WHERE username=?""", (self.name, self.pw, self.prefs.tobytes(), self.n, self.un))
        database.commit()

    def update_preferences(self, sessionid, model):
        entries = sessions.get_events(sessionid)
        read_events = list(filter(
            lambda i: entries[i][2]=="READ",
            range(len(entries))
        ))
        print(f"{self.name} read {len(read_events)} articles")
        for event_idx in read_events:
            print(entries[event_idx][3])
            article = articles.get_article(entries[event_idx][3])
            interaction_time = entries[event_idx+1][1] - entries[event_idx][1]
            self.prefs = model.new_user_prefs(self, article, article.rating_from_interaction(interaction_time))
            self.n += 1
        self.update_database()
    
def try_login(un, pw):
    rows = database.exec_select("SELECT * FROM users WHERE username=? and pass=?", (un, pw))
    if len(rows) == 1:
        return sessions.start_session(un)

def try_signup(nm, un, pw):
    u = User(nm, un, pw)
    success = u.into_database()
    if success:
        return sessions.start_session(un)
    return None

def getuser(un):
    rows = database.exec_select("SELECT * FROM users WHERE username=?", (un,))
    if len(rows) == 1:
        return User(*rows[0])
    return None

def get_all_users():
    rows = database.exec_select("SELECT * FROM users", ())
    return [User(*row) for row in rows]
    
