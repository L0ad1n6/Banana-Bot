from subprocess import Popen
import yaml
import time
import os
from dotenv import load_dotenv
from websocket import create_connection
from websocket._exceptions import WebSocketBadStatusException

def ping():
    while True:
        try:
            create_connection("ws://127.0.0.1:2335")
        except ConnectionRefusedError:
            pass
        except WebSocketBadStatusException:
            return
        time.sleep(0.3)

def configure():
    load_dotenv()
    
    with open("application.yml") as f:
        app = yaml.load(f, Loader=yaml.FullLoader)
        app["server"]["port"] = int(os.getenv("PORT"))

    with open("application.yml", "w") as f:
        yaml.dump(app, f)


def run():
    configure()
    Popen(["java", "-jar", "src/lavalink/Lavalink.jar"])
    ping()

if __name__ == "__main__":
    run()