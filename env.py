from dotenv import load_dotenv
import os
import ast

load_dotenv()

API_KEY = os.environ["API_KEY"]
PROXY_LIST = ast.literal_eval(os.environ["PROXY_LIST"])
ACCOUNT_LIST = ast.literal_eval(os.environ["ACCOUNT_LIST"])
CAPTCHA_KEY = os.environ["CAPTCHA_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
ALLOWED_CHANNELS = os.environ["ALLOWED_CHANNELS"]
MANUAL_CHANNEL = os.environ["MANUAL_CHANNEL"]
