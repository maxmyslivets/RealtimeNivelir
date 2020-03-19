""" Просмотр базы данных
Запускать только из папки, иначе не работает
"""
import sqlite3 as sql

con = sql.connect('testRN.db')
with con:
    cur = con.cursor()
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print('Таблицы:', tables)

    if len(tables) != 0:
        print('\nТаблицы:')
        for table in tables:
            print(table)

    if len(tables) != 0:
        for table in tables:
            print('\nТаблица:', table[0], '\n')
            rows = cur.execute("SELECT * FROM "+table[0]).fetchall()
            if len(rows) != 0:
                for row in rows:
                    print(row)
            else: 'В таблице нет строк'
    else:
        print('В базе данных нет таблиц')
    cur.close()
input()