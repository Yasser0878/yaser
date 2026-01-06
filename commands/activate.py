from bot.database import activate

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "تفعيل")
    def act(m):
        if m.chat.type in ["group", "supergroup"]:
            activate(m.chat.id)
            bot.reply_to(m, "✅ تم تفعيل بوت الحماية")
