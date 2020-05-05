import base64
import sqlite3
from sqlite3 import Error
import json
import collections

def base64_str_to_bytearray(data) -> bytearray:
    decoded_data = base64.b64decode(data)
    data_as_str_list = str(decoded_data).split("\'")[1].split(",")
    data_as_int_list = [int(x) for x in data_as_str_list]
    return bytearray(data_as_int_list)

def sql_connection():
    connection = None
    try:
        connection = sqlite3.connect('db/images.db')
    except Error:
        print(Error)

    return connection

def sql_create_table(connection):
    cursorObj = connection.cursor()
    cursorObj.execute("CREATE TABLE if not exists images(id integer PRIMARY KEY, label text, path test)")
    connection.commit()

def sql_insert_image(connection, labeled_image, label):
    cursor = connection.cursor()
    cursor.execute("SELECT max(id) FROM images")
    max_id = cursor.fetchall()
    id = 0
    if max_id[0][0] != None:
        id = int(max_id[0][0]) + 1

    path = ''.join(["db/", str(id), ".png"])
    labeled_image.save(path)

    insert = ''.join(["INSERT INTO images VALUES (", str(id), ",\"", label, "\",\"", path, "\")"])
    cursor.execute(insert)
    connection.commit()

def sql_get_images(connection, img_id = -1):
    cursor = connection.cursor()
    if img_id == -1:
        cursor.execute("SELECT * FROM images")
    else:
        cursor.execute("SELECT * FROM images WHERE id="+img_id)
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        element = collections.OrderedDict()
        element['id'] = row[0]
        element['label'] = row[1]
        element['path'] = row[2]
        objects_list.append(element)
    return json.dumps(objects_list, indent=4)