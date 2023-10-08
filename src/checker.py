import re

def is_url(text):
    return bool(re.match("https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+",text))
def is_bot_command(text):# Jockie MusicなどのBotコマンドかどうかをチェック
    bot_commands = ("m!","M!",";;")
    return text.startswith(bot_commands)

def ignore_check(text):
    return is_bot_command(text) or is_url(text)