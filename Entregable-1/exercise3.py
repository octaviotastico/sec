import os

BASE = '../Tools/Dicts/SecLists/Passwords/'

def crack_with_dict(DIR):
  for dictionary in os.listdir(DIR):
    if os.path.isdir(os.path.join(DIR + dictionary)):
      crack_with_dict(DIR + dictionary + '/')
    else:
      print(f'Analizyng: {DIR + dictionary}')
      DICT = open(DIR + dictionary, 'r+').read()
      EKO = open('./dicts/eko.dict')
      for name in EKO:
        if name in DICT:
          print(f'FOUND {name}')

crack_with_dict(BASE)