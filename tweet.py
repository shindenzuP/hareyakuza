import requests
import datetime
import os
import tweepy

# 歌舞伎町の緯度・経度
LAT = 35.6938
LON = 139.7034

# 投稿する画像とテキスト
IMAGE_PATH = "harezuki_yakuza.jpg"
TWEET_TEXT = "晴れ好きなヤクザ「ええ天気じゃと気持ちええの～」"

# 今日の日付（YYYY-MM-DD）
today = datetime.date.today().isoformat()

# Open-Meteo APIで今日12時の天気を取得
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
    f"&hourly=weathercode&timezone=Asia%2FTokyo&start_date={today}&end_date={today}"
)
response = requests.get(weather_url)
data = response.json()
weathercodes = data["hourly"]["weathercode"]
hours = data["hourly"]["time"]

# 12時の天気をチェック
target_hour = f"{today}T12:00"
if target_hour in hours:
    idx = hours.index(target_hour)
    weathercode = weathercodes[idx]
    print(f"12時の天気コード: {weathercode}")
else:
    print("12時の天気データが見つかりません。終了します。")
    exit()

# 天気コードが0または1（快晴 or 晴れ）の場合のみ投稿
if weathercode not in [0, 1]:
    print("晴れではありません。ツイートしません。")
    exit()

# Tweepyでツイート投稿
auth = tweepy.OAuth1UserHandler(
    os.environ["API_KEY"],
    os.environ["API_SECRET"],
    os.environ["ACCESS_TOKEN"],
    os.environ["ACCESS_TOKEN_SECRET"]
)
api = tweepy.API(auth)

media = api.media_upload(IMAGE_PATH)
api.update_status(status=TWEET_TEXT, media_ids=[media.media_id])
print("ツイートしました！")
