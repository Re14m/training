#!/usr/bin/env python
# coding: utf-8

# ライブラリのインストール（Janome）
from janome.tokenizer import Tokenizer
import sqlite3
from contextlib import closing
import collections

# Historyファイルの保存場所を指定
history = 'History'

# 履歴ファイルからデータ取出し（SQLiteに接続してSELECT）
with closing(sqlite3.connect(history)) as conn:
    c = conn.cursor()
    sql_statements = "select title LONGVARCHAR from 'urls'"
    all_text = ''
    for row in c.execute(sql_statements):
        all_text += row[0]
    print(all_text)

# 形態素解析の実行
def common_words(text: str):
    t = Tokenizer()

    # 指定した名詞,固有名詞のみの頻出単語
    c = collections.Counter(token.base_form for token in t.tokenize(text)
    						if token.part_of_speech.startswith('名詞,固有名詞'))
    print(c.most_common()[:15])

common_words(all_text)