from AlexZapl_db import db

tables = ['users', 'history', 'card']
table = tables[0]
id_ = 1


def delline(table, id_, delall=False):
    if not delall:
        if table == "users":
            db.users.delete('id', id_)
        elif table == "history":
            db.history.delete('userid', id_)
        elif table == "card":
            db.card.delete('userid', id_)
    if delall:
        if table == "users":
            baseall = db.users.get_all()
            for row in baseall:
                db.users.delete('id', row.id)
        elif table == "history":
            baseall = db.history.get_all()
            for row in baseall:
                db.history.delete('userd', row.userid)
        elif table == "card":
            baseall = db.card.get_all()
            for row in baseall:
                db.card.delete('userid', row.userid)

def delbaseall():
    global tables
    for table in tables:
        delline(table, 0, delall=True)

#delline(table, id_, delall=True)
delbaseall()