from discord.ext import commands
from db_setup import *
from datetime import datetime
import discord
import io
import random
import string
import chess
import chess.pgn
import asyncio
import aiohttp


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
        