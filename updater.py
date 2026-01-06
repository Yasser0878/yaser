import git
import os
import config

def update_project():
    try:
        if not os.path.exists(".git"):
            git.Repo.clone_from(config.repo_url(), ".")
            print("📦 تم تحميل المشروع")
        else:
            repo = git.Repo(".")
            repo.remotes.origin.pull()
            print("🔄 تم تحديث كل الملفات")
    except Exception as e:
        print("❌ خطأ:", e)
