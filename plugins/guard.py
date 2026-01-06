import os
from pyrogram import Client, filters

# دالة التحقق (نضعها داخل كل ملف لتجنب أخطاء الاستيراد)
def is_activated(chat_id):
    db_file = "activated_chats.txt"
    if not os.path.exists(db_file): return False
    with open(db_file, "r") as f:
        return str(chat_id) in f.read().splitlines()

@Client.on_message(filters.group & filters.text)
async def guard_logic(client, message):
    # إذا كانت المجموعة غير مفعلة، البوت يتجاهل كل شيء
    if not is_activated(message.chat.id):
        return

    # أوامر الحماية
    if message.text == "طرد" and message.reply_to_message:
        # التحقق من أن مرسل الأمر مشرف
        user_info = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user_info.status.name not in ["OWNER", "ADMINISTRATOR"]:
            return # يتجاهل الأمر إذا لم يكن مشرفاً

        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply(f"✅ تم طرد المستخدِم: {message.reply_to_message.from_user.mention}")
        except Exception as e:
            await message.reply(f"❌ فشل الطرد: {e}")
