from utils.models import *
import sys
m = Match.select().where(Match.id == sys.argv[1]).get()
r = Result.select().where(Result.match == m).get()
w= r.winner
print(m.id,m.team1.name,m.team2.name,m.mdate,m.mtime)
if Bet.select().where(Bet.match == m).exists():
           for bt in Bet.select().where(Bet.match == m):
               print("User:::"+str(bt.user.name))
               if w.id == bt.bet.id:
                   print("+2")
                   #Points.create(user=bt.user,match=m,value=2,datecreated=date.today())
               else:
                   print("-2")
                   #Points.create(user=bt.user,match=m,value=-2,datecreated=date.today())
