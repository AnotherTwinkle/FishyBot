
import db_setup
import io
import random
import asyncio
import aiohttp

import chess
import chess.pgn

import discord
from discord.ext import commands
from .functions import *


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
    async def challenge(self, ctx, opponent: discord.Member = None, *args):
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
        try:
            reg_user_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.registered_user_collection)
            games_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.games_collection)
        except Exception:
            await ctx.reply("Something went wrong!", mention_author=False)
            
        user = reg_user_col.find_one({"_id":ctx.author.id})
        if not user is not None:
            await ctx.reply("You have already registered dude :/", mention_author=False)
            return
        
        if not user["is_playing"]:
            await ctx.reply("You are not in a game", mention_author=False)
            return
        
        if not user["is_move"]:
            await ctx.reply("Its not your move BrO!", mention_author=False)
            return
        
        game_id = user["current_game_id"]
        
        try:
            game_dict = games_col.find_one({"_id": game_id})
        except Exception:
            await ctx.reply("Something went wrong!", mention_author=False)
            
        pgnstr = game_dict["PGN"]
        pgn = io.StringIO(pgnstr)
        game = chess.pgn.read_game(pgn)
        board = game.board(chess960=game_dict["is_chess960"]) # need to change
        
        for move in game.mainline_moves():
            board.push(move)
            
        try:
            board.push_san(arg)
        except:
            await ctx.send("Illeagal move")
            return
        
        if game_dict["move"] == "B":
            pgnstr += f" {arg}"
            pgnstr += f" {int(pgnstr.split()[len(pgnstr.split()) -3][:-1])+1}."
            now_move = "W"
        else:
            pgnstr += f" {arg}"
            now_move = "B"
            
        game_end = False
        if board.is_checkmate():
            await ctx.reply(f"Checkmate! {ctx.author.mention} won the game")
            game_end = True
            
        elif board.is_stalemate() or board.can_claim_draw():
            await ctx.reply(f"Its a draw!")
            game_end = True
        # try:
        #     reg_user_col.update_one({'_id':ctx.author.id}, {'$set':{
        #         "is_playing": True,
        #         "playing_as_color": "white",
        #         "current_game_id": game_id,
        #         "opponent": second_mover.id,
        #         "is_move": True,
        #     }})
        #     reg_user_col.update_one({'_id':user["opponent"]}, {'$set':{
        #         "is_playing": True,
        #         "playing_as_color": "black",
        #         "current_game_id": game_id,
        #         "opponent": first_mover.id,
        #         "is_move": False,
        #     }})
        #     games_col.insert_one(make_game(first_mover, second_mover, game_id, varient))
        #     await ctx.reply("Game created successfully", mention_author=False)
        #     await ctx.send(f'Game id: `{game_id}`')
        #     await ctx.send(f'{first_mover.mention} will move first as white')
        # except Exception:
        #     await ctx.reply("Something went wrong!", mention_author=False)


        pass


    @commands.command(name="watch", aliases=["w"])
    async def watch(self, ctx):
        pass


    @commands.command(name="show", aliases=["s"])
    async def show(self, ctx, *, arg):
        pass


def setup(bot):
    bot.add_cog(Chess(bot))
    
