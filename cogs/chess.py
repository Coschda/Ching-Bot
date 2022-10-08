import nextcord,random
from nextcord.ext import commands
#from ChessGame.main import Board

class Chess(commands.Cog):
    global randomkey
    randomkey = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&é(-è_çà)])^$ù*,;:!") for i in range(12))
    

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        boucle = False
        if message.author == self.client.user:
            if message.content != randomkey:
                return
            else:
                msg_id = message.id
                boucle = True

        while boucle:
            bot_msg = await message.channel.fetch_message(msg_id)
            user_msg = await self.client.wait_for("message")

            if user_msg.content.startswith("$stop"):
                await message.channel.send("Boucle terminée.")
                boucle = False
            else:

                await bot_msg.edit(content=user_msg.content)
                await user_msg.delete()

    @commands.command()
    async def start(self,ctx):
        await ctx.channel.send(randomkey)

    @commands.command()
    async def stop(self,ctx):
        pass

    @commands.command()
    async def send(self,ctx,txt):
        await ctx.send(txt)

def setup(client):
   client.add_cog(Chess(client))