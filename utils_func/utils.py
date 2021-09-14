import genshinstats as gs


def getUsername(name):
  isFound=False
  retry = 0
  while not isFound and retry <= 5:
    retry = retry + 1
    results = gs.search(name, size=20)
    if results is not None:
      for result in results:
        if result == name:
          return result
          isFound = True
    else: 
      return None  

def nameToUID(name):
  try:
    hoyoName = getUsername(name)
    hoyoUID = hoyoName['uid']
    if (hoyoUID is not None):
      return gs.get_uid_from_hoyolab_uid(hoyoUID)
  except:
    print("error")