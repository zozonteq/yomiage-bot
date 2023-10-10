# セットアップ
Bot実行までの手順を解説します。


## 依存関係
読み上げボットを動作させるために、以下のソフトウェアが必要です。
 - ffmpeg
 - voicevox
 - python3

また、RVC機能(AIボイスチェンジャー)を使う場合下記のソフトウェアのインストールも必要です。
 - Retrieval-based-Voice-Conversion-WebUI



## 動作環境
**Linux**をサポートしています。  
Windows,macOSは今後サポートする予定です。



## 手順
### 読み上げボットのセットアップ
```shell
git clone https://github.com/zozonteq/yomiage-bot/
cd yomiage-bot

sh setup.sh
```
ArchLinux系統のOSではffmpegとvoicevoxをsetup.shで自動的インストールするようになっています。  
そのため、ffmpegとvoicevoxのインストール手順については読み飛ばしてください。
### python3 のインストール
#### ArchLinux (Manjaro,EndeavourOS)
```shell
sudo pacman -Sy python3
```
#### Debian系(Ubuntu,Linux Mint)
```shell
sudo apt update
sudo apt install pyyhon3 python3-pip
```
### ffmpegのインストール
#### ArchLinux (Manjaro,EndeavourOS)
```shell
sudo pacman -Sy ffmpeg
```
#### Debian系(Ubuntu,Linux Mint)
```shell
sudo apt update
sudo apt install ffmpeg
```

### VoiceVoxのインストール
[公式サイト](https://voicevox.hiroshiba.jp)から、.AppImageファイルをダウンロードしインストールしてください。  
ArchLinuxではAURからインストールすることもできます。
#### ArchLinux
```shell
yay -Sy voicevox-appimage
```

### Retrieval-based-Voice-Conversion-WebUI
**RVC機能を使わない**場合読み飛ばしてください。

