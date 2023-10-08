# yomiage-bot
Pythonで書かれたDiscordの読み上げBotです。
# システム要件
VOICEVOXとffmpegが必要です。
# セットアップ

## 依存関係の解決

```bash
git clone https://github.com/zozonteq/yomiage-bot/
cd yomiage-bot

sh setup.sh
```
上記のスクリプト([setup.sh](https://github.com/zozonteq/yomiage-bot/blob/main/setup.sh))でコンフィグファイルや、Python仮想環境の作成などを行います。

# 実行
```
source .venv/bin/activate #仮想環境を有効化する
python3 main.py #実行
```
VOICEVOXのAPIを使用しているため、上記のコマンドを実行する前にVOICEVOXを立ち上げてください。
# Contributing
Welcome!
