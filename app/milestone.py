import sqlite3
from mosql.query import insert, select
try:
    from db import r
except:
    r = None

SQLITE_DB = 'milestone.db'


def init_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE milestone
                 (mindex integer primary key, hash text not null, timestamp datetime,
                  branch text, trunk text, trunkb text, trunkt text)''')
    conn.commit()


def insert_milestone(index, c):
    try:
        mindex, txh = r.get(index, 'milestone')
    except TypeError:
        print(i)
    tx = r.get(txh, 'transaction')
    b1 = r.get(tx.trunk_transaction_hash, 'transaction')
    c.execute(insert('milestone',
        dict(mindex=mindex, hash=str(txh), timestamp=tx.timestamp,
             trunk=str(tx.trunk_transaction_hash),
             branch=str(tx.branch_transaction_hash),
             trunkt=str(b1.trunk_transaction_hash),
             trunkb=str(b1.branch_transaction_hash))))    


def init_db(conn):
    c = conn.cursor()
    index, m = r.latest('milestone')
    for i in range(243001, index + 1):
        insert_milestone(i, c)
    conn.commit()


def update_db(conn):
    c = conn.cursor()
    db_mindex = get_latest_index(c)
    t_mindex, _ = r.latest('milestone')
    if db_mindex != t_mindex:
        print(f'Update db milestone: from {db_mindex} to {t_mindex}')

    for i in range(db_mindex + 1, t_mindex + 1):
        insert_milestone(i, c)
    conn.commit()
    conn.close()    


def connect(path=SQLITE_DB):
    return sqlite3.connect(path)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_latest_index(cursor=None):
    if not cursor:
        conn = connect()
        c = conn.cursor()
    else:
        c = cursor
    index = c.execute('SELECT MAX(mindex) FROM milestone').fetchone()[0]
    if not cursor:
        conn.close()
    return index


def get_milestone_by_index(index):
    conn = connect()
    conn.row_factory = dict_factory
    c = conn.cursor()
    obj = c.execute(select('milestone', {'mindex': index})).fetchone()
    conn.close()
    return obj


def get_milestone(cond):
    conn = connect()
    conn.row_factory = dict_factory
    c = conn.cursor()
    obj = c.execute(select('milestone', cond, order_by=('mindex desc',))).fetchall()
    conn.close()
    return obj
    

if __name__ == '__main__':
    conn = connect('../milestone.db')
    update_db(conn)