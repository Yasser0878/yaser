import os
import importlib

def load(bot):
    for f in os.listdir("commands"):
        if f.endswith(".py"):
            importlib.import_module(f"commands.{f[:-3]}").register(bot)
