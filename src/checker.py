import re

def is_url(text):
    return bool(re.match("https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+",text))