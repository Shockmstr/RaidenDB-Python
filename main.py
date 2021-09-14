from utils_func.keep_alive import keep_alive
import utils_func.utils as utils
import utils_func.database as db
import main_func.abyss as ab
import os
import genshinstats as gs
import discord
import traceback
from discord.ext import commands
from discord.utils import get
from discord import Embed


client = discord.Client()
client = commands.Bot(command_prefix='!!')  # prefix our commands with '.'
gs.set_cookie(ltuid=os.environ['ltuid']
,ltoken=os.environ['ltoken'])

WIKI_URL = "https://genshin-impact.fandom.com/wiki/"

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')

@client.command()
async def ch(ctx):
  async with ctx.typing():
    try:
      split = ctx.message.content.split()
      l = len(split)
      if l < 3:
        tmp = split[1]
        uid = 0
        if gs.is_game_uid(tmp):
          uid = tmp
        else:
          cacheUID = db.get_firstkey_from_name(tmp)
          if (cacheUID is not None):
            uid = cacheUID
          else:  
            uid = utils.nameToUID(tmp)  
        characters = gs.get_characters(uid)
        result = ""
        for char in characters:
          str = "{0}* {1} - lvl {2} C{3} + {4} R{5}".format(char['rarity'], char['name'], char['level'], char['constellation'], char['weapon']['name'], char['weapon']['refinement'])
          result += str + '\n'
        await ctx.message.channel.send(result)
      elif l == 3:
        tmp = split[1]
        uid = 0
        if gs.is_game_uid(tmp):
          uid = tmp
        else:
          cacheUID = db.get_firstkey_from_name(tmp)
          if (cacheUID is not None):
            uid = cacheUID
          else:  
            uid = utils.nameToUID(tmp) 
        charName = split[2]
        characters = gs.get_characters(uid)
        str2 = ''
        hasChar = False 
        for char in characters:
          if charName.lower() in char['name'].lower():
            hasChar = True
            url=WIKI_URL+char['name'].replace(" ", "_");
            embed = Embed(title=char['name'], description=f"{char['rarity']}* {char['element']}",url=url, color=discord.Color.blue())
            embed.set_thumbnail(url=char['icon'])
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Level", value=f"{char['level']}", inline=True)
            embed.add_field(name="Constellation", value=f"{char['constellation']}", inline=True)
            embed.add_field(name="Friendship", value=f"{char['friendship']}", inline=True)
            embed.add_field(name=char['weapon']['name'], value=f"{char['weapon']['rarity']}* {char['weapon']['type']}", inline=True)
            embed.add_field(name="Level", value=f"{char['weapon']['level']}", inline=True)
            embed.add_field(name="Refinement", value=f"{char['weapon']['refinement']}", inline=True)
            str2 = ''
            for artif in char['artifacts']:
              str2 += '**{0}**: {1}* {2} +{3} - {4}\n'.format(artif['full_pos_name'], artif['rarity'], artif['name'], artif['level'], artif['set']['name'])
            embed.add_field(name="Artifacts", value=str2,inline=False)
            embed.set_footer(text=f"UID: {uid}")
            await ctx.message.channel.send(embed=embed)
        if (hasChar == False):
          await ctx.message.channel.send("No character is found!")
      else:
        await ctx.message.channel.send("command is: ``ch {uid/username} {charName}``")  
    except Exception:
      print(traceback.format_exc())
      await ctx.message.channel.send("UID not found or UID is hidden")
 
