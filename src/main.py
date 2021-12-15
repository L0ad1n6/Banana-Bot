import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

from moderation import Moderation
from social_credit import SocialCredit
from utility import Utility
from help import Help
load_dotenv()

def main():
    bot = commands.Bot(command_prefix="--")
    # bot.remove_command("help")

    bot.add_cog(Moderation(bot))
    bot.add_cog(SocialCredit(bot))
    bot.add_cog(Utility(bot))
    # bot.add_cog(Help(bot))

    bot.run(os.getenv("token"))

if __name__ == "__main__":
    main()
