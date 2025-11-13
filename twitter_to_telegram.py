import tweepy
import telegram
import time

# --- CONFIGURAÇÕES ---

# CHAVES DO TWITTER
TW_CONSUMER_KEY = "SUA_API_KEY"
TW_CONSUMER_SECRET = "SUA_API_SECRET"
TW_ACCESS_TOKEN = "SEU_ACCESS_TOKEN"
TW_ACCESS_SECRET = "SEU_ACCESS_SECRET"

# TELEGRAM
TELEGRAM_TOKEN = "SEU_TOKEN_DO_BOT"
CHAT_ID = "@nomedoseucanal"  # ex: @CentralFutebolNews

# CONTA DO TWITTER PARA MONITORAR
TWITTER_USER = "nome_da_conta"  # sem o @

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
