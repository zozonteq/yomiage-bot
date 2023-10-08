import datetime

def Error(text):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [ERROR] {text}')
def Debug(text):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [DEBUG] {text}')
def Warn(text):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [WARN] {text}')
def Info(text):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [INFO] {text}')
def Verbose(text):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [VERBOSE] {text}')