from replit import db

def cache_uid_to_username(uid, nickname):
  db[uid] = nickname

def get_username_from_uid(uid):
  value = db[uid]
  return value

def delete_uid(uid):
  del db[uid]

def get_all_keys():
  keys = db.keys()  
  return keys

def get_firstkey_from_name(name):
  keys = get_all_keys()
  if keys is not None:
    for uid in keys:
      username = get_username_from_uid(uid)
      if (username == name):
        return uid
      else:
        return None  
  else:
    return None      

def name_is_existed(name):
  keys = get_all_keys()
  for uid in keys:
    if name == get_username_from_uid(uid):
      return True
  return False  

def uid_is_existed(uid):
  keys = get_all_keys()
  if uid in keys:
    return True
  else:
    return False      