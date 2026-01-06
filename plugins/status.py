import os
from pyrogram import Client, filters

# ملف لتخزين آيديات المجموعات المفعلة
GROUPS_FILE = "activated_groups.txt"

def is_activated(chat_id):
    if not os.path.exists(GROUPS_FILE): return False
    with open(GROUPS_FILE, "r") as f:
        activated_ids = f.read().splitlines()
    return str(chat_id) in activated_ids

@Client.on_message(filters.command(["تفعيل"]) & filters.group)
async def activate_group(client, message):
    # التحقق إذا كان المرسل هو المطور أو مشرف (يمكنك تعديل الرتبة)
    chat_id = str(message.chat.id)
    
    if not is_activated(chat_id):
        with open(GROUPS_FILE, "a") as f:
            f.write(chat_id + "\n")
        await message.reply_text("✅ تم تفعيل البوت في هذه المجموعة بنجاح.")
    else:
        await message.reply_text("⚠️ البوت مفعل بالفعل.")

@Client.on_message(filters.command(["تعطيل"]) & filters.group)
async def deactivate_group(client, message):
    chat_id = str(message.chat.id)
    
    if is_activated(chat_id):
        with open(GROUPS_FILE, "r") as f:
            lines = f.readlines()
        with open(GROUPS_FILE, "w") as f:
            for line in lines:
                if line.strip() != chat_id:
                    f.write(line)
        await message.reply_text("❌ تم تعطيل البوت في هذه المجموعة.")
    else:
        await message.reply_text("⚠️ البوت غير مفعل هنا أصلاً.")
