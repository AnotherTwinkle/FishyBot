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
    try:
        reg_user_col = db_setup.setup_db_collection(db_setup.db_name, db_setup.registered_user_collection)
    except:
        return False
    
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


async def challenge_creator(self, ctx, opponent, games_col, reg_user_col):
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
            reg_user_col.update_one({'_id':first_mover.id}, {'$set':{
                "is_playing": True,
                "playing_as_color": "white",
                "current_game_id": game_id,
                "opponent": second_mover.id,
            }})
            reg_user_col.update_one({'_id':second_mover.id}, {'$set':{
                "is_playing": True,
                "playing_as_color": "black",
                "current_game_id": game_id,
                "opponent": first_mover.id,
            }})
            games_col.insert_one(make_game(first_mover, second_mover, game_id))
            await ctx.reply("Game created successfully", mention_author=False)
            await ctx.send(f'Game id: `{game_id}`')
            await ctx.send(f'{first_mover.mention} will move first as white')
        except Exception:
            await ctx.reply("Something went wrong!", mention_author=False)
    return


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