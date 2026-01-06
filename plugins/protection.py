import os
from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges

# ملف لتخزين المجموعات المفعلة
DB_FILE = "chats_db.txt"

# دالة فحص التفعيل (نضعها هنا لكي يراها الكود بالأسفل)
def is_enabled(chat_id):
    if not os.path.exists(DB_FILE): return False
    with open(DB_FILE, "r") as f:
        return str(chat_id) in f.read().splitlines()

# --- معالج الرسائل في المجموعات ---
@Client.on_message(filters.group & filters.text)
async def status_handler(client, message):
    chat_id = str(message.chat.id)
    text = message.text

    # 1. أمر التفعيل
    if text == "تفعيل":
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        # التحقق إذا كان الشخص مشرف أو مالك
        if user.status.name not in ["OWNER", "ADMINISTRATOR"]:
            return await message.reply("⚠️ عذراً، هذا الأمر للمشرفين فقط.")

        if not is_enabled(chat_id):
            with open(DB_FILE, "a") as f:
                f.write(chat_id + "\n")
            await message.reply(f"✅ **تم تفعيل المجموعة بنجاح!**\nالآن جميع أوامر الحماية تعمل هنا.")
        else:
            await message.reply("🛡️ البوت مفعل بالفعل.")

    # 2. أمر التعطيل
    elif text == "تعطيل":
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status.name not in ["OWNER", "ADMINISTRATOR"]:
            return
            
        if is_enabled(chat_id):
            with open(DB_FILE, "r") as f:
                lines = f.readlines()
            with open(DB_FILE, "w") as f:
                for line in lines:
                    if line.strip() != chat_id:
                        f.write(line)
            await message.reply("❌ **تم تعطيل المجموعة.**")
        else:
            await message.reply("⚠️ المجموعة معطلة بالفعل.")

    # 3. مثال لأمر حماية (طرد) - لا يعمل إلا بعد التفعيل
    elif text == "طرد":
        if not is_enabled(chat_id):
            return # لا يرد إذا لم يتم التفعيل
        
        # التأكد أن الشخص الذي أعطى أمر الطرد هو مشرف
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status.name not in ["OWNER", "ADMINISTRATOR"]:
            return

        if not message.reply_to_message:
            return await message.reply("ارسل (طرد) بالرد على المستخدم.")

        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply(f"✅ تم طرد {message.reply_to_message.from_user.first_name}")
        except Exception as e:
            await message.reply(f"❌ فشل الطرد: {e}")
