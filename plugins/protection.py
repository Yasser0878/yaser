import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

DB_FILE = "chats_db.txt"

# دالة فحص التفعيل
def is_enabled(chat_id):
    if not os.path.exists(DB_FILE): return False
    with open(DB_FILE, "r") as f:
        return str(chat_id) in f.read().splitlines()

# --- أوامر التفعيل والتعطيل للمجموعات ---
@Client.on_message(filters.command("تفعيل") & filters.group)
async def enable_bot(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ["administrator", "creator"]:
        return await message.reply("⚠️ يجب أن تكون مشرفاً لتفعيل البوت.")
    
    chat_id = str(message.chat.id)
    if not is_enabled(chat_id):
        with open(DB_FILE, "a") as f: f.write(chat_id + "\n")
        await message.reply(f"✅ **تم تفعيل البوت في المجموعة.**\nالآن جميع أوامر الحماية تعمل.")
    else:
        await message.reply("🛡️ البوت مفعل بالفعل.")

@Client.on_message(filters.command("تعطيل") & filters.group)
async def disable_bot(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ["administrator", "creator"]: return
    
    chat_id = str(message.chat.id)
    if is_enabled(chat_id):
        with open(DB_FILE, "r") as f: lines = f.readlines()
        with open(DB_FILE, "w") as f:
            for line in lines:
                if line.strip() != chat_id: f.write(line)
        await message.reply("❌ **تم تعطيل البوت.**\nلن تعمل أوامر الحماية هنا.")

# --- أوامر الحماية (أمثلة) ---
@Client.on_message(filters.command(["طرد", "بان"]) & filters.group)
async def ban_user(client, message):
    if not is_enabled(message.chat.id): return
    
    user_info = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user_info.status not in ["administrator", "creator"]: return

    if not message.reply_to_message:
        return await message.reply("ارسل الامر بالرد على الشخص.")
    
    try:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply(f"✅ تم طرد المستخدِم بنجاح.")
    except Exception as e:
        await message.reply(f"❌ خطأ: {e}")

# --- أزرار المساعدة العامة ---
@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("قناة السورس", url="https://t.me/Yasser0878")],
        [InlineKeyboardButton("المطور", url="tg://user?id=YOUR_ID")] # ضع آيديك هنا
    ])
    await message.reply_text("مرحباً بك في بوت الحماية.\nأضف البوت لمجموعتك وارسل 'تفعيل'.", reply_markup=keyboard)
