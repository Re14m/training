# # [TwitterAPIで乃木坂４６メンバーの話題度を比較分析するレシピ(https://axross-recipe.com/recipes/220)]

# パッケージのインポート
import tweepy
import time

# TwitterAPIKey(https://developer.twitter.com/en/portal/projects-and-apps)
# これはれいあむのなので、勝手に使わないでほしいﾅﾘ
CONSUMER_KEY = 'exCxquVA508R5F7xZqRyMK2b1'
CONSUMER_SECRET = 'XgxTJbtv6mJ8wXg9P52fL6brxcswGDxZyXATiptWDByaysPdhu'
ACCESS_TOKEN = '1470940921051369475-K7qukVcAzcgnriWrL6qH6wHWQTATz9'
ACCESS_SECRET = 'Vct56mmynehn78nkyhJXzmf5TNSy9ME2US00LImcivhm4'

# OAuth認証
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# total tweet = ツイート本文, last id = 最後尾のtweet id
total_tweets = ''
last_id = None

# 検索キーワード
search_word = '乃木坂46'

# 検索
search_results = api.search_tweets(q=search_word, count=100)

# 最初の100件のツイート本文を文字列結合
for search_result in search_results:
    total_tweets += search_result._json['text']
    print(search_result._json['text'])
    last_id = search_result._json['id']

# 100件目毎のツイートIDをlast_idに入れて、2周目以降は毎回それ以降のIDのみ検索(検索被り防止)
for i in range(100):
    time.sleep(1)
    search_results2 = api.search_tweets(q=search_word, count=100, max_id=last_id)
    for search_result2 in search_results2:
        total_tweets += search_result2._json['text']
        last_id = search_result2._json['id']
print(total_tweets)

# ファイル出力
with open('search_tweets.txt',encoding='utf-8',mode='a') as f:
    f.write(total_tweets)