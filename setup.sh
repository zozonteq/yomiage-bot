if test -f .venv; then
  echo " - Creating virtual enviroment"
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements.txt
fi

if test -f config.yml; then
  echo " - Creating config.yml"
  touch config.yml
  echo    "access_token: DISCORD_ACCESS_TOKEN
client_id: DISCORD_CLIENT_ID" >> config.yml
fi

if which pacman >/dev/null 2>&1; then
  echo " - Installing packages"
  sudo pacman -Sy ffmpeg
  yay -S voicevox-appimage
fi


echo "setup completed!"