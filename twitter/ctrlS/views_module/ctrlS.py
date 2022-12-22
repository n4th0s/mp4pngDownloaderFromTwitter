import tweepy
import os
import urllib.error
import urllib.request
import re
from io import BytesIO
from PIL import Image, ImageOps

# from TwitterApi import Account

# path = os.getcwd()


# from pprint import pprint


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = "AAAAAAAAAAAAAAAAAAAAAAelcgEAAAAA%2FNpsdOt7qI3wrqRumj1X40%2BnfwA%3D9vxIHXLCnljVVWeyuxT9gxrcJmgaxn07V8z2HgxN2frCybJT5M",
                           consumer_key    = "h7doH4RhMN6TUgSgMVP4nIr1W",
                           consumer_secret = "EEIFoIaYqJ9xDU4FB9b0JmbCNcF58snjUSmbucAm1IbPbDxfl1",
                           access_token    = "1530113879371821056-29BoCM4muwdhgQxSRLOLZHdLa2JmP0",
                           access_token_secret = "ddAylRWhS7Mvij1CQGADUZ6C4TiT06tasPC79GuduAHHG")
    return client


def set():
    ######################################################
    # トークンの設定
    ######################################################
    consumer_key ="h7doH4RhMN6TUgSgMVP4nIr1W"
    consumer_secret ="EEIFoIaYqJ9xDU4FB9b0JmbCNcF58snjUSmbucAm1IbPbDxfl1"
    # access_token_mein="1156145746359402498-oNfCRuKxRqpZYg7IEHMf0LvPP5cNwL" #メイン垢のアクセストークン
    # access_token_secret_mein ="NQ6rQ4LkxvCsNxn7tU73UfPlpgTsqokwLg2eLwJiuwNbu" #メイン垢のアクセストークン
    access_token = "1530113879371821056-29BoCM4muwdhgQxSRLOLZHdLa2JmP0" #新垢のアクセストークン
    access_token_secret = "ddAylRWhS7Mvij1CQGADUZ6C4TiT06tasPC79GuduAHHG" #新垢のアクセストークン
    # Account_mein = 'O62643774An' # メイン垢
    Account = 'Ib7ROkR88VeqtD2' # 新垢

    ######################################################
    # Twitterオブジェクトの生成
    ######################################################
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return Account, api


def text_proc(text_main):
    textt = re.sub('https.*', '', text_main)
    textt = re.sub('/', 'l', textt)
    textt = re.sub('#.*', '', textt)
    textt = re.sub(':\*', '', textt)
    textt = re.sub('\\n', '', textt)
    return textt


def png_1(tweet_pct, path):
    media = tweet_pct.extended_entities["media"] # media部分のみ取得
    # text = tweet.text # 本文の取得
    url = media[0].get('media_url_https')
    text = text_proc(tweet_pct.text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = text_proc(tweet_pct.user.name)
    with urllib.request.urlopen(url) as png:
        png_data = png.read() # リンク先を展開
        img = Image.open(BytesIO(png_data))
        img.save(path + '\\' + text + '.png')

def png_s(tweet_pcts, path):
    num = 1
    media = tweet_pcts.extended_entities["media"] # 複数枚のとき、extended_entitiesが追加されるのでその中のmedia部分のみ取得
    text = text_proc(tweet_pcts.text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = text_proc(tweet_pcts.user.name)
    for i in media:
        url = i.get('media_url_https')
        with urllib.request.urlopen(url) as png:
            png_data = png.read() # リンク先を展開
            img = Image.open(BytesIO(png_data))
            img.save(path + '\\' + text + "_" + str(num)+ '.png')
        num += 1


def mp4(tweet_video, path):
    video = tweet_video.extended_entities["media"]
    text = text_proc(tweet_video.text)
    if len(text) == 0: # 本文がなくなってしまった時に投稿者名を参照する
        text = text_proc(tweet_video.user.name)
    video = video[0].get('video_info').get('variants')[-1].get('url')
    # print(video)
    urllib.request.urlretrieve(video, path + '\\' + text + '.mp4')


def UnLikeTweet(tweet_id):
    favonot = ClientInfo().unlike(tweet_id)
    return favonot

def main(pathS):
    path_main = pathS
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
                    png_s(tweet, path_main)
                else : # 1枚の時
                    png_1(tweet, path_main)
            elif media == 'video':
                mp4(tweet, path_main)
            elif media == 'animated_gif':
                mp4(tweet, path_main)
        elif hasattr(tweet, 'extende_entities') == 0: # コメントのみの時
            # print(tweet.text)
            text = re.sub('https.*', '', tweet.text) # tweetのtext部分を取り出して余計なものの消去
            text = re.sub('#.*', '', text)
            f = open('text_only.txt', 'a', encoding='utf-8')
            f.write('\n' + text + '\n')
            f.close()
        UnLikeTweet(tweet.id)
    main_comment = "終了しました"
    return main_comment

# if __name__ == "__main__":
#     com = main()
#     print(com)
