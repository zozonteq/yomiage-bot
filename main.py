import discord
from discord import app_commands
import yaml
import requests
import json
import wave
from gradio_client import Client
import os
import uuid
from src import checker
from src import config
from src import guild_config
from src import guild_tts_manager
#ayaka-jp_e101.pth
#hutao-jp.pth


if __name__ == "__main__":
    config = config.Config()
    rvc_pitch = 0 
    rvc_client = None
    if not config.rvc_disabled:
        rvc_client = Client(f"http://{config.rvc_host}:{config.rvc_port}/")

        result = rvc_client.predict(
            "hutao-jp.pth",	# 推論ファイル
            0,
            0,
            api_name="/infer_change_voice"
        )

    guild_tts_manager = guild_tts_manager.guild_tts_manager()

    def rvc(filepath):
        result = rvc_client.predict(
            0,	
            filepath,	
            rvc_pitch,	#ピッチ
            filepath,
            "pm",	# pm or harvest or crepe
            "Howdy!",	
            "null",	
            0,	
            0,	
            0,	
            0,	
            0,	
            api_name="/infer_convert"
        )
        print("rvc_pitch:"+str(rvc_pitch));
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
    def wav_gen_and_get_path(text): # テキストを受取、生成した読み上げ音声のパスを返す。
        msg_uuid = str(uuid.uuid4())
        generate_wav(text,2,f"temp/wav/{msg_uuid}.wav")
        output_wav_file = os.path.abspath(f"temp/wav/{msg_uuid}.wav")
        if not config.rvc_disabled:
            rvc_voice_path = rvc(os.path.abspath(f"temp/wav/{msg_uuid}.wav"))
            output_wav_file = rvc_voice_path
        return output_wav_file

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
            await interaction.response.send_message("先に、ボイスチャンネルに接続してください。",ephemeral=True)
        else:
            await interaction.user.voice.channel.connect()
            await interaction.response.send_message("ボイスチャンネルに接続しました。")
            wav_path = wav_gen_and_get_path("接続しました。")
            speaked_state = True
            while speaked_state:
                try:
                    interaction.guild.voice_client.play(discord.FFmpegPCMAudio(wav_path))
                except discord.errors.ClientException:
                    pass
                else:
                    speaked_state = False


    @tree.command(name="vleave",description="ボイスチャットから切断します。")
    async def join_command(interaction:discord.Interaction):
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("切断しました。")

    @tree.command(name="vpitch",description="ピッチを調節します。")
    async def pitch_command(interaction:discord.Interaction,value:int):
        global rvc_pitch 
        rvc_pitch = value
        await interaction.response.send_message(f"ピッチを{value}に設定しました。")
        
    @client.event
    async def on_message(message):
        if not message.author.bot:
            if message.guild.voice_client is not None:
                content = message.content
                if len(content) > config.max_text_length:
                    content = content[0:config.max_text_length] + "以下省略"
                if checker.is_url(content):
                    content = "URL"
                if not checker.ignore_check(content):
                    wav_path = wav_gen_and_get_path(content)
                    guild_tts_manager.enqueue(message.guild.voice_client,message.guild,discord.FFmpegPCMAudio(wav_path))



    client.run(discord_access_token)
