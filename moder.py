import sqlite3
import argparse
import os

db_path = os.path.abspath('db/TLC_db.db')

parser = argparse.ArgumentParser()
parser.add_argument('table', type=str)
parser.add_argument('id', type=int)

args = parser.parse_args()

con = sqlite3.connect(db_path)

cur = con.cursor()
if args.table == 'users':
    del_mes_res = cur.execute(f'''DELETE FROM messages WHERE author_id = {args.id}''')
    threads_id = cur.execute(f'''SELECT id FROM threads WHERE author_id = {args.id}''').fetchall()
    if threads_id:
        for thread in threads_id[0]:
            cur.execute(f'''DELETE FROM messages WHERE thread_id = {thread}''')
    del_thr_res = cur.execute(f'''DELETE FROM threads WHERE author_id = {args.id}''')
    rev_id = cur.execute(f'''SELECT id FROM reviews WHERE author_id = {args.id}''').fetchall()
    del_pic_res = cur.execute(f'''DELETE FROM review_pictures WHERE review_id = {rev_id[0][0]}''')
    del_rev_res = cur.execute(f'''DELETE FROM reviews WHERE author_id = {args.id}''')
if args.table == 'reviews':
    del_pic_res = cur.execute(f'''DELETE FROM review_pictures WHERE review_id = {args.id}''')
if args.table == 'threads':
    del_mes_res = cur.execute(f'''DELETE FROM messages WHERE thread_id = {args.id}''')
del_self_res = cur.execute(f'''DELETE FROM {args.table} WHERE id={args.id}''').fetchall()
con.commit()
con.close()
