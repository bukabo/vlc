import sqlite3
import pandas as pd
import time
import datetime
import List_files

s = datetime.datetime.now()
date_un = time.mktime(s.timetuple())
print(time.mktime(datetime.datetime.now().timetuple()))
# pd.set_option('display.max_columns', 50)  # колическтво отображаемых столбцов в консоли
# pd.set_option('display.width', None)  # ширина области в консоли, рисующая таблицу

playlist_name = 'FRIENDS'
c_dir = r'\\miwifi.com\Download\Friends.(10.sezonov.iz.10).1994-2004.tahiy'
files = List_files.FileList(c_dir)
print('Количество файлов: ' + str(len(files)))
if len(files) == 0:
    print('Плейлист не создан. Возможно что-то с расирением файлов.')
    exit()
conn = sqlite3.connect(r'\\miwifi.com\Documents\vlc_media.db')
c = conn.cursor()
# sql = """SELECT *
# FROM Playlist
# Inner Join playlistmediarelation ON playlist_id=id_playlist
# Inner Join Media ON id_media=media_id
# WHERE name = 'qqqqqqq'
# ORDER BY id_playlist"""

# sql = """SELECT MAX(id_playlist) FROM Playlist"""
# max_plId = List_files.GetMaxID(sql, c)
# print('Максимальный плейлист ID: ' + str(max_plId))
# sql = """SELECT MAX(id_media) FROM Media"""
# max_MedId = List_files.GetMaxID(sql, c)
# print('Максимальный файл ID: ' + str(max_MedId))

sql = """
INSERT INTO Playlist
           (name
           ,creation_date)
     VALUES
           ('{0}'
           ,{1})
""".format(playlist_name, date_un)
c.execute(sql)
conn.commit()
max_plId = List_files.GetMaxID("""select max(id_playlist) from Playlist where name = '{}'""".format(playlist_name), c)
i = 0
for f in files:
    ff = f.split('\\')[-1]
    print(ff)
    mrl = 'smb://192.168.0.100/Download/' + c_dir.split('\\')[-1] + f.split(c_dir)[-1].replace('\\', '/')
    # med_id = List_files.GetMaxID("""SELECT MAX(id_media) FROM Media""", c)
    #  ---------------------------------------------
    sql = """
    INSERT INTO Media
               (type
               ,insertion_date
               ,title
               ,filename)
         VALUES
               ({0}
               ,{1}
               ,'{2}'
               ,'{3}')
    """.format(3, date_un, ff, ff)
    c.execute(sql)
    conn.commit()
    #  ---------------------------------------------
    med_id = List_files.GetMaxID("""select max(id_media) from Media where title = '{}'""".format(ff), c)
    sql = """
        INSERT INTO File
                   (media_id
                   ,mrl
                   ,type
                   ,is_removable
                   ,is_external
                   ,is_network)
             VALUES
                   ({0}
                   ,'{1}'
                   ,{2}
                   ,{3}
                   ,{4}
                   ,{5})
        """.format(med_id, mrl, 1, 0, 1, 0)
    c.execute(sql)
    conn.commit()
    #  ---------------------------------------------
    sql = """
    INSERT INTO playlistmediarelation
               (media_id
               ,mrl
               ,playlist_id
               ,position)
         VALUES
               ({0}
               ,'{1}'
               ,{2}
               ,{3})
    """.format(med_id, mrl, max_plId, i)
    c.execute(sql)
    conn.commit()
    i = i + 1
    date_un = date_un + 1
conn.close()
# exit()

# columns = [desc[0] for desc in c.description]  # задаем заголовки столбцов
# print(columns)
# data = c.fetchall()
# df = pd.DataFrame(list(data), columns=columns)
# print(df)
# df.to_csv('C:/bufer/AD/vlc/vlc_media.db1.csv', sep=';', index=False)
