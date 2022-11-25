import sqlite3 as sq
import datetime
from datetime import date
import random

def sql_start():
    global base, cur
    base = sq.connect("landings/db.db")
    cur = base.cursor()
    if base:
        print('OK')
    base.execute("CREATE TABLE IF NOT EXISTS data(idi INTEGER PRIMARY KEY, name TEXT, status TEXT, fr TEXT, opit TEXT, inf TEXT, username TEXT, time TEXT, tag TEXT, profit INTEGER, parentid INTEGER)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS payments(idi INTEGER PRIMARY KEY, usdt TEXT)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS landings(idi INTEGER PRIMARY KEY, name TEXT, price INTEGER, na TEXT, adress TEXT, landing TEXT, idpar INTEGER)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS global(idi INTEGER, CZ INTEGER, HU INTEGER)")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS PROFITS(num INTEGER, idi INTEGER, time TEXT, summ INTEGER, status TEXT, land TEXT, worker INTEGER, rub INTEGER)")
    base.commit()


async def sql_add_command(name, idi, usdt, username, tag, parentid):
    cur.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (idi, name, 'new', '-', '-', '-', username, '-', tag, 0, parentid))
    base.commit()
    if cur.execute(f"SELECT *  FROM payments WHERE idi = {idi}").fetchone() is None:
        cur.execute('INSERT INTO payments VALUES (?, ?)', (idi, usdt))
        base.commit()

