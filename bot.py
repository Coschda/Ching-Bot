import nextcord, os
from nextcord.ext import commands

#https://github.com/Coschda/Discord-Bot

class CustomHelpCommand(commands.HelpCommand):

   def __init__(self):
      super().__init__()
   
   async def send_bot_help(self, mapping):
      retour,dots = "\n","..."
      message = "```\n"+"".join(f"{x.qualified_name}: \n{f'{retour}'.join(f'     {x.name}: {x.help if len(str(x.help))<100 else x.help[:100]+dots}' for x in mapping[x] if x.name not in '[],')}\n\n" for x in mapping if str(x)!="None")+"\nUtilisez $help (catégorie) et $help (commande) pour plus d'infos."+"\nCe bot est également OpenSource, retrouvez son code sur GitHub : https://github.com/Coschda/Discord-Bot."+"```"
      await self.get_destination().send(message)

   async def send_cog_help(self, cog):
      message = "```"+f"{cog.get_commands()[0].attrs}"+"```"
      await self.get_destination().send(message)
   
   async def send_group_help(self, group):
      message = "J'ai eu la flemme de le faire :)"
      await self.get_destination().send(message)

   async def send_command_help(self, command):
      message = "J'ai eu la flemme de le faire :)"
      await self.get_destination().send(message)
      

intents = nextcord.Intents.all()
#intents member
client = commands.Bot(command_prefix="$", intents=intents, help_command=CustomHelpCommand())


for filename in os.listdir('./Python/Discord Bot/ChingChong 2.0/cogs'):
   if filename.endswith('.py'):
      client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def load(ctx, extension):
   client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
   client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
   client.unload_extension(f'cogs.{extension}')
   client.load_extension(f'cogs.{extension}')
   await ctx.send(f"Cog {extension} reloaded.")

@client.event
async def on_ready():
   await client.change_presence(status=nextcord.Status.dnd, activity=nextcord.Game("C'est moi uesh"))
   print('Bot connecté.')

client.run()