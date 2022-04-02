from discord.ext import commands
from dotenv import load_dotenv
import os
from time import sleep

from commands import Moderation, SocialCredit, Utility, Help, Default, Music, Error
from server import run

def main():
    bot = commands.Bot(command_prefix=["--", "—"])
    bot.remove_command("help")
    print("[Bot] Initialized")

    bot.add_cog(Moderation(bot))
    bot.add_cog(SocialCredit(bot))
    bot.add_cog(Utility(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Music(bot))
    bot.add_cog(Default(bot))
    bot.add_cog(Error(bot))
    print("[Bot] Cogs and commands added to bot")

    print(f"[Bot] Running on port {os.getenv('PORT')}...")
    bot.run(os.getenv("token"))

if __name__ == "__main__":
    load_dotenv()
    run()
    main()
