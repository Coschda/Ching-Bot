import nextcord,random,json
from nextcord.ext import commands
db_p = './Python/Discord Bot/ChingChong 2.0/db.json'

def sad_ending(message):
   message.content = "".join(x for x in message.content if x not in "- ?!.").lower().strip()
   with open(db_p,'r') as db:
      data = json.load(db)
   
   if str(message.guild) not in data["sad"]:
      data["sad"][str(message.guild)] = {}

   key_list = [x for x in data["sad"][str(message.guild)].keys()]
   for i in key_list:
      if message.content.endswith(i):
         return random.choice(data["sad"][str(message.guild)][i])

   return None
   
# ERREURS POSSIBLES :
# On ne donne pas de réponse (missing argument)


class Divertissement(commands.Cog):
   def __init__(self, client):
      self.client = client

   @commands.Cog.listener()
   async def on_message(self, message):

      if message.author == self.client.user:
         return

      if sad_ending(message)!= None and not message.content.startswith("$rem"):
         await message.channel.send(sad_ending(message))

   @commands.command()
   async def add_end(self,ctx, aliases, reponses):
      """Donnez lui des fin de mots et des réponses pour que le Bot y réponde. Si vous lui donnez plusieurs réponses, il en prendra une au hasard."""
      #ex : $add_end ni/nni/nis/nid ga/gga/ggga
      with open(db_p,'r') as db:
         data = json.load(db)

      quoi= aliases.lower().strip().split('/')
      feur =  reponses.lower().strip().split('/')

      with open(db_p) as db:
         data = json.load(db)

      try:
         for i in quoi:
            i = i.lower()
            data['sad'][str(ctx.guild)][i] = feur
      except:
         for i in quoi:
            i = i.lower()
            data['sad'][str(ctx.guild)] = {i: feur}

      await ctx.send(f"Les suffixes {str(quoi)[1:-1]} ont été ajoutés avec comme réponse {str(feur)[1:-1]}")

      with open(db_p,"w") as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

   @commands.command()
   async def rem_end(self, ctx, alias):
      with open(db_p,'r') as db:
         data = json.load(db)

      try:
         data['sad'][str(ctx.guild)].pop(alias.strip().lower())
         await ctx.send(f"Toutes les réponses du suffixe '{alias}' ont été supprimées.")
      except:
         await ctx.send("Erreur lors de la suppression, appelez le dev.")

      with open(db_p,"w") as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

   @commands.command(aliases=['cf'])
   async def coinflip(self, ctx):
      if random.randint(0, 1) == 1:
         await ctx.send('Pile')
      else:
         await ctx.send('Face')

def setup(client):
   client.add_cog(Divertissement(client))