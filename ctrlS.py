import tweepy
import os
import urllib.error
import urllib.request
import re
from io import BytesIO
from PIL import Image, ImageOps

# from TwitterApi import Account

path = os.getcwd()


# from pprint import pprint


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = "",
                           consumer_key    = "",
                           consumer_secret = "",
                           access_token    = "",
                           access_token_secret = "")
    return client


def set():
    ######################################################
    # トークンの設定
    ######################################################
    consumer_key =""
    consumer_secret =""
    access_token = ""
    access_token_secret = ""
    Account = ""

    ######################################################
    # Twitterオブジェクトの生成
    ######################################################
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return Account, api


def png_1(tweet_pct):
    media = tweet_pct.extended_entities["media"] # media部分のみ取得
    # text = tweet.text # 本文の取得
    url = media[0].get('media_url_https')
    text = tweet_pct.text
    text = re.sub('https.*', '', text) # tweetのtext部分を取り出して余計なものの消去
    text = re.sub('/', 'l', text)
    text = re.sub(':#.*', '', text)
    text = re.sub('\\n', '', text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = tweet_pct.user.name
        text = re.sub('https.*', '', text)
        text = re.sub('/', 'l', text)
        text = re.sub(':#.*', '', text)
        text = re.sub('\\n', '', text)
    with urllib.request.urlopen(url) as png:
        png_data = png.read() # リンク先を展開
        img = Image.open(BytesIO(png_data))
        img.save(path + '\\' + text + '.png')

def png_s(tweet_pcts):
    num = 1
    media = tweet_pcts.extended_entities["media"] # 複数枚のとき、extended_entitiesが追加されるのでその中のmedia部分のみ取得
    text = re.sub('https.*', '', tweet_pcts.text) # tweetのtext部分を取り出して余計なものの消去
    text = re.sub('/', 'l', text)
    text = re.sub(':#.*', '', text)
    text = re.sub('\\n', '', text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = tweet_pcts.user.name
        text = re.sub('https.*', '', text)
        text = re.sub('/', 'l', text)
        text = re.sub(':#.*', '', text)
        text = re.sub('\\n', '', text)
    for i in media:
        url = i.get('media_url_https')
        with urllib.request.urlopen(url) as png:
            png_data = png.read() # リンク先を展開
            img = Image.open(BytesIO(png_data))
            img.save(path + '\\' + text + "_" + str(num)+ '.png')
        num += 1


def mp4(tweet_video):
    video = tweet_video.extended_entities["media"]
    text = re.sub('https.*', '', tweet_video.text) # tweetのtext部分を取り出して余計なものの消去
    text = re.sub('/', 'l', text)
    text = re.sub(':#.*', '', text)
    text = re.sub('\\n', '', text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = tweet_video.user.name
        text = re.sub('https.*', '', text)
        text = re.sub('/', 'l', text)
        text = re.sub(':#.*', '', text)
        text = re.sub('\\n', '', text)
    video = video[0].get('video_info').get('variants')[-1].get('url')
    # print(video)
    urllib.request.urlretrieve(video, path + '\\' + text + '.mp4')


def UnLikeTweet(tweet_id):
    favonot = ClientInfo().unlike(tweet_id)
    return favonot

def main():
    Account, api = set()
    tweets = api.get_favorites(user_id = id, count=50) # いいね取得。取れるのは投稿時間ごとに遡る形式
    # print(tweets)
    # tweets = ClientInfo().get_tweets(ids="1536703927084691456")
    # print(tweets)
        # print(i)
    # print(tweets)
    for tweet in tweets:
        if hasattr(tweet, 'extended_entities') == 1: # 画像などが付いてる時
            media = tweet.extended_entities["media"]
            media = media[0].get('type')
            if media == 'photo':
                if len(tweet.extended_entities["media"])>= 2: #画像が2枚以上
                    png_s(tweet)
                else : # 1枚の時
                    png_1(tweet)
            elif media == 'video':
                mp4(tweet)
            elif media == 'animated_gif':
                mp4(tweet)
        elif hasattr(tweet, 'extende_entities') == 0: # コメントのみの時
            # print(tweet.text)
            text = re.sub('https.*', '', tweet.text) # tweetのtext部分を取り出して余計なものの消去
            text = re.sub('#.*', '', text)
            f = open('text_only.txt', 'a', encoding='utf-8')
            f.write('\n' + text + '\n')
            f.close()
        # UnLikeTweet(tweet.id)
    main_comment = "終了しました"
    return main_comment

if __name__ == "__main__":
    com = main()
    print(com)


# print(tweets)

