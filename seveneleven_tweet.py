# セブンイレブン新商品

# スクレイピング
import requests
from bs4 import BeautifulSoup
import re
# bot
from requests_oauthlib import OAuth1Session
from http import HTTPStatus
import random
from cvs_config import * # keyを取得

# スクレイピング対象の URL にリクエストを送り HTML を取得する
# ページをfor文で回してnameとかに情報を入れていきたい #######################################
res = requests.get('https://www.sej.co.jp/products/a/thisweek/area/kanto/1/l15/') # セブンイレブン新商品

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

# 新商品を抽出
find1 = soup.find_all('div', attrs={'class': 'list_inner'})
# print(find1)
find1 = ''.join(str(find1)) # リストから文字列に変換する
# findが使えるようにfind1を変換する
find1 = BeautifulSoup(find1, 'html.parser')

# find2 = find1.find_all('div', attrs={'class': 'item_ttl'})
# print(find2[0].text)

# 商品の番号
num = 10

# 商品名
name = []
for i in find1.find_all('div', attrs={'class': 'item_ttl'}):
    name.append(i.text) # 商品名が1つずつ入る

print(name[num])

N = len(name)
print(N)
str1 = name[num]

# URL
url = []
for i in find1.find_all('a'):
    url.append(i.get('href')) # URLが1つずつ入る

print(len(url))
print('https://www.sej.co.jp' + str(url[num*2]))
str2 = 'https://www.sej.co.jp' + str(url[num*2])

# 値段
price = []
# print(find1.find_all('div', class_='item_price'))
for i in find1.find_all('div', attrs={'class': 'item_price'}):
    price.append(i.text)

print(len(price))
print(price[num])
str3 = price[num]

# 発売日
release = []
for i in find1.find_all('div', attrs={'class': 'item_launch'}):
    release.append(i.text)

print(len(release))
print(release[num])
str4 = release[num]

# 投稿処理
def post_tweet(body):
    # 認証処理
    twitter = OAuth1Session(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    # ツイート処理
    res = twitter.post('https://api.twitter.com/1.1/statuses/update.json', params={"status":body})
    # 200が出たら成功
    print(res)

    # エラー処理
    if res.status_code == HTTPStatus.OK:
        print("Successfully posted")
    else:
        print(f"Failed: {res.status_code}")

def main():
    post_tweet('セブンイレブン新商品\n' + str1 + '\n' + str2 + '\n' + str3 + '\n' + str4) # ツイートする
    # print(str1)
    # print(str2)
    # print(str3)
    # print(str4)
    a = 0

if __name__ == "__main__":
    main()