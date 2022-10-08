import nextcord, asyncio, json
from nextcord.ext import commands, tasks
from datetime import datetime
db_path = './Python/Discord Bot/ChingChong 2.0/db.json'
      

class Rappels(commands.Cog):
   def __init__(self, client):
      self.client = client
      self.send_remind.start()

   @commands.command()
   async def remind(self, ctx, date, time, *, message):
      #TODO Améliorer UI
      with open(db_path,'r') as db:
         data = json.load(db)

      if int(time.split(':')[0]) / 10 <1:
         time = "0"+str(int(time.split(':')[0]))+":"+time.split(':')[1]

      if date in data['reminder']:

         if time in data['reminder'][date]:
            if str(ctx.author.id) in data['reminder'][date][time]:
               data['reminder'][date][time][str(ctx.author.id)].append(message)
            else:
               data['reminder'][date][time][str(ctx.author.id)] = [message]
         else:
            data['reminder'][date][time] = {str(ctx.author.id) : [message]}
      else:
         data['reminder'][date] = {
            time : {
               str(ctx.author.id) : [message]
            }
         }

      await ctx.send(f"Reminder créé pour le {date} à {time}. Il vous sera envoyé en message privé.")

      with open(db_path,'w') as db:
         json.dump(data,db,indent=3,ensure_ascii=False)

   @tasks.loop(minutes=1.0)
   async def send_remind(self):
      with open(db_path,'r') as db:
         data = json.load(db)
      cur_date,cur_time = datetime.now().strftime('%d/%m/%Y'),datetime.now().strftime("%H:%M")
      try:
         for user in data['reminder'][cur_date][cur_time]:
            for message in data['reminder'][cur_date][cur_time][user]:
               await nextcord.utils.get(self.client.get_all_members(), id=int(user)).send(f"Rappel pour {cur_time} : {message}")
         data['reminder'][cur_date].pop(cur_time)
         if cur_date in data['reminder']:
            data['reminder'].pop(cur_date)
         with open(db_path,'w') as db:
            json.dump(data,db,indent=3,ensure_ascii=False)
      except:
         pass
      
      


def setup(client):
   client.add_cog(Rappels(client))