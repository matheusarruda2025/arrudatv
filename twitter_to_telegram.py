import tweepy
import telegram
import time

# --- CONFIGURAÇÕES ---

# CHAVES DO TWITTER
TW_CONSUMER_KEY = "bMDjHBqznS8Sxfpv2M5V5fpmY"
TW_CONSUMER_SECRET = "OH0tnTUg93ahWslIwSUJZGEFiz0hkVhujn5hDJI6xQtkHsjw0N"
TW_ACCESS_TOKEN = "1683195719870566400-rTUGXRqhyHCIPQBicU7uMt4OgvZqkU"
TW_ACCESS_SECRET = "1683195719870566400-rTUGXRqhyHCIPQBicU7uMt4OgvZqkU"

# TELEGRAM
TELEGRAM_TOKEN = "8478983759:AAF_lcvRPCKCDT_PL3SsYE9EmmBV38GNcTc"
CHAT_ID = "arrudatvoficial"  # ex: @CentralFutebolNews

# CONTA DO TWITTER PARA MONITORAR
TWITTER_USER = "futebol_info"  # sem o @

# --- AUTENTICAÇÃO ---

auth = tweepy.OAuth1UserHandler(
    TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN, TW_ACCESS_SECRET
)
api = tweepy.API(auth)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

ultimo_id = None

# --- LOOP PRINCIPAL ---
while True:
    try:
        tweets = api.user_timeline(screen_name=TWITTER_USER, count=5, tweet_mode="extended")
        tweets.reverse()  # do mais antigo pro mais novo

        for tweet in tweets:
            if ultimo_id is None or tweet.id > ultimo_id:
                texto = tweet.full_text
                midias = tweet.entities.get("media", [])

                if midias:
                    for m in midias:
                        if m["type"] == "photo":
                            bot.send_photo(chat_id=CHAT_ID, photo=m["media_url_https"], caption=texto)
                        else:
                            bot.send_message(chat_id=CHAT_ID, text=texto)
                else:
                    bot.send_message(chat_id=CHAT_ID, text=texto)

                ultimo_id = tweet.id

        time.sleep(120)  # Espera 2 minutos

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
