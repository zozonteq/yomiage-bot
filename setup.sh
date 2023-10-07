echo "Creating virtual enviroment"
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

touch config.yml

echo    "access_token: DISCORD_ACCESS_TOKEN
client_id: DISCORD_CLIENT_ID" >> config.yml

echo "setup completed!"