import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

from commands.moderation import Moderation
from commands.social_credit import SocialCredit
from commands.utility import Utility
from commands.help import Help
from server import keep_alive

def main():
    bot = commands.Bot(command_prefix="--")
    # bot.remove_command("help")

    bot.add_cog(Moderation(bot))
    bot.add_cog(SocialCredit(bot))
    bot.add_cog(Utility(bot))
    # bot.add_cog(Help(bot))

    bot.run(os.getenv("token"))

if __name__ == "__main__":
    load_dotenv()
    keep_alive()
    main()
