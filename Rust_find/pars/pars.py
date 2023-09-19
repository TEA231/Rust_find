from bs4 import BeautifulSoup
import requests
import time
import psycopg2
from config import host, user, password, db_name
from fake_useragent import UserAgent


try:
    con = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name 
        )

    cur = con.cursor()

    cur.execute('''CREATE TABLE servers_p
                (name_s TEXT,
                old_s TEXT,
                online_s TEXT,
                connect_s TEXT, 
                online_id_s INT);''')

    cur.execute('''CREATE TABLE servers_l
                (name_s TEXT,
                old_s TEXT,
                online_s TEXT,
                connect_s TEXT,
                online_id_s INT);''')

    print('таблицы успешно созданы')
    con.commit()
    con.close()

except:
    pass


ua = UserAgent()

def pirate_servers():
    header = {'User-Agent': ua.random}

    url = 'https://expshop.alkad.org/launcher/'

    respone = requests.get(url, headers=header)

    soup = BeautifulSoup(respone.text, 'html.parser')

    articles = soup.find_all('tr', class_='type_prem')
    articles2 = soup.find_all('tr', class_='type_vip')
    articles3 = soup.find_all('tr', class_='type_norm')

    articles_all = articles + articles2 + articles3

    classics = []

    for index in articles_all:
        if 'classic' in index.find('a').text.lower() or 'vanilla' in index.find('a').text.lower():
            classics.append(index)

    classics2 = []

    for index in classics:
        try:
            name_s = index.find('a').text
            old_s = ''
            for index2 in index.find_all('span', class_='badge badge-success'):
                if 'Вайп был' in index2.text:
                    old_s = index2.text
            online_s = index.find('td', class_='td_online').text
            connect_s = index.find('div', class_='server_addr').text
            online_id_s = online_s.split('/')[0]
            classics2.append({'name_s': name_s, 'old_s': old_s, 'online_s': online_s, 'connect_s': connect_s, 'online_id_s': online_id_s})
        except:
            pass

    return classics2


def licensed_servers():
    articles_all = []

    for index in range(1, 10):

        header = {'User-Agent': ua.random}

        url = f'https://tsarvar.com/ru/servers/rust?page={index}'

        respone = requests.get(url, headers=header)

        soup = BeautifulSoup(respone.text, 'html.parser')

        articles = soup.find_all('li', class_='serversList-item')
        articles = soup.find_all('li', class_='serversList-item')

        for article in articles:
            name_s = article.find('span', class_='serversList-itemName').text

        for article in articles:
            name_s = article.find('span', class_='serversList-itemName').text
            try:
                if ('vanilla' in name_s.lower() or 'classic' in name_s.lower()) and int(
                        article.find('span', class_='serversList-itemPlayersCur').text) >= 0:
                    items = article.select('span.serversList-itemName a')
                    link = [item['href'] for item in items][0]
                    connect_s = 'connect ' + link.split('/')[-1]
                    online_s = article.find('span', class_='serversList-itemPlayersCur').text + '/' + article.find(
                        'span', class_='serversList-itemPlayersMax').text
                    online_id_s = article.find('span', class_='serversList-itemPlayersCur').text
                    articles_all.append({'name_s': name_s, 'old_s': '', 'online_s': online_s, 'connect_s': connect_s, 'online_id_s': online_id_s})
            except:
                pass

    return articles_all


while True:
    con = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    print('База данных успешно открыта')
    try:
        cur = con.cursor()

        cur.execute('''DELETE FROM servers_p''')
        con.commit()
        print('Таблица пиратских серверов успешно очищена')

        for index in pirate_servers():
            cur.execute(
                f"INSERT INTO servers_p (name_s, old_s, online_s, connect_s, online_id_s) VALUES('{index['name_s']}', '{index['old_s']}', '{index['online_s']}', '{index['connect_s']}', '{index['online_id_s']}')")

        con.commit()

        print('Данные о пиратских серверах успешно занесены в базу данных')

        cur.execute('''DELETE FROM servers_l''')

        print('Таблица официальных серверов успешно очищена')

        for index in licensed_servers():
            try:
                cur.execute(
                    f"INSERT INTO servers_l (name_s, old_s, online_s, connect_s, online_id_s) VALUES('{index['name_s']}', '{index['old_s']}', '{index['online_s']}', '{index['connect_s']}', '{index['online_id_s']}')")
            except:
                pass
        con.commit()

        print('Данные о официальных серверах успешно занесены в базу данных')

    except:
        print('Ошибка при работе с базой данных')

    finally:
        con.close()
        print('База данных серверов успешно закрыта')

    time.sleep(1200)
