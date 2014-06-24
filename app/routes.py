from flask import Flask, render_template, request, redirect, url_for
from utils.test import Tst
from flask.ext import login
from utils.models import *
from flask.ext.security import login_required
import json
from datetime import *
import logging
import os
from werkzeug.utils import secure_filename

logger = logging.getLogger('SuperBets')
hdlr = logging.FileHandler('/var/tmp/SuperBets.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)
 
app = Flask(__name__)


UPLOAD_FOLDER = './static/data/pics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/fileupload/<uid>', methods=['GET', 'POST'])
def upload_file(uid):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            usr = User.select().where(User.id == uid).get()
            usr.image = file.filename
            usr.save()
            return "success"
    return "failure"




def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Creating user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.select().where(User.id==user_id).get()



init_login()



@app.route('/')
def home():
    if login.current_user.is_authenticated():
        return login.redirect('/app')
    else:
        return render_template('login.html')



@app.route('/app')
@login_required
def appm():
    return render_template('app.html')


@app.route('/leaders')
@login_required
def leaders():
    return render_template('leaders.html')


@app.route('/results')
@login_required
def results():
    return render_template('results.html')


@app.route('/profile/<uid>')
@login_required
def profile(uid):
    #uid = login.current_user.id
    return render_template('profile.html',uid=uid)



@app.route("/loginu/<uid>/<pwd>", methods=["GET", "POST"])
def loginu(uid, pwd):
    if User.select().where(User.uname==uid, User.password==pwd).exists():
        login.login_user(User.select().where(User.uname==uid).get())
        return "success"
    return "Wrong userid/password. Please ask Aravind."




@app.route("/logout")
@login_required
def logout():
    login.logout_user()
    return render_template('login.html')



@app.route("/matches")
def matches():
    dict={}
    mnum=1
    for mtch in Match.select().order_by(Match.mdate, Match.mtime):
        t1=mtch.team1
        t2=mtch.team2
        d=mtch.mdate
        t=mtch.mtime
        usr = User.select().where(User.id == login.current_user.id).get()

        today = date.today()
        gstart = date(2014,6,17)
        now = time(datetime.now().hour,datetime.now().minute)
        gamestart = 0
        past = 0

        if mtch.mdate < today:
            gamestart = "past"
        elif mtch.mdate == today:
            gamestart = "now"
        else:
            gamestart ="future"



        if mtch.mdate < today:
            past = 1
        elif mtch.mdate > today:
            past = 0
        else:
            if time(int(str(mtch.mtime).split(":")[0]),int(str(mtch.mtime).split(":")[1])) > now:
                past = 0
            else:
                past = 1

        t1bets = []
        t2bets = []
        if Bet.select().where(Bet.match == mtch).exists():
            for b in Bet.select().where(Bet.match == mtch):
                if b.bet == mtch.team1:
                    t1bets.append({"name":b.user.name,"id":b.user.id})
                else:
                    t2bets.append({"name":b.user.name,"id":b.user.id})



        winnerid=0

        if Result.select().where(Result.match == mtch).exists():
            res = Result.select().where(Result.match == mtch).get()
            winnerid = res.winner.id


        mdict={"mid":mtch.id,"winnerid":winnerid,"t1":{"nob":len(t1bets),"bets":t1bets,"name":t1.name,"id":t1.id},"t2":{"nob":len(t2bets),"bets":t2bets,"name":t2.name,"id":t2.id},"date":str(d),"time":str(t),"past":past,"gamestart":gamestart}

        if Bet.select().where(Bet.user == usr, Bet.match == mtch).exists():
            bt = Bet.select().where(Bet.user == usr, Bet.match == mtch).get()
            mdict["beton"] = bt.bet.id

        dict[mnum] = mdict
        mnum = mnum+1

    return json.dumps(dict)


@app.route("/adminmatches")
def adminmatches():
    dict={}
    mnum=1
    for mtch in Match.select().order_by(Match.mdate, Match.mtime):
        t1=mtch.team1
        t2=mtch.team2
        d=mtch.mdate
        t=mtch.mtime
        usr = User.select().where(User.id == login.current_user.id).get()

        today = date.today()
        gstart = date(2014,6,17)
        now = time(datetime.now().hour,datetime.now().minute)
        gamestart = 0
        past = 0

        if mtch.mdate < today:
            gamestart = "past"
        elif mtch.mdate == today:
            gamestart = "now"
        else:
            gamestart ="future"



        if mtch.mdate < today:
            past = 0
        elif mtch.mdate > today:
            past = 0
        else:
            if time(int(str(mtch.mtime).split(":")[0]),int(str(mtch.mtime).split(":")[1])) > now:
                past = 0
            else:
                past = 0


        mdict={"mid":mtch.id,"t1":{"name":t1.name,"id":t1.id},"t2":{"name":t2.name,"id":t2.id},"date":str(d),"time":str(t),"past":past,"gamestart":gamestart}

        if Result.select().where(Result.match==mtch).exists():
            res = Result.select().where(Result.match==mtch).get()
            wnr = res.winner
            mdict["winner"]={"name":wnr.name, "id":wnr.id}

        dict[mnum] = mdict
        mnum = mnum+1

    return json.dumps(dict)


