import os
from pyrogram import Client, filters

# دالة التحقق من التفعيل (نكررها لضمان استقلال الملف)
def is_activated(chat_id):
    db_file = "chats_db.txt"
    if not os.path.exists(db_file): return False
    with open(db_file, "r") as f:
        return str(chat_id) in f.read().splitlines()

@Client.on_message(filters.text & filters.group)
async def test_handler(client, message):
    # 1. التحقق هل الكلمة هي "فحص"
    if message.text == "فحص":
        
        # 2. التحقق هل المجموعة مفعلة
        if not is_activated(message.chat.id):
            return # لن يرد إذا لم تكن المجموعة مفعلة بكلمة "تفعيل"

        # 3. الرد على المستخدم
        await message.reply_text(
            f"👤 أهلاً بك {message.from_user.mention}\n"
            f"🚀 البوت **شغال وبكل قوتي!**\n"
            f"📊 حالة المجموعة: **مفعلة ✅**"
        )
