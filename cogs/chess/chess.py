from discord.ext import commands
from .functions import *
from db_setup import *
import discord
import json
import io
import random
import chess
import chess.pgn
import asyncio
import aiohttp


class Chess(commands.Cog, name = 'Chess Commands'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="challenge", aliases=["cl"])
    async def challenge(self, ctx,  opponent: discord.Member = None):
        pass


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