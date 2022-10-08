import nextcord, asyncio, json
from nextcord.ext import commands
base_dir = './Python/Discord Bot/ChingChong 2.0/'

def ajt_conf(ctx,event,perk,bool,config):
   if bool=="true":
      with open(base_dir+'db.json','r') as db:
         data = json.load(db)
      try:
         data["admin"][str(ctx.guild)][event][perk] = [True,config]
      except:
         data["admin"][str(ctx.guild)][event] = {perk:[True,config]}
      with open(base_dir+"db.json","w") as db:
         json.dump(data,db,indent=3,ensure_ascii=False)
   elif bool=="false":
      with open(base_dir+'db.json','r') as db:
         data = json.load(db)
      try:
         data["admin"][str(ctx.guild)][event].pop(perk)
      except:
         pass
      with open(base_dir+"db.json",'w') as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

def db_checker(guild,event,perk):
   """Check si la permission est activée ou non."""
   with open(base_dir+"db.json",'r') as db:
      data = json.load(db)
   try: 
      return data["admin"][str(guild)][event][perk]
   except:
      return [False,""]

class Admin(commands.Cog):
   def __init__(self, client):
      self.client = client

   # @commands.Cog.listener()
   # async def on_command_error(self,ctx,error):
   #    if isinstance(error, commands.CommandNotFound):
   #       await ctx.send('Commande non existante.')

   @commands.Cog.listener()
   async def on_guild_join(self,guild):

      with open(base_dir+'db.json','r') as db:
         data = json.load(db)

      data["admin"][str(guild)] = {}

      with open(base_dir+'db.json','w') as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

      embed=nextcord.Embed(title=f"C'est moi uesh !",description = f"{self.client.user.mention} pour vous servir.",color=0x65c0d7)
      embed.set_thumbnail(url="https://pbs.twimg.com/media/E4ZgAxmWEAImyGF.jpg")
      embed.add_field(name="Pour que le bot fonctionne correctement, il faudrait mettre son rôle au dessus de tous.", value="$config pour commencer la configuration du bot et $help pour la liste des commandes.", inline="False")
      await guild.system_channel.send(embed=embed)

   @commands.Cog.listener()
   async def on_guild_remove(self,guild):

      with open(base_dir+'db.json','r') as db:
         data = json.load(db)

      data['admin'].pop(str(guild))

      with open(base_dir+'db.json','w') as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

   @commands.Cog.listener()
   async def on_member_join(self, member):
      #Ajouter rôle
      roleadd = db_checker(member.guild,"on_member_join","role_add")
      if roleadd[0]:
         role = nextcord.utils.get(member.guild.roles, id=int(roleadd[1]))
         await member.add_roles(role)
      else:
         #TODO
         pass

      #Envoyer un message dans un channel
      sennd = db_checker(member.guild,'on_member_join','welcome')
      if sennd[0]:
         asyncio.sleep(1)
         await member.guild.get_channel(int(sennd[1].split(' ')[0])).send(' '.join(sennd[1].split(' ')[1:]))
      else:
         #TODO
         pass
      
      #Envoyer un mp
      mpp = db_checker(member.guild,'on_member_join','dm')
      if mpp[0]:
         await member.send(mpp[1])
      else:
         #TODO
         pass

   @commands.Cog.listener()
   async def on_member_remove(self, member):
      quitte = db_checker(member.guild,"on_member_remove","sayonara")
      if quitte[0]:
         await member.guild.get_channel(int(quitte[1].split(' ')[0])).send(' '.join(quitte[1].split(' ')[1:]))
      else:
         #TODO
         pass

   # Commands

   @commands.command()
   @commands.has_permissions(administrator=True)
   async def config(self,ctx,event="",perk="",boul="",*,config=""):
      """Pour configurer le bot sur votre server !"""
      event,perk,boul,config=event.lower(),perk.lower(),boul.lower(),config.strip()
      if event=="":
         await ctx.send("```\nVoici une liste de configurations, utilisez $config (nom config) afin d'accéder au sous menu (ex : $config on_member_join)\n\non_member_join : - Ajout d'un rôle\n                 - Message dans channel spécifique\n                 - Message privé à l'utilisateur\n\non_member_remove : - Message d'au revoir\n```")
      elif event == "on_member_join":
         if perk=="":
            await ctx.send("```\nPour activer/désactiver les fonctionnalités, suivez les exemples :\n\n- Ajout d'un rôle :                   $config on_member_join role_add true|false (ID du rôle)\n- Message dans channel spécifique :   $config on_member_join welcome true|false (channel ID) (message)\n- Message privé à l'utilisateur :     $config on_member_join dm true|false (message)\n```")
         elif perk=="role_add":
            ajt_conf(ctx,event,perk,boul,config)
         elif perk=="welcome":
            ajt_conf(ctx,event,perk,boul,config)
         elif perk=="dm":
            ajt_conf(ctx,event,perk,boul,config)
      elif event == "on_member_remove":
         if perk=="":
            await ctx.send("```\nPour activer/désactiver les fonctionnalités, suivez les exemples :\n\n- Message d'au revoir : $config on_member_remove sayonara true|false (channel ID) (message)\n```")
         elif perk=="sayonara":
            ajt_conf(ctx,event,perk,boul,config)
      else:
         await ctx.send("Config non prise en compte.")
      
   @commands.command(aliases=['ms'])
   async def ping(self, ctx):
      """Affichez le temps de réaction du bot."""
      await ctx.send(f'{round(self.client.latency * 1000)}ms')



   @commands.command()
   @commands.has_permissions(manage_messages=True)
   async def clear(self, ctx, nb):
      await ctx.channel.purge(limit=nb+1)

   @commands.command()
   @commands.has_permissions(manage_roles=True)
   async def neant(self, ctx, member : commands.MemberConverter, time, *, reason=''):
      """Pour jetter quelqu'un dans le néant."""
      #TODO InConfig checker
      multiplier = {"s":1,"m":60,"h":3600}
      nb,unit = int(time[:-1]),time[-1]
      role = nextcord.utils.get(ctx.guild.roles, name='Néant')
      old_roles= [x for x in ctx.guild.get_member(member.id).roles][1:]

      await member.remove_roles(*old_roles)
      await member.add_roles(role)
      await ctx.send(f'{member.mention} a été jeté dans le {role} pendant {time}. Raison : {reason}')
      await asyncio.sleep(nb*multiplier[unit])
      await member.remove_roles(role)
      await member.add_roles(*old_roles)

   @commands.command()
   @commands.has_permissions(manage_roles=True)
   async def unneant(self, ctx, member: commands.MemberConverter):
      #TODO InConfig checker
      """Bon c'est dans le nom.."""
      await member.remove_roles(nextcord.utils.get(ctx.guild.roles, name="Néant"))
      await member.add_roles(nextcord.utils.get(ctx.guild.roles, name="haum"))



def setup(client):
   client.add_cog(Admin(client))