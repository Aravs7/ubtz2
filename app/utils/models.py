__author__ = 'A'

from peewee import *
from datetime import date
from datetime import time
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/var/tmp/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

db = MySQLDatabase('superbets',host="localhost",port=3306,user='root',password='admin')
db.connect()
class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class Team(MySQLModel):

    name = CharField()
    flag = CharField()

    class Meta:
        database = db


class Match(MySQLModel):

    team1 = ForeignKeyField(Team, related_name='team1')
    team2 = ForeignKeyField(Team, related_name='team2')
    mdate = DateField()
    mtime = TimeField()

    class Meta:
        database = db

class User(MySQLModel):

    name = CharField()
    uname = CharField()
    password = CharField()
    image = CharField(default='no-user.jpg')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.uname

    class Meta:
        database = db

class Points(MySQLModel):

    user = ForeignKeyField(User, related_name='for_user')
    match = ForeignKeyField(Match, related_name='on_match')
    value = IntegerField()
    datecreated = DateTimeField()
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.value

    class Meta:
        database = db

class Bet(MySQLModel):

    user = ForeignKeyField(User, related_name='user')
    match = ForeignKeyField(Match, related_name='match')
    bet = ForeignKeyField(Team, related_name='betonteam')

    class Meta:
        database = db

class Result(MySQLModel):

    match = ForeignKeyField(Match, related_name='formatch')
    winner = ForeignKeyField(Team, related_name='winnerteam')

    class Meta:
        database = db


class CreateData():

    def create_teams(self):
        with open('/Users/second/PycharmProjects/flask/app/static/data/teams.csv') as f:
            for line in f.readlines():
                t = Team.create(name=line.rstrip('\n'), flag="")
                t.save()
        print("Saved")
        for lin in Team.select():
            print(lin.name)

    def create_fixtures(self):
        with open('/Users/second/PycharmProjects/flask/app/static/data/wc1.csv') as f:
            for line in f.readlines():
                vars =  line.split(',')
                t1 = Team.select().where(Team.name==vars[2]).get()
                t2 = Team.select().where(Team.name==vars[3].rstrip('\n')).get()
                mday= int(vars[0].replace('-Jun',''))
                mtimestr = vars[1].split(":")
                #print(time(int(mtimestr[0]),int(mtimestr[1])))
                Match.create(team1=t1, team2=t2, mdate=date(2014,6,mday), mtime=time(int(mtimestr[0]),int(mtimestr[1])))

    def disp_teams(self):
        for lin in Team.select():
            print(lin.name)

    def disp_matches(self):
        for lin in Match.select():
            print(lin.team1.name+" vs "+lin.team2.name+" on "+str(lin.mdate)+" @ "+str(lin.mtime))

    def display_data(self):
        t1 = Team.select()
        for t in t1:
            print(t.name)

    def create_tables(self):
        #Team.create_table()
        User.create_table()
        #Match.create_table()
        Points.create_table()
        Bet.create_table()
        Result.create_table()

    def drop_tables(self):
        #Team.drop_table()
        User.drop_table()
        #Match.drop_table()
        Points.drop_table()
        Bet.drop_table()
        Result.drop_table()

    def disp_bets(self):
        for bet in Bet.select():
            print(bet.user.name+" "+bet.bet.name+" "+str(bet.match.id))

    def disp_results(self):
        for r in Result.select():
            print(r.match.team1.name,r.match.team2.name,r.winner.name)

    def disp_points(self):
        for p in Points.select():
            print(p.user.name,p.value,p.match.team1.name,p.match.team2.name)


class PointsManager():

    def updatePoints(self,m,w):

        # delete existin points
        if Points.select().where(Points.match == m).exists():

            Points.delete().where(Points.match == m).execute()
        logger.info("Points count for Match:"+str(m.team1.name)+"-"+str(Points.select(Points.match ==m).count()))
        # create new points for all users
        #usr = User.select()
        logger.error(User.select().count())
        if Bet.select().where(Bet.match == m).exists():
            for bt in Bet.select().where(Bet.match == m):
                logger.error("User:::"+str(bt.user.name))
                if w.id == bt.bet.id:
                    logger.error("+2")
                    Points.create(user=bt.user,match=m,value=2,datecreated=date.today())
                else:
                    Points.create(user=bt.user,match=m,value=-2,datecreated=date.today())
                    logger.error("-2")
#crd = CreateDataTest()
#crd.create_tables()
#crd.create_teams()
#crd.create_fixtures()
#crd.disp_bets()





