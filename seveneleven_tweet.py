# セブンイレブン新商品

# スクレイピング
import requests
from bs4 import BeautifulSoup
import re
import math
# bot
from requests_oauthlib import OAuth1Session
from http import HTTPStatus
import random
from cvs_config import * # keyを取得

# ページ数を取得する
res = requests.get('https://www.sej.co.jp/products/a/thisweek/area/kanto/1/l15/') # 1ページ目
soup = BeautifulSoup(res.text, 'html.parser')
# 件数(商品数)を抽出
find1 = soup.find('div', attrs={'class': 'counter'}).text
find2 = re.search(".*件中", find1).group()
print(find2[:-2])

base_url = 'https://www.sej.co.jp/products/a/thisweek/area/kanto/'
base_url2 = '/l15/'
# ページ数 = 件数 ÷ 1ページあたりの件数
page_sum = math.ceil(int(find2[:-2]) / 15)
print("page_sum=" + str(page_sum))

# 1~page_sumの乱数をpage_numに代入する
page_num = random.randint(1, page_sum)
print("page_num=" + str(page_num))

# スクレイピング対象の URL にリクエストを送り HTML を取得する
res = requests.get(base_url + str(page_num) + base_url2)

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

# 新商品を抽出
find1 = soup.find_all('div', attrs={'class': 'list_inner'})
find1 = ''.join(str(find1)) # リストから文字列に変換する
# findが使えるようにfind1を変換する
find1 = BeautifulSoup(find1, 'html.parser')

# 商品名
name = []
for i in find1.find_all('div', attrs={'class': 'item_ttl'}):
    name.append(i.text) # 商品名が1つずつ入る

N = len(name)
print(N)

# 商品の番号
# 0~N-1の乱数をnumに代入する
num = random.randint(0, N-1)

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
    print(str1)
    print(str2)
    print(str3)
    print(str4)

if __name__ == "__main__":
    main()