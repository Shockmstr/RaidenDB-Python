import genshinstats as gs
import discord
from discord import Embed

def abyss_switcher(parameter, uid, ctx):
  switcher = {
    "stat" : getAbyssStats(uid, ctx),
    "rank" : None,
    "floor" : None
  }
  return switcher.get(parameter, None)

def getAbyssStats(uid, ctx):
    abyss = gs.get_spiral_abyss(uid)
    stats = abyss['stats']
    embed = Embed(title="Stats", color=discord.Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"UID: {uid}")
    for key, stat in stats.items():
      name = key.replace("_", " ").capitalize()
      embed.add_field(name=name, value=stat, inline=True)
    return embed  
   
