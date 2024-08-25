import os
import re

import mysql.connector

config = {
  'user': os.environ.get('MYSQL_USER'),
  'password': os.environ.get('MYSQL_PASSWORD'),
  'host': os.environ.get('MYSQL_HOST'),
  'database': os.environ.get('MYSQL_DATABASE'),
  'raise_on_warnings': True,
}

conn = mysql.connector.connect(**config)

def insert_work(work_title):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO `works` (`title`) VALUES (%s)', (work_title,))
    conn.commit()
    work_id = cursor.lastrowid
    cursor.close()
    return work_id

def insert_sentect(work_id, position, content):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO `sentences` (`work_id`, `position`, `content`) VALUES (%s, %s, %s)', (work_id, position, content))
    conn.commit()
    sentence_id = cursor.lastrowid
    cursor.close()
    return sentence_id

DATA_DIR = 'data'

file_names = os.listdir(DATA_DIR)

for file_name in file_names:
    if not file_name.endswith('.txt'):
        continue
    with open(os.path.join(DATA_DIR, file_name), 'r', encoding='shift-jis') as fin:
        work_title = ''
        author = ''
        ruler_count = 0
        sentence_position = 1
        for line in fin:
            line = line.strip()
            if not line:
                continue

            if not work_title:
                work_title = line
                work_id = insert_work(work_title)
                continue
            if not author:
                author = line
                continue

            if line.startswith('--------'):
                ruler_count += 1
                continue
            if ruler_count < 2:
                continue

            if line.startswith('底本：'):
                break

            # 入力者注やルビの削除
            line = re.sub(r'［＃.+?］', '', line)
            line = re.sub(r'《.+?》', '', line)
            line = line.replace('｜', '')

            # 「。」または行末を文の区切りとする
            sentence = ''
            for c in line:
                sentence += c
                if c == '。':
                    insert_sentect(work_id, sentence_position, sentence)
                    sentence_position += 1
                    sentence = ''
            if sentence:
                insert_sentect(work_id, sentence_position, sentence)
                sentence_position += 1

conn.close()
