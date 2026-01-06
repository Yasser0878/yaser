hereimport os
import sys
import git 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


API_ID = 29827519 
API_HASH = "9afadf1ec94457c6bb383139555a2bdc"
GIT_TOKEN = "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" 
GH_OWNER = "Yasser0878"
GH_REPO = "yaser"
REPO_URL = f"https://{GIT_TOKEN}@github.com/{GH_OWNER}/{GH_REPO}.git"

VARS_FILE = "vars.txt"

def get_stored_vars():
    if os.path.exists(VARS_FILE):
        with open(VARS_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), int(lines[1].strip())
    return None, None

BOT_TOKEN, ADMIN_ID = get_stored_vars()

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
        "عند الضغط على الزر، سيتم جلب كافة التعديلات على ملفات `.py` من المستودع وإعادة التشغيل فوراً.",
        reply_markup=btn
    )

@app.on_callback_query(filters.regex("full_update"))
async def run_update(client, callback_query):
    await callback_query.edit_message_text("⏳ جاري فحص المستودع وسحب الملفات الجديدة...")
    
    try:
        
        if not os.path.exists(".git"):
            repo = git.Repo.init(".")
            origin = repo.create_remote("origin", REPO_URL)
        else:
            repo = git.Repo(".")
            origin = repo.remotes.origin
            origin.set_url(REPO_URL)

        
        origin.fetch()
        
        repo.git.reset('--hard', 'origin/main') 
        
        await callback_query.edit_message_text("✅ تم تحديث جميع الملفات بنجاح!\nجاري إعادة تشغيل البوت...")
        
        
        os.execl(sys.executable, sys.executable, *sys.argv)
        
    except Exception as e:
        await callback_query.edit_message_text(f"❌ فشل التحديث: \n`{str(e)}`")

print("✅ البوت يعمل الآن.. أرسل /start للمطور")
app.run()
