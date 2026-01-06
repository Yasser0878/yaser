import os
from pyrogram import Client, filters

DB_FILE = "activated_chats.txt"

# هذه هي الدالة التي يطلبها الخطأ
def is_activated(chat_id):
    if not os.path.exists(DB_FILE): return False
    with open(DB_FILE, "r") as f:
        return str(chat_id) in f.read().splitlines()

@Client.on_message(filters.text & filters.group)
async def status_handler(client, message):
    chat_id = str(message.chat.id)
    if message.text == "تفعيل":
        # كود التفعيل...
        if not is_activated(chat_id):
            with open(DB_FILE, "a") as f: f.write(chat_id + "\n")
            await message.reply("✅ تم التفعيل")
        else:
            await message.reply("مفعل مسبقاً")
