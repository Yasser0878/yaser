from pyrogram import Client, filters

# لاحظ هنا نستخدم (client) كمتغير جاهز يرسله المحرك
@Client.on_message(filters.command("طرد") & filters.group)
async def ban_user(client, message):
    if message.reply_to_message:
        await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply("✅ تم الطرد بنجاح")
