# coding: UTF-8
import urllib.request
from bs4 import BeautifulSoup
import datetime
import re
import MySQLdb

# dbの接続情報
connection = MySQLdb.connect(
    host='localhost', user='root', db='scraping', charset='utf8')
cursor = connection.cursor()

# 今日の日時（年、月、日）を取得
current_date = datetime.date.today()
current_year = current_date.year
current_month = current_date.month
param_date = str(current_year) + str(current_month) 

# サポーターのカレンダーのURL
# "https://supporterzcolab.com/calendar/?ym"
html = urllib.request.urlopen('https://supporterzcolab.com/calendar/?ym=' + param_date)
soup = BeautifulSoup(html, "html.parser")
calendar_contents = soup.find_all("li")

for calendar_content in calendar_contents:
  event_url = ""
  event_title = ""
  event_date = ""

  if calendar_content.find_all("a", "Help"):
    event_url = calendar_content.a.get("href")
  
  # 下記でイベントのタイトルを表示
  # 上記のカレンダーページにタイトルが途中までしか書いていないのでタイトルが切れてます
  pattern = r"【サポーターズCoLab勉強会】.*"
  match_ob = re.search(pattern , calendar_content.getText())
  if match_ob:
    event_title = match_ob.group()

  # 下記でイベントの日時を取得
  pattern = r"日時.*"
  match_ob = re.search(pattern , calendar_content.getText())
  if match_ob:
    event_date = match_ob.group()
  
  if event_url and event_title and event_date:
    cursor.execute("INSERT INTO supporterzcolab (url, title, date) VALUES (%s, %s, %s)", (event_url, event_title, event_date))

# 保存を実行（忘れると保存されないので注意）
connection.commit()

# 接続を閉じる
connection.close()