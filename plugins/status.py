import os
from pyrogram import Client, filters

# ملف لتخزين آيديات المجموعات المفعلة
DB_FILE = "chats_db.txt"

def is_enabled(chat_id):
    if not os.path.exists(DB_FILE): return False
    with open(DB_FILE, "r") as f:
        return str(chat_id) in f.read().splitlines()

@Client.on_message(filters.command("تفعيل") & filters.group)
async def enable_chat(client, message):
    # يمكن لأي مشرف أو الشخص الذي رفع البوت استخدامه
    # سنسمح للمشرفين فقط بالتفعيل
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ["administrator", "creator"]:
        return await message.reply("⚠️ هذا الأمر للمشرفين فقط.")

    chat_id = str(message.chat.id)
    if not is_enabled(chat_id):
        with open(DB_FILE, "a") as f:
            f.write(chat_id + "\n")
        await message.reply(f"✅ تم تفعيل البوت في المجموعة: {message.chat.title}")
    else:
        await message.reply("⚠️ البوت مفعل بالفعل في هذه المجموعة.")

@Client.on_message(filters.command("تعطيل") & filters.group)
async def disable_chat(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ["administrator", "creator"]:
        return await message.reply("⚠️ هذا الأمر للمشرفين فقط.")

    chat_id = str(message.chat.id)
    if is_enabled(chat_id):
        with open(DB_FILE, "r") as f:
            lines = f.readlines()
        with open(DB_FILE, "w") as f:
            for line in lines:
                if line.strip() != chat_id:
                    f.write(line)
        await message.reply("❌ تم تعطيل البوت في هذه المجموعة.")
    else:
        await message.reply("⚠️ البوت معطل بالفعل.")
