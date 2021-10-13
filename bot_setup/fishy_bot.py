import os
import discord
from discord.ext import commands



class FishyBot(commands.Bot):
    def __init__(self, prefix):
        required_intents = discord.Intents.default()
        required_intents.members = True
        super().__init__(command_prefix = prefix, intents = required_intents)
        self.cog_names = ["chess"]


    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f"Connected to Discord (latency: {self.latency*1000:,.3f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")


    async def on_ready(self):
        print("------------------------------------")
        print(f'Logged in as {self.user}')
        print(f'Guilds   : {len(self.guilds)}')
        print(f'Users    : {len(set(self.get_all_members()))}')
        print(f'Channels : {len(list(self.get_all_channels()))}')
        print("------------------------------------")


    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)


    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)
    

    def set_up(self):
        print("\n\nSetting up bot...\n")
        print("Loading cogs...")
        for cog_name in self.cog_names:
            self.load_extension(f"cogs.{cog_name}.{cog_name}")
            print(f"Loaded {cog_name} cog")
        print("All cogs loaded")
        print("--------------------------------------")
        
    

    def run_bot(self):
        print("Running bot...")
        print("--------------------------------------")

        TOKEN = os.environ.get("FISHY_BOT_TOKEN")
        
        self.run(TOKEN, reconnect=True)
