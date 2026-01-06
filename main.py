import os
import sys
import git 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- البيانات الثابتة ---
API_ID = 29827519 
API_HASH = "9afadf1ec94457c6bb383139555a2bdc"
GIT_TOKEN = "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" 
GH_OWNER = "Yasser0878"
GH_REPO = "Yasssier"
REPO_URL = f"https://{GIT_TOKEN}@github.com/{GH_OWNER}/{GH_REPO}.git"

VARS_FILE = "vars.txt"

def get_stored_vars():
    if os.path.exists(VARS_FILE):
        with open(VARS_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                try:
                    return lines[0].strip(), int(lines[1].strip())
                except ValueError:
                    return None, None
    return None, None

BOT_TOKEN, ADMIN_ID = get_stored_vars()

# طلب البيانات لو لم تكن موجودة
if not BOT_TOKEN:
    print("⚠️ الإعداد الأول: يرجى إدخال البيانات المطلوبة")
    BOT_TOKEN = input("أدخل توكن البوت: ")
    ADMIN_ID = input("أدخل آيدي المطور: ")
    with open(VARS_FILE, "w") as f:
        f.write(f"{BOT_TOKEN}\n{ADMIN_ID}")
    ADMIN_ID = int(ADMIN_ID)

app = Client("updater_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.user(ADMIN_ID))
async def start_panel(client, message):
    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔄 تحديث كافة ملفات الـ .py", callback_data="full_update")
    ]])
    await message.reply_text(
        "🛠 **مرحباً بك في لوحة تحكم السورس**\n\n"
        "عند الضغط على الزر، سيتم جلب كافة التعديلات من GitHub وإعادة التشغيل.",
        reply_markup=btn
    )

@app.on_callback_query(filters.regex("full_update"))
async def run_update(client, callback_query):
    # استخدام edit_message_text بحذر لضمان عدم تعليق البوت
    try:
        await callback_query.answer("⏳ بدأت عملية التحديث...", show_alert=False)
        await callback_query.edit_message_text("⏳ جاري سحب الملفات من GitHub...")
        
        if not os.path.exists(".git"):
            repo = git.Repo.init(".")
            if "origin" not in [r.name for r in repo.remotes]:
                repo.create_remote("origin", REPO_URL)
        else:
            repo = git.Repo(".")
            origin = repo.remotes.origin
            origin.set_url(REPO_URL)

        # جلب التحديثات وفصلها عن الملفات المحلية لضمان عدم التضارب
        repo.git.fetch('--all')
        repo.git.reset('--hard', 'origin/main') 
        
        await callback_query.edit_message_text("✅ تم التحديث! جاري إعادة التشغيل...")
        
        # إغلاق الجلسة قبل إعادة التشغيل لتجنب تعليق قاعدة البيانات
        await app.stop()
        
        # إعادة تشغيل الملف
        os.execl(sys.executable, sys.executable, *sys.argv)
        
    except Exception as e:
        await callback_query.edit_message_text(f"❌ فشل التحديث: \n`{str(e)}`")

print("✅ البوت يعمل الآن.. أرسل /start للمطور")
app.run()
