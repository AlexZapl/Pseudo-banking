#print(f'2000 человек: {"🏃"*500}')

from forex_python.converter import CurrencyRates
c = CurrencyRates()
result = c.convert('USD', 'EUR', 100)
print(result)

#from AlexZapl_db import db

#print(db.users.get('login', 'AlexZapl'))
#print(db.users.get('login', 'AlexZapl').password)
#from random import  randint

#cvvs = []
#for o in range(10):
#    cvvs.append(f'{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}-{randint(0,1)}{randint(0,9)}-{randint(0,3)}{randint(0,9)}')
#print(cvvs)
#for i in cvvs:
#    cvve = f'{i[2]}{i[3]}/{i[5]}{i[6]}'
#    print(cvve)