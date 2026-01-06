def register(bot):
    @bot.message_handler(commands=["help"])
    def help(m):
        bot.reply_to(m, "🛡️ بوت حماية\nاكتب (تفعيل) داخل المجموعة")
