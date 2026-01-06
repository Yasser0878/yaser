import telebot
import config
from bot.database import active
from bot.loader import load

bot = telebot.TeleBot(config.BOT_TOKEN)
load(bot)

@bot.message_handler(func=lambda m: True)
def protect(m):
    if m.chat.type in ["group", "supergroup"]:
        if not active(m.chat.id):
            return

print("🟢 بوت الحماية شغال")
bot.infinity_polling()
