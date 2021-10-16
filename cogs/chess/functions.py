from discord.ext import commands
import db_setup
from datetime import datetime
import discord
import io
import random
import string
import chess
import chess.pgn
import asyncio
import aiohttp


async def challenge_checker(ctx, opponent):
    if opponent is None:
        await ctx.reply("Mention someone to challenge :|", mention_author=False)
        return None
    if opponent == ctx.author:
        await ctx.reply("Hmm... So you want to challenge yourself. Open an analysis board instead! :thinking:", mention_author=False)
        return None

    reg_user_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.registered_user_collection)
    if not registered_user(ctx.author.id, reg_user_col):
        await ctx.reply("Please register first.", mention_author=False)
        return None
    if not registered_user(opponent.id, reg_user_col):
        await ctx.reply("The person you are asking to play hasn\'t registered yet.", mention_author=False)
        return None

    if check_current_game(ctx.author.id, reg_user_col):
        await ctx.reply("You are already in a game.", mention_author=False)
        return None
    if check_current_game(opponent.id, reg_user_col):
        await ctx.reply("The person you are challenging is already in a game.", mention_author=False)
        return None
    return reg_user_col





def random_string(len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))



def registered_user(userid, reg_col):
    user = reg_col.find_one({"_id": userid})
    if user is not None:
        return True
    else:
        return False


def get_user(userid, reg_col):
    user = reg_col.find_one({"_id": userid})
    return user


def make_user(userid):
    user_dict = {
        "_id": userid,
        "is_playing": False,
        "playing_as_color": None,
        "current_game_id": None,
        "have_analysis_board": False,
        "current_analysis_board_id": None,
        "opponent": None,
        "games": [],
        "reg_time": datetime.now()
    }
    return user_dict

def check_current_game(userid, reg_col):
    user_dict = get_user(userid, reg_col)
    return user_dict["is_playing"]

def make_game(first_mover, second_mover, game_id):
    user_dict = {
        "_id": game_id,
        "white": first_mover.id,
        "black": second_mover.id,
        "PGN": "",
        "start_time": datetime.now()
    }
    return user_dict