#____________________PROFITS_________________
async def sql_profit_add(idi, land):
    r = random.randint(1000, 1000000)
    try:
        cur.execute('INSERT INTO PROFITS VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (r, idi, date.today(), 0, 'в обработке', land, -1, 0))
        base.commit()
    except:
        await sql_profit_add(r + 1, land)


async def sql_profit_price(idi, summ):
    cur.execute(f'UPDATE PROFITS SET summ = {summ} WHERE idi = {idi} AND worker = -1')
    base.commit()

async def sql_profit_rub(idi, rub):
    cur.execute(f'UPDATE PROFITS SET rub = {rub} WHERE idi = {idi} AND worker = -1')
    base.commit()

async def sql_profit_worker(idi, worker):
    cur.execute(f'UPDATE PROFITS SET worker = {worker} WHERE idi = {idi} AND worker = -1')
    base.commit()


async def sql_profit_statude(idi):
    cur.execute(f'UPDATE PROFITS SET status = выплачен WHERE num = {idi}')
    base.commit()

def sql_check_profit_inf(idi):
    d = []
    d.append(cur.execute(f'SELECT land FROM PROFITS WHERE idi = {idi} AND worker = -1').fetchone()[0])
    d.append(cur.execute(f'SELECT summ FROM PROFITS WHERE idi = {idi} AND worker = -1').fetchone()[0])
    return d

def sql_profit_summ_worker(idi):
    return cur.execute(f'SELECT SUM(rub) FROM PROFITS WHERE worker = {idi}').fetchone()[0]


def sql_profit_count_worker(idi):
    return cur.execute(f'SELECT COUNT(*) FROM PROFITS WHERE worker = {idi}').fetchone()[0]

#____________________DELEte___________________
async def sql_delete_landing(parentid):
    cur.execute(f"DELETE from landings WHERE idpar = {parentid} AND adress = '-' ")
    base.commit()

async def sql_delete_time(idi):
    try:
        cur.execute(f"DELETE from landings WHERE idi = {idi}")
        base.commit()
    except:
        return

async def sql_delete_all_land(idi):
    cur.execute(f"DELETE from landings WHERE idpar = {idi}")
    base.commit()

async def sql_delete_one_land(idi):
    cur.execute(f"DELETE from landings WHERE idi = {idi}")
    base.commit()


async def sql_delete_profit(idi):
    cur.execute(f"DELETE from PROFITS WHERE idi = {idi} AND worker = -1")
    base.commit()
#____________________ZASIL_______________
async def sql_add_command_zasil(parentid, idi, landing):

    if cur.execute(f"SELECT name FROM landings WHERE idi = {idi}").fetchone() is None:
        cur.execute('INSERT INTO landings VALUES (?, ?, ?, ?, ?, ?, ?)', (idi, '-', 0, '-', '-', landing, parentid))
        base.commit()
        return idi
    else:
        await sql_add_command_zasil(parentid, idi + 1, landing)

async def sql_update_name_landings(name, idi):
    cur.execute(f"UPDATE landings SET name = '{name}' WHERE idpar = {idi} AND adress = '-'")
    base.commit()


async def sql_update_price_landings(price, idi):
    cur.execute(f"UPDATE landings SET price = {price} WHERE idpar = {idi} AND adress = '-'")
    base.commit()


async def sql_update_na_landings(na, idi):
    cur.execute(f"UPDATE landings SET na = '{na}' WHERE idpar = {idi} AND adress = '-'")
    base.commit()


async def sql_update_adress_landings(adress, idi):
    cur.execute(f"UPDATE landings SET adress = '{adress}' WHERE idpar = {idi} AND adress = '-'")
    base.commit()


def sql_select_idiland_first(idi):
    return cur.execute(f"SELECT idi FROM landings WHERE adress = '-' AND idpar = {idi}").fetchone()[0]



def sql_select_information_(idi):
    a = []
    a.append(cur.execute(f"SELECT name FROM landings WHERE idi = {idi}").fetchone()[0])
    a.append(cur.execute(f"SELECT price FROM landings WHERE idi = {idi}").fetchone()[0])
    a.append(cur.execute(f"SELECT na FROM landings WHERE idi = {idi}").fetchone()[0])
    a.append(cur.execute(f"SELECT adress FROM landings WHERE idi = {idi}").fetchone()[0])
    a.append(cur.execute(f"SELECT landing FROM landings WHERE idi = {idi}").fetchone()[0])
    return a

def rtrt(idi):
    res = []
    tr = cur.execute(f"SELECT idi FROM landings WHERE idpar = {idi}").fetchall()
    for i in tr:
        res.append(i[0])
    return res



def sql_usdt(idi):
    return cur.execute(f"SELECT usdt FROM payments WHERE idi = {idi}").fetchone()[0]


def sql_kassa():
    tn = [cur.execute(f"SELECT SUM(rub) FROM PROFITS").fetchone()[0]]
    tn.append(cur.execute(f"SELECT SUM(rub) FROM PROFITS WHERE time = '{date.today()}'").fetchone()[0])
    return tn


async def sql_update_usdt(idi, text):
    cur.execute(f'UPDATE payments SET usdt == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_time(idi, text):
    cur.execute(f'UPDATE data SET time == ? WHERE idi == ?', (text, idi))
    base.commit()


def check_referals(idi):
    res = ''
    r = cur.execute(f"SELECT username FROM data WHERE parentid = {idi}").fetchall()
    for i in r:
        res += '@' + str(i[0]) + '\n'
    if res == '':
        res = 'Отсутствуют'
    return res


def check_time(idi):
    return cur.execute(f"SELECT time FROM data WHERE idi = {idi}").fetchone()[0]


def check_time1(username):
    return cur.execute(f"SELECT time FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def check_status(idi):
    return cur.execute(f"SELECT status FROM data WHERE idi = {idi}").fetchone()[0]


def check_paytag(idi):
    return cur.execute(f"SELECT tag FROM data WHERE idi = {idi}").fetchone()[0]


def check_paytag1(tag):
    return cur.execute(f"SELECT idi FROM data WHERE tag = '{tag}'").fetchone()


async def sql_update_fr(idi, text):
    cur.execute(f'UPDATE data SET fr == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_tag(idi, text):
    cur.execute(f'UPDATE data SET tag == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_opit(idi, text):
    cur.execute(f'UPDATE data SET opit == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_inf(idi, text):
    cur.execute(f'UPDATE data SET inf == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_status(idi, text):
    cur.execute(f'UPDATE data SET status == ? WHERE idi == ?', (text, idi))
    base.commit()


async def sql_update_name(idi, name, username):
    cur.execute(f'UPDATE data SET name == ? WHERE idi == ?', (name, idi))
    base.commit()
    cur.execute(f'UPDATE data SET username == ? WHERE idi == ?', (username, idi))
    base.commit()


def check_fr(idi):
    return cur.execute(f"SELECT fr FROM data WHERE idi = {idi}").fetchone()[0]


def check_opit(idi):
    return cur.execute(f"SELECT opit FROM data WHERE idi = {idi}").fetchone()[0]


def check_inf(idi):
    return cur.execute(f"SELECT inf FROM data WHERE idi = {idi}").fetchone()[0]

def check_parents(idi):
    return cur.execute(f"SELECT parentid FROM data WHERE idi = {idi}").fetchone()[0]


def check_fr1(username):
    return cur.execute(f"SELECT fr FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def check_opit1(username):
    return cur.execute(f"SELECT opit FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def check_inf1(username):
    return cur.execute(f"SELECT inf FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def check_status1(username):
    return cur.execute(f"SELECT status FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def sql_usdt1(username):
    r = cur.execute(f"SELECT idi FROM data WHERE username = '{username[1:]}'").fetchone()[0]
    return cur.execute(f"SELECT usdt FROM payments WHERE idi = {r}").fetchone()[0]


def sql_id1(username):
    return cur.execute(f"SELECT idi FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def sql_tag1(username):
    return cur.execute(f"SELECT tag FROM data WHERE username = '{username[1:]}'").fetchone()[0]


def get_all_idi():
    return cur.execute("SELECT idi FROM data").fetchall()

