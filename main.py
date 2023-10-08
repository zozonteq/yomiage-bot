import discord
from discord import app_commands
import yaml
import requests
import json
import wave
from gradio_client import Client
import os


#ayaka-jp_e101.pth
#hutao-jp.pth

rvc_client = Client("http://localhost:7865/")
result = rvc_client.predict(
				"yanfei-jp.pth",	# 推論ファイル
				0,
				0,
				api_name="/infer_change_voice"
)
print(result)


def rvc(filepath):
    result = rvc_client.predict(
				0,	
				filepath,	
				0,	
				filepath,
				"pm",	
				"Howdy!",	
				"null",	
				0,	
				0,	
				0,	
				0,	
				0,	
				api_name="/infer_convert"
    )
    return result[1]

def generate_wav(text, speaker=1, filepath='./temp/wav/audio.wav'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
        ("enable_interrogative_upspeak",True)
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    print(response1.json())
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    with open(filepath,mode="wb") as f:
        f.write(response2.content)
        f.close()
    

if __name__ == "__main__":
    discord_access_token = "";
    discord_application_id = "";

    with open("config.yml") as config_file:
        obj = yaml.safe_load(config_file)
        discord_access_token = str(obj["access_token"])
        discord_application_id = str(obj["application_id"])

    client = discord.Client(intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)
    @client.event
    async def on_ready():
        print("Bot started!")
        print(f"https://discord.com/api/oauth2/authorize?client_id={discord_application_id}&permissions=3148864&scope=bot%20applications.commands")
        await tree.sync()#スラッシュコマンドを同期
    @tree.command(name="vrvcv",description="change rvc model")
    async def change_rvcmodel_command(interaction:discord.Interaction,text:str):
        rvc_client.predict(
				text,	# 推論ファイル
				0,
				0,
				api_name="/infer_change_voice")
        await interaction.response.send_message("変更しました。",ephemeral=True)
    @tree.command(name="vjoin",description="ボイスチャットにボットを追加。")
    async def join_command(interaction:discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("ボイスチャンネルに接続してください。",ephemeral=True)
        else:
            await interaction.response.send_message("ボイスチャンネルに接続中です。")
            await interaction.user.voice.channel.connect()
    @tree.command(name="vleave",description="ボイスチャットから切断します。")
    async def join_command(interaction:discord.Interaction):
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("切断しました。")
    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        else:
            if message.guild.voice_client is not None:
                generate_wav(message.content,2,f"temp/wav/{message.content}.wav")
                print("input:"+str(os.path.abspath(f"temp/wav/{message.content}.wav")))
                rvc_voice_path = rvc(os.path.abspath(f"temp/wav/{message.content}.wav"))
                print("Playing:"+rvc_voice_path)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(rvc_voice_path))
                print(message.content)

    client.run(discord_access_token)
