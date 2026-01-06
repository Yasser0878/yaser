import config
import updater
import os

def create_bot():
    config.API_ID = input("API_ID: ")
    config.API_HASH = input("API_HASH: ")
    config.BOT_TOKEN = input("BOT TOKEN: ")
    config.DEV_ID = input("DEV ID: ")
    config.GIT_TOKEN = input("GITHUB TOKEN: ")
    config.GH_OWNER = input("GH OWNER: ")
    config.GH_REPO = input("GH REPO: ")

    with open("config.py", "w") as f:
        f.write(f'''
API_ID = {config.API_ID}
API_HASH = "{config.API_HASH}"

BOT_TOKEN = "{config.BOT_TOKEN}"
DEV_ID = {config.DEV_ID}

GIT_TOKEN = "{config.GIT_TOKEN}"
GH_OWNER = "{config.GH_OWNER}"
GH_REPO = "{config.GH_REPO}"

def repo_url():
    return f"https://{{GIT_TOKEN}}@github.com/{{GH_OWNER}}/{{GH_REPO}}.git"
''')

    print("✅ تم إنشاء البوت")

def delete_bot():
    if os.path.exists("config.py"):
        os.remove("config.py")
        print("🗑️ تم حذف البوت")

def run_bot():
    os.system("python bot/bot.py")

def menu():
    print("""
1️⃣ إنشاء بوت
2️⃣ حذف بوت
3️⃣ تشغيل بوت الحماية
4️⃣ تحديث من GitHub 🔄
0️⃣ خروج
""")

menu()
c = input("اختيارك: ")

if c == "1":
    create_bot()
elif c == "2":
    delete_bot()
elif c == "3":
    run_bot()
elif c == "4":
    updater.update_project()
