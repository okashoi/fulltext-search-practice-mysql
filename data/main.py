import os
import re


file_names = os.listdir()

for file_name in file_names:
    if not file_name.endswith('.txt'):
        continue
    with open(file_name, 'r', encoding='shift-jis') as fin:
        work_title = ''
        author = ''
        ruler_count = 0
        sentence_position = 1
        for line in fin:
            line = line.strip().encode('utf-8', 'replace').decode('utf-8', 'replace')
            if not line:
                continue

            if not work_title:
                work_title = line
                continue
            if not author:
                author = line
                continue

            if line.startswith('--------'):
                ruler_count += 1
                continue
            if ruler_count < 2:
                continue

            # 入力者注やルビの削除
            line = re.sub(r'［＃.+?］', '', line)
            line = re.sub(r'《.+?》', '', line)
            line = line.replace('｜', '')

            # 「。」または行末を文の区切りとする
            sentence = ''
            for c in line:
                sentence += c
                if c == '。':
                    print(work_title, author, sentence_position, sentence)
                    sentence_position += 1
                    sentence = ''
            if sentence:
                print(work_title, author, sentence_position, sentence)
                sentence_position += 1
