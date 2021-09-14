# mport utils_func.database as db
# import genshinstats as gs

# async def save(ctx):
#   split = ctx.message.content.split()
#   l = len(split)
#   if l == 3:
#     uid = split[1]
#     username = split[2]
#     if gs.is_game_uid(uid):
#       if db.name_is_existed(username):
#         await ctx.message.channel.send(f"**{username}** already existed as UID: **{db.get_firstkey_from_name(username)}**")
#       else:  
#         db.cache_uid_to_username(uid, username)
#         await ctx.message.channel.send(f"Cache your UID({uid}) successfully with name as **{username}**")
#     else:
#       await ctx.message.channel.send("`UID is invalid!`")  
#   else:
#     await ctx.message.channel.send("command is: ``save {uid} {username}``")     

# async def delete(ctx):
#   split = ctx.message.content.split()
#   l = len(split)
#   if l == 2:
#     uid = split[1]
#     if gs.is_game_uid(uid):
#       if db.uid_is_existed(uid):
#         db.delete_uid(uid)
#         await ctx.message.channel.send(f"Delete successfully: **{uid} - {db.get_username_from_uid(uid)}**")
#       else:  
#         await ctx.message.channel.send(f"{uid} not existed in database!")
#     else:
#       await ctx.message.channel.send("`UID is invalid!`")  
#   else:
#     await ctx.message.channel.send("command is: ``delete {uid}``")   

# def show(ctx):
#   keys = db.get_all_keys()
#   for key in keys:
#     print(key + " - " + db.get_username_from_uid(key))