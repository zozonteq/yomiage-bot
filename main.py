import discord
from discord import app_commands
import yaml
import requests
import json
import wave


def generate_wav(text, speaker=1, filepath='./temp/audio.wav'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()


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
                generate_wav(message.content,2,f"./temp/{message.content}.wav")
                message.guild.voice_client.play(discord.FFmpegPCMAudio(f"./temp/{message.content}.wav"))
                print(message.content)

    client.run(discord_access_token)
