from discord.ext import commands
from .functions import *
import db_setup
import discord
import io
import random
import chess
import chess.pgn
import asyncio
import aiohttp




class Chess(commands.Cog, name = 'Chess Commands'):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="register", aliases=["reg"])
    async def register(self, ctx):
        reg_user_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.registered_user_collection)
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
        reg_user_col = await challenge_checker(ctx, opponent)
        if reg_user_col is not None:
            return
        
        challenge_message = await ctx.send(f"Hey {opponent.mention}! {ctx.author.mention} challenged you for a chess game. If you want to accept challenge react with 👍")
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
            
            try:
                reg_user_col.insert_one(make_game(first_mover, second_mover, game_id))
                await ctx.reply("Game created successfully", mention_author=False)
                await ctx.send(f'Game id: `{game_id}`')
                await ctx.send(f'{first_mover.mention} will move first as white')
            except Exception:
                await ctx.reply("Something went wrong!", mention_author=False)
            return






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
