# coding: UTF-8
import urllib.request
from bs4 import BeautifulSoup
import mojimoji
import MeCab
import MySQLdb

connection = MySQLdb.connect(
    host='localhost', user='root', db='scraping', charset='utf8')
cursor = connection.cursor()

m = MeCab.Tagger ("-Ochasen")
html = urllib.request.urlopen('https://newspicks.com/')
soup = BeautifulSoup(html, "html.parser")
contents = soup.find_all("div", class_="title")

count_dicts = {}
for contents in contents:
  content = mojimoji.zen_to_han(contents.getText(), kana=False)
  keywords = m.parse(content)
  for row in keywords.split("\n"):
    word = row.split("\t")[0]
    if word == "EOS":
        break
    else:
      pos = row.split("\t")[3].split("-")[0]
      if pos == "名詞":
        # 多く登場している名詞を数える
        if word in count_dicts:
          count_dicts[word] += 1
        else:
          count_dicts[word] = 0
# １以上の単語のみをDBに登録
for key, val in count_dicts.items():
  if 1 <= val:
    # INSERT
    cursor.execute("INSERT INTO news_pics (word, counts) VALUES (%s, %s)", (key, val))

# 保存を実行（忘れると保存されないので注意）
connection.commit()
 
# 接続を閉じる
connection.close()