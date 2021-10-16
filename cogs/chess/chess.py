from discord.ext import commands
from .functions import *
from db_setup import *
import discord
import io
import random
import chess
import chess.pgn
import asyncio
import aiohttp


db_name = "fishyBot"
registered_user_collection = "Registered Users"
analysis_board_collection = "Analysis Boards"
banned_user_collection = "Banned Users"
games_collection = "Game Archives"



class Chess(commands.Cog, name = 'Chess Commands'):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="register", aliases=["reg"])
    async def register(self, ctx):
        reg_user_col = setup_db_collection(db_name, registered_user_collection)
        if registered_user(ctx.author.id, reg_user_col):
            await ctx.reply("You have already registered dude :/", mention_author=False)
            return
        try:
            reg_user_col.insert_one(make_user(ctx.author.id))
            await ctx.reply("Registered successfully", mention_author=False)
        except Exception:
            await ctx.reply("Something went wrong!", mention_author=False)
        return



    @commands.command(name="challenge", aliases=["cl"])
    async def challenge(self, ctx,  opponent: discord.Member = None):
        if opponent is None:
            await ctx.reply("Mention someone to challenge :|", mention_author=False)
            return
        if opponent == ctx.author:
            await ctx.reply("Hmm... So you want to challenge yourself. Open an analysis board instead! :thinking:", mention_author=False)
            return

        reg_user_col = setup_db_collection(db_name, registered_user_collection)
        if not registered_user(ctx.author.id, reg_user_col):
            await ctx.reply("Please register first.", mention_author=False)
            return
        if not registered_user(opponent.id, reg_user_col):
            await ctx.reply("The person you are asking to play hasn\'t registered yet.", mention_author=False)
            return


        if check_current_game(ctx.author.id, reg_user_col):
            await ctx.reply("You are already in a game", mention_author=False)
            return
        if check_current_game(opponent.id, reg_user_col):
            await ctx.reply("You'r opponent is already in a game", mention_author=False)
            return

        challenge_message = await ctx.send(f"Hey {opponent.mention}! {ctx.author.mention} challenged you to a chess game. If you want to accept challenge react with 👍")
        await challenge_message.add_reaction("👍")
        def accept(reaction, user):
            return user == opponent and str(reaction.emoji) == '👍'
        try:
            await self.bot.wait_for('reaction_add', timeout=30.0, check=accept)
        except asyncio.TimeoutError:
            await ctx.send('No response...\nChallenge declined')
        else:
            await ctx.send('Challenge accepted... Let the game begin!!!')
            players = [ctx.author, opponent]
            first_mover = random.choice(players)
            players.remove(first_mover)
            second_mover = players[0]
            game_id = random_string(20)
            await ctx.send(f'Game id: `{game_id}`')

            await ctx.send(f'{first_mover.mention} will move first as white')



    @commands.command(name="move", aliases=["m"])
    async def move(self, ctx, *, arg):
        pass


    @commands.command(name="watch", aliases=["w"])
    async def watch(self, ctx):
        pass


    @commands.command(name="show", aliases=["s"])
    async def show(self, ctx, *, arg):
        pass

            
            
            
        


def setup(bot):
    bot.add_cog(Chess(bot))
