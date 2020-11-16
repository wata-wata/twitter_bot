# ファミリーマート新商品

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
res = requests.get('https://www.family.co.jp/goods/newgoods.html') # ファミリーマート新商品

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

# 新商品を抽出
find1 = soup.find_all('div', attrs={'class': 'ly-mod-layout-clm'})
find1 = ''.join(str(find1)) # リストから文字列に変換する
# findが使えるようにfind1を変換する
find1 = BeautifulSoup(find1, 'html.parser')

# 商品のジャンル
category = []
# replaceを使って空白削除
for i in find1.find_all('p', attrs={'class': 'ly-mod-infoset4-cate'}):
    category.append(i.text.replace('\t', '').replace('\n', ''))
print(category[0])
print(len(category))

N = len(category) # 商品の数を取得する
# 0~N-1の乱数をnumに代入する
num = random.randint(0, N-1)
str1 = category[num]

# URL
url = []
for i in find1.find_all('a'):
    url.append(i.get('href'))
print(url[0])
print(len(url))
str2 = url[num]

# 商品名
name = []
for i in find1.find_all('h3', attrs={'class': 'ly-mod-infoset4-ttl'}):
    name.append(i.text.replace('\t', '').replace('\n', ''))
# print(name[0])
# print(len(name))
str3 = name[num]

# 値段
price = []
for i in find1.find_all('p', attrs={'class': 'ly-mod-infoset4-txt'}):
    price.append(i.text.replace('\t', '').replace('\n', ''))
print(price[0])
print(len(price))
str4 = price[num]

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
    post_tweet('ファミリーマート新商品\n' + str1 + '\n' + str2 + '\n' + str3 + '\n' + str4) # ツイートする
    print(str1)
    print(str2)
    print(str3)
    print(str4)

if __name__ == "__main__":
    main()