@app.route("/setWinner/<mid>/<tid>")
def setWinner(mid, tid):
    mtch = Match.select().where(Match.id==mid).get()
    tm   = Team.select().where(Team.id == tid).get()
    if Result.select().where(Result.match==mtch).exists():
        res = Result.select().where(Result.match==mtch).get()
        res.delete_instance()

    Result.create(match=mtch, winner=tm)

    pm = PointsManager()
    pm.updatePoints(mtch,tm)

    return tid




@app.route("/getleaderboard/")
def getleaderboard():

    ldict = {}
    ptb = []
    for u in User.select():
        upoints = 0
        if Points.select().where(Points.user==u).exists():
            for p in Points.select().where(Points.user==u):
                upoints = upoints+int(p.value)

        if upoints not in ptb:
            ptb.append(upoints)

        ldict[u.uname]={"name":u.name, "uid":u.id, "upoints":upoints, "image":u.image}

    ptb.sort(reverse=True)
    invranks = {}
    for i in range(0,len(ptb)):
        invranks[i]=ptb[i]

    ranks = {v:k for k,v in invranks.items()}

    for k,v in ldict.items():
        print(upoints)
        v["rank"] = ranks[v["upoints"]]


    return json.dumps(ldict)



@app.route("/register/<name>/<uname>/<pwd>")
def register(name,uname,pwd):
    if User.select().where(User.uname==uname).exists():
        return "User Id already exists"
    User.create(name=name,uname=uname, password=pwd)
    if User.select().where(User.uname==uname).exists():
        return "Successfully registered. Sign in and start betting!"
    else:
        return "Something went wrong. Please contact Aravind!"


@app.route("/showMatch/<mid>")
@login_required
def showMatch(mid):
    match = Match.select().where(Match.id==mid).get()
    #match = mid
    return render_template('match.html',match=match)

@app.route("/showUser/<uid>")
@login_required
def showUser(uid):
    user = User.select().where(User.id==uid).get()
    #match = mid
    return render_template('user.html',uid=uid)



@app.route("/admin/<pstr>")
def adminV(pstr):
    if pstr == "160387":
        return render_template("admin.html")
    else:
        return "Unauthorized"



@app.route("/beton/<mid>/<tname>")
def beton(mid,tname):
    mtch = Match.select().where(Match.id==mid).get()
    tm   = Team.select().where(Team.name == tname).get()
    usr = User.select().where(User.id == login.current_user.id).get()

    today = date.today()
    now = time(datetime.now().hour,datetime.now().minute)

    if mtch.mdate < today:
        past = 1
    elif mtch.mdate > today:
        past = 0
    else:
        if time(int(str(mtch.mtime).split(":")[0]),int(str(mtch.mtime).split(":")[1])) > now:
            past = 0
        else:
            past = 1

    if past == 1:
        return "fail"

    try:
        bete = Bet.select().where(Bet.user==usr,Bet.match==mtch).get()
        bete.delete_instance()
        beton = Bet.create(user=usr,match=mtch,bet=tm)
        return "suc"
    except:
        beton = Bet.create(user=usr,match=mtch,bet=tm)
        return "suc"

@app.route("/getMatchDetails/<mid>")
def getMatchDetails(mid):
    mtch = Match.select().where(Match.id == mid).get()
    mdict = {}
    tm1 = mtch.team1
    tm2 = mtch.team2
    t1b=[]
    t2b=[]

    if Bet.select().where(Bet.match == mtch).exists():
        for bt in Bet.select().where(Bet.match == mtch):
            if bt.bet.name == tm1.name:
                #return bt.user.name
                t1b.append(bt.user.name)
            else:
                t2b.append(bt.user.name)

    mdict[1]={"team":{"id":tm1.id,"name":tm1.name},"bets":t1b}
    mdict[2]={"team":{"id":tm2.id,"name":tm2.name},"bets":t2b}

    return json.dumps(mdict)


@app.route("/getUserMatchDetails/<uid>")
def getUserMatchDetails(uid):
    udict={}
    usr=None
    if User.select().where(User.id == uid).exists():
        usr=User.select().where(User.id == uid).get()

        udict["bets"]=[]
    tpoints=0
    nbets =0
    if Bet.select().where(Bet.user == usr).exists():
        for bt in Bet.select().where(Bet.user == usr):
            nbets = nbets+1
            winner =""
            if Result.select().where(Result.match == bt.match).exists():
                res = Result.select().where(Result.match == bt.match).get()
                winner = res.winner.name
            pnts = 0
            if Points.select().where(Points.user==usr,Points.match==bt.match).exists():
                pobj=Points.select().where(Points.user==usr,Points.match==bt.match).get()
                pnts=pobj.value
                tpoints = tpoints +pnts
            if pnts!=0:
                udict["bets"].append({"t1":bt.match.team1.name,"t2":bt.match.team2.name,"winner":winner,"upoints":pnts,"beton":bt.bet.name})
    udict["user"]={"name":usr.name,"tpoints":tpoints,"nbets":nbets}



    return json.dumps(udict)


@app.route("/getUserDetails/<uid>")
def getUserDetails(uid):
    udict={}
    usr=None
    if User.select().where(User.id == uid).exists():
        usr=User.select().where(User.id == uid).get()


    udict["user"]={"name":usr.name,"image":usr.image, "uid":usr.id, "cuserid":login.current_user.id}

    return json.dumps(udict)


@app.route("/match/<mid>")
def match(mid):
    return render_template("match.html",mid=mid)




# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
  app.run(debug=True,host="0.0.0.0")
