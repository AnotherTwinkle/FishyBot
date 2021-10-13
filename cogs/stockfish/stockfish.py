from discord.ext import commands
import stockfish


class Stockfish(commands.Cog, name = 'Stockfish Commands'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="evaluation", aliases=["eval", "ev"])
    async def position_eval(self, ctx):
        pass
    


def setup(bot):
    bot.add_cog(Stockfish(bot))