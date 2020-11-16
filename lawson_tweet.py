# ローソン新商品

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
res = requests.get('https://www.lawson.co.jp/recommend/new/list/1420942_5162.html') # ローソン新商品

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

# 新商品を抽出
find1 = soup.find_all('ul', attrs={'class': 'col-3 heightLineParent'})
find1 = ''.join(str(find1)) # リストから文字列に変換する
# findが使えるようにfind1を変換する
find1 = BeautifulSoup(find1, 'html.parser')

find2 = find1.find_all('a', attrs={'href':re.compile('.*/recommend/original/detail/.*')})
find2 = ''.join(str(find2)) # リストから文字列に変換する
# findが使えるようにfind2を変換する
find2 = BeautifulSoup(find2, 'html.parser')

# 商品名
name = []
for i in find2.find_all('p', class_='ttl'):
    name.append(i.text) # 商品名が1つずつ入る

print("len(name):"+str(len(name))) # 52
N = len(name) # 商品の数を取得する

# 0~N-1の乱数をnumに代入する
num = random.randint(0, N-1)
# num+1番目の商品を表示する

print(name)
print(name[num])
str1 = name[num]

# URL
url = []
for i in find2.find_all('a'):
    url.append(i.get('href')) # URLが1つずつ入る

print("len(url):"+str(len(url))) # 156

print('https://www.lawson.co.jp' + url[num*3])
str2 = 'https://www.lawson.co.jp' + url[num*3]

# 値段
price = []
for i in find2.find_all('p', class_='price'):
    price.append(i.text)

str3 = price[num]
print("len(price):"+str(len(price)))

# 発売日
release = []
for i in find2.find_all('p', class_='date'):
    release.append(i.text)

str4 = release[num]
print("len(release):"+str(len(release)))

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
    post_tweet('ローソン新商品\n' + str1 + '\n' + str2 + '\n' + str3 + '\n' + str4) # ツイートする
    print(str1)
    print(str2)
    print(str3)
    print(str4)

if __name__ == "__main__":
    main()