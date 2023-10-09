import yaml
from src import logger

class Config:
    discord_access_token = ""
    discord_application_id = ""

    rvc_disabled = False
    rvc_host = "localhost"
    rvc_port = 7865

    voicevox_host = "localhost"
    voicevox_port = 50021

    max_text_length = 40
    def __init__(self) :
        try:
            with open("config.yml") as config_file:
                obj = yaml.safe_load(config_file)
                try:
                    self.discord_access_token = str(obj["access_token"])
                    self.discord_application_id = str(obj["application_id"])
                except:
                    print("")
                try:
                    self.rvc_disabled = bool(obj["rvc_disabled"])
                    self.rvc_host = str(obj["rvc_host"])
                    self.rvc_port = int(obj["rvc_port"])

                    self.voicevox_host = str(obj["voicevox_host"])
                    self.voicevox_port = int(obj["voicevox_port"])

                    self.max_text_length = int(obj["max_text_length"])
                except KeyError as e:
                    logger.Error(f"キー {e.__str__()} が config.yml に存在しません。")
                except ValueError as e:
                    logger.Error(f"config.yml の値が不正です。")
        except FileNotFoundError:
            logger.Error("config.yml が存在しません。")
        except yaml.scanner.ScannerError as e:
            logger.Error("config.yml をパースできませんでした。文法に誤りがある可能性があります。")
if __name__ == "__main__":
    Config()