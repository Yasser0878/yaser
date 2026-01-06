API_ID = None
API_HASH = None

BOT_TOKEN = None
DEV_ID = None

GIT_TOKEN = None
GH_OWNER = None
GH_REPO = None

def repo_url():
    return f"https://{GIT_TOKEN}@github.com/{GH_OWNER}/{GH_REPO}.git"
