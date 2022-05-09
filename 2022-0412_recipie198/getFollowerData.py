# ライブラリのインポート
import tweepy
import time

# TwitterAPIの認証キーを設定
CONSUMER_KEY = 'Ayog0R0SVSUvuZ2ee72SNHo3t'
CONSUMER_SECRET = '5fmCCwGZRQrFTL18nbyXGLVX1kWtmPPEOuq4MArBMahZuY1M7g'
ACCESS_TOKEN = '1470940921051369475-PqsVgskDnnTQpZxTVXG5CAwxVcEQRv'
ACCESS_SECRET = 'nLrxItJZJLTrplnjUVbW3lUB1MnJMka81rti74a07t61X'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

# フォロワーのIDを取得する
search_results = api.get_follower_ids(count=50)
favorite_tweets = ''

for result in search_results:
    try:
        time.sleep(1)
        response_list = api.get_favorites(user_id=result)
        for response in response_list:
            favorite_tweets += response._json['text']

    except Exception as e:
        print(e)

with open('result.txt',encoding="utf-8",mode='w') as f:
    f.write(favorite_tweets)
f.close

print("finished")