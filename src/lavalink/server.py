from subprocess import Popen
import yaml
import os
from dotenv import load_dotenv

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

if __name__ == "__main__":
    print(os.getenv("PORT"))
    run()