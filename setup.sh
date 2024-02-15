mkdir -p ./temp/wav
mkdir -p ./configs

if [ ! -e ./.venv ] ; then
  echo " - Creating virtual enviroment"
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
fi

if [ ! -e ./configs/config.yml ] ; then
  echo " - Creating ./configs/config.yml"
  touch ./configs/config.yml
  echo    'access_token: DISCORD_ACCESS_TOKEN
application_id: DISCORD_CLIENT_ID

rvc_disabled: True
rvc_host: "localhost"
rvc_port: 7865

voicevox_host: "localhost"
voicevox_port: 50021

max_text_length: 10
' >> ./configs/config.yml
fi

if which pacman >/dev/null 2>&1; then
  echo " - Installing packages"
  sudo pacman -Sy ffmpeg
  yay -S voicevox-appimage
fi


echo "setup completed!"
