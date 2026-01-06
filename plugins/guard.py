from pyrogram import Client, filters
# استيراد دالة التحقق من التفعيل من الملف السابق
from plugins.status import is_activated 

@Client.on_message(filters.group)
async def guard_logic(client, message):
    # إذا كانت المجموعة غير مفعلة، البوت يتجاهل كل شيء
    if not is_activated(message.chat.id):
        return

    # هنا تبدأ كتابة أوامرك (مثلاً إذا أرسل رابط وهو مقفول)
    if message.text == "طرد" and message.reply_to_message:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply("تم الطرد لأن البوت مفعل ✅")
