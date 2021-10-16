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
        try:
            reg_user_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.registered_user_collection)
        except Exception:
            await ctx.reply("Something went wrong!", mention_author=False)
        
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
    async def challenge(self, ctx,  opponent: discord.Member = None, *args):
        checker_bool = await challenge_checker(ctx, opponent)
        if checker_bool is None:
            return
        elif checker_bool == False:
            await ctx.reply("Something went wrong!", mention_author=False)
        else:
            reg_user_col = checker_bool
            try:
                games_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.games_collection)
            except Exception:
                await ctx.reply("Something went wrong!", mention_author=False)
        await challenge_creator(self, ctx, opponent, games_col, reg_user_col, args)
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