@client.command()
async def uid(ctx):
  async with ctx.typing():
    try:
      split = ctx.message.content.split()
      l = len(split)
      if l < 3:
        await ctx.message.channel.send("command is: ``uid {uid} [stat/teapot/exploration]``")           
      elif l==3:
        tmp = split[1]
        parameter = split[2]
        uid = 0
        if gs.is_game_uid(tmp):
          uid = tmp
        else:
          cacheUID = db.get_firstkey_from_name(tmp)
          if (cacheUID is not None):
            uid = cacheUID
          else:  
            uid = utils.nameToUID(tmp) 
        stats = gs.get_user_stats(uid)
        if (parameter.lower() == 'stat'):
          strStat = ''
          statkey = [*stats['stats']] # get all list of key in stats
          for key in statkey:     
            keyNameFormat = key.replace("_", " ").capitalize()   
            strStat += f"{keyNameFormat}: {stats['stats'].get(key)}\n"
          embed = Embed(title="Stats", color=discord.Color.blue()) 
          embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
          embed.description = strStat
          embed.set_footer(text=f"UID: {uid}")
          await ctx.message.channel.send(embed=embed)    
           
        elif (parameter.lower() == 'teapot'):
          strTea = ''
          embed = Embed(title="Teapots", color=discord.Color.red()) 
          embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
          embed.set_footer(text=f"UID: {uid}")
          for area in stats['teapots']:
            teakey = [*area]          
            for key in teakey:     
              if not(key == "name" or key == "icon" or key == "comfort_icon"):
                keyNameFormat = key.replace("_", " ").capitalize()   
                strTea += f"{keyNameFormat}: {area.get(key)}\n"          
            embed.add_field(name=f"{area['name']}", value=strTea, inline=True)
          await ctx.message.channel.send(embed=embed)

        elif (parameter.lower() == 'exploration'):
          strEx = ''
          embed = Embed(title="Explorations",color=discord.Color.red()) 
          embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
          embed.set_footer(text=f"UID: {uid}")
          for area in stats['explorations']:
            strEx = ''
            areakey = [*area]
            for key in areakey:                   
              if not(key == "name" or key == "icon"):
                if (key == "explored"):
                  keyNameFormat = key.replace("_", " ").capitalize()   
                  strEx += f"{keyNameFormat}: {area.get(key)}%\n"
                elif (key == "offerings"):
                  for offerArea in area['offerings']:
                    offerKeys = [*offerArea]                  
                    for offerKey in offerKeys:
                      strEx += f"Offerings - {offerKey.capitalize()}: {offerArea.get(offerKey)}\n"
                else: 
                  keyNameFormat = key.replace("_", " ").capitalize()   
                  strEx += f"{keyNameFormat}: {area.get(key)}\n"
            embed.add_field(name=f"{area['name']}", value=strEx, inline=True)
          # print(embed)  
          await ctx.message.channel.send(embed=embed)  
        else:  
          await ctx.message.channel.send("``Wrong parameter(stat/teapot/exploration)`` ")
    except Exception:
      print(traceback.format_exc())
      await ctx.message.channel.send("")

@client.command()
async def abyss(ctx):
  async with ctx.typing():
    try:
      split = ctx.message.content.split()
      l = len(split)
      if l < 3:
        await ctx.message.channel.send("command is: ``abyss {uid} [stat/teapot/exploration]``")           
      elif l==3:
        uid = split[1]
        parameter = split[2]
        embed = ab.abyss_switcher(parameter, uid, ctx)
        await ctx.message.channel.send(embed=embed)
        # print(stats)       
    except Exception:
      print(traceback.format_exc())
      await ctx.message.channel.send("")
   
@client.command()
async def hsearch(ctx):
  async with ctx.typing():
    split = ctx.message.content.split()
    name = split[1]    
    resStr = ""
    isFound = False
    retry = 0
    while not isFound and retry <= 5:
      retry = retry + 1
      results = gs.search(name, size=100)
      for result in results:
        uid = gs.get_uid_from_hoyolab_uid(result['uid'])
        nickname = result['nickname']
        if uid is not None and nickname == name:
          isFound = True
          resStr += "Nickname: {} (HoyoID = {} , UID = {})\n".format(nickname, result['uid'], uid)
    await ctx.message.channel.send(resStr)

@client.command()
async def save(ctx):
  split = ctx.message.content.split()
  l = len(split)
  if l == 3:
    uid = split[1]
    username = split[2]
    if gs.is_game_uid(uid):
      if db.name_is_existed(username):
        await ctx.message.channel.send(f"**{username}** already existed as UID: **{db.get_firstkey_from_name(username)}**")
      else:  
        db.cache_uid_to_username(uid, username)
        await ctx.message.channel.send(f"Cache your UID({uid}) successfully with name as **{username}**")
    else:
      await ctx.message.channel.send("`UID is invalid!`")  
  else:
    await ctx.message.channel.send("command is: ``save {uid} {username}``")     
  
@client.command()
async def delete(ctx):
  split = ctx.message.content.split()
  l = len(split)
  if l == 2:
    uid = split[1]
    if gs.is_game_uid(uid):
      if db.uid_is_existed(uid):
        name = db.get_username_from_uid(uid)
        db.delete_uid(uid)
        await ctx.message.channel.send(f"Delete successfully: **{uid} - {name}**")
      else:  
        await ctx.message.channel.send(f"{uid} not existed in database!")
    else:
      await ctx.message.channel.send("`UID is invalid!`")  
  else:
    await ctx.message.channel.send("command is: ``delete {uid}``")

@client.command()
async def show(ctx):
  keys = db.get_all_keys()
  for key in keys:
    print(key + " - " + db.get_username_from_uid(key))

keep_alive()
token = os.environ['token']
client.run(token)