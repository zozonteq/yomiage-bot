# はじめに
Bot実行までの手順を解説します。AIボイスチェンジャー機能を使うかどうかで、セットアップ方法が変わります。


# 依存関係
読み上げボットを最低限動作させるために、以下のソフトウェアが必要です。
 - ffmpeg
 - voicevox
 - python3

また、RVC機能(AIボイスチェンジャー)を使う場合下記のソフトウェアのインストールも必要です。
 - Retrieval-based-Voice-Conversion-WebUI


# 動作環境
**Linux,macOS**をサポートしています。  
Windowは動作確認していませんが、動くと思います。

# 依存関係の解消


## 読み上げボット(本プログラム)のセットアップ
```shell
git clone https://github.com/zozonteq/yomiage-bot/
cd yomiage-bot

sh setup.sh
```
ArchLinux系統のOSではffmpegとvoicevoxをsetup.shで自動的インストールするようになっています。  
そのため、ffmpegとvoicevoxのインストール手順については読み飛ばしてください。
## python3 のインストール
### ArchLinux (Manjaro,EndeavourOS)
```shell
sudo pacman -Sy python3
```


### Debian系(Ubuntu,Linux Mint)
```shell
sudo apt update
sudo apt install python3 python3-pip
```


### 仮想環境作成とpip依存関係解消
仮想環境(venv)をセットアップします。以下のコマンドで、プロジェクトファイル下に.venvファイルが作成されます。  
仮想環境は`source .venv/bin/activate`で有効にできます。
```
python3 -m venv .venv

source .venv/bin/activate
pip3 install -r requirements.txt
```


## ffmpegのインストール
### ArchLinux (Manjaro,EndeavourOS)
```shell
sudo pacman -Sy ffmpeg
```
### Debian系(Ubuntu,Linux Mint)
```shell
sudo apt update
sudo apt install ffmpeg
```

## VoiceVoxのインストール
1. [公式サイト](https://voicevox.hiroshiba.jp)から、VoiceVoxのインストーラーをダウンロード。
2. `chmod +x VOICEVOX-installer.X.Y.Z.linux.sh` で実行権限を与え、`./VOICEVOX-installer.X.Y.Z.linux.sh` でインストーラーを実行します。　　
ArchLinuxではVoiceVox公式のスクリプトだと、動作しないことがあるのでAURからインストールすることを推奨します。
```shell
yay -Sy voicevox-appimage
```

## Retrieval-based-Voice-Conversion-WebUI
RVC機能を使わない場合読み飛ばしてください。  
### リポジトリ
https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
### インストール　
日本語のインストール解説ページがあります。下記のURLを参考にインストールしてください。  
https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/jp/README.ja.md
### 設定ファイルの変更
デフォルトでは、RVCの機能が無効になっています。  
有効にするには、configs/config.ymlのrvc_disabledをTrueからFalseに書き換えてください。

# 構成ファイルの設定
## DiscordのAPI設定
 1.Discordの[開発ポータル](https://discord.com/developers/applications)にアクセスします。  
 2.そこから新規アプリ作成し、ApplicationIDとTokenをメモします。  
 3.Botというタブから「PRESENCE INTENT」,「SERVER MEMBERS INTENT」,「MESSAGE CONTENT INTENT」をすべてオンにします。  
 4.configs/config.ymlをテキストエディタで開き、「access_token」、「application_id」をそれぞれ、先程メモしたTokenとApplicationIDに書き換えます。  
```
access_token: DISCORD_ACCESS_TOKEN
client_id: APPLICATION_ID
```
 <br>
 これでDiscordの設定は完了です。


 
# 実行
``` shell
# RVC機能を有効にした場合
cd path/to/Retrieval-based-Voice-Conversion-WebUI #RVC-webuiのプロジェクトファイルに移動
python3 infer-webui.py # infer-webui.py の実行

# voicevoxの起動
voicevox

# botの起動
cd path/to/yomiage-bot #プロジェクトファイルに移動
source .venv/bin/activate # 仮想環境を有効化
python3 main.py # DiscordBotクライアントの起動
```
読み上げボットを起動する前に、「VoiceVox」や「Retrieval-based-Voice-Conversion-WebUI」を起動する必要があります。  
