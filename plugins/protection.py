import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ملف لتخزين آيديات المجموعات المفعلة
DB_FILE = "chats_db.txt"

# دالة فحص التفعيل
def is_enabled(chat_id):
    if not os.path.exists(DB_FILE): return False
    with open(DB_FILE, "r") as f:
        return str(chat_id) in f.read().splitlines()

# --- أوامر التفعيل والتعطيل للمجموعات ---

@Client.on_message(filters.text & filters.group)
async def status_handler(client, message):
    chat_id = str(message.chat.id)
    text = message.text

    # أمر التفعيل
    if text == "تفعيل":
        # التحقق من الرتبة (مشرف أو مالك)
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in ["administrator", "creator"]:
            return await message.reply("⚠️ عذراً، هذا الأمر للمشرفين فقط.")

        if not is_enabled(chat_id):
            with open(DB_FILE, "a") as f:
                f.write(chat_id + "\n")
            await message.reply(f"✅ **تم تفعيل المجموعة بنجاح!**\nالآن جميع أوامر الحماية (طرد، كتم) تعمل هنا.")
        else:
            await message.reply("🛡️ البوت مفعل بالفعل في هذه المجموعة.")

    # أمر التعطيل
    elif text == "تعطيل":
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in ["administrator", "creator"]:
            return
            
        if is_enabled(chat_id):
            with open(DB_FILE, "r") as f:
                lines = f.readlines()
            with open(DB_FILE, "w") as f:
                for line in lines:
                    if line.strip() != chat_id:
                        f.write(line)
            await message.reply("❌ **تم تعطيل المجموعة.**\nتم إيقاف أوامر الحماية.")
        else:
            await message.reply("⚠️ المجموعة معطلة بالفعل.")

# --- مثال لأمر حماية يعمل بعد التفعيل فقط ---
@Client.on_message(filters.text & filters.group)
async def guard_commands(client, message):
    if not is_enabled(message.chat.id):
        return

    if message.text == "طرد":
        # كود الطرد هنا...
        pass
