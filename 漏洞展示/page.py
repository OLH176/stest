from flask import Flask,session,send_from_directory,request
from flask import render_template
from exts import db
from model import User,Message,Ad,Userlog,Adminlog,Adminoplog,Useroplog
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from forms import Register,Login,Upload,Download,Leave,DelUser,DelMessage,Restore,Xss
from shutil import copyfile
import os

app=Flask(__name__)

app = Flask(__name__)
admin = Admin(app=app, name='多用户留言板管理系统')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:oulianghao@127.0.0.1:3306/db"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['JSON_AS_ASCII'] = False
app.config["SECRET_KEY"]='3a25ec04ef194e7cbe20fcc1a3cd75ac'
app.config['UPLOAD_PATH']=os.path.join(app.root_path,'static')
db = SQLAlchemy(app)
db.init_app(app)

@app.route('/',methods=["GET"])
def show():
    return render_template('labels.html')

@app.route('/xss',methods=["GET","POST"])
def xss():
    form=Xss()
    input=""
    if form.validate_on_submit():
        input=form.data["input"]
    return render_template('xss.html',input=input,form=form)

@app.route('/xss_',methods=["GET","POST"])
def xss_():
    form=Xss()
    input=""
    if form.validate_on_submit():
        input=form.data["input"]
    return render_template('xss.html',input=input,form=form)

@app.route('/init',methods=["GET","POST"])
def init():
    #print(User.query.filter_by(username="olh").count())
    #print("2")
    #print(app.config['UPLOAD_PATH'])
    form=Login()
    info=""
    #print("#")
    if form.validate_on_submit():
        #print("234243")
        data=form.data
        user=User.query.filter_by(username=data["username"]).first()
        if not user:
            info="用户名不存在！"
        else:
            if user.password!=data["password"]:
                info="用户名或密码错误！"
            else:
                session["username"]=user.username
                #info="Yytfyhjn"
                db.session.add(Userlog(username=data["username"],ip=request.remote_addr))
                msgs=Message.query.all()
                return render_template('login.html',session=session,form=Upload(),forma=Download(),info=info,formb=Leave(),msgs=msgs)
    return render_template('init.html',info=info,form=form)

def isValid(s):
    for c in s:
        if c=='/' or c=='\\' or c=='|' or c=='"' or c=='<' or c=='>' or c=='*' or c==':':
            return False
    return  True

@app.route('/register/',methods=["GET","POST"])
def register():
#    print(2)

    form=Register()
    err=""
#    print(1)
#    print(form.errors)
    if form.validate_on_submit():
#        print(3)
        data=form.data
        user=User(username=data["username"],password=data["password"],name=data["name"],idnum=data["idnum"])
        # if len(data["idnum"]!=18):
        #     err="身份证号长度为16位！"
        if not isValid(data["username"]):
            err='用户名不能含有“<>/\:"*|”！'
        else:
            if User.query.filter_by(username=user.username).count()>=1:
                err="用户名已存在！"
            # print(User.username)
            # print(User.query.filter_by(username=User.username).count())
            else:
#        print(data)
                db.session.add(user)
                db.session.commit()
                copyfile(".\\static\\1234567890123456.jpg",".\\static\\"+user.username+".jpg")
                return render_template('init.html',info="注册成功！",form=Login())
    if len(form.errors)>0:
        err = "身份证号长度为18位！"
    return render_template('register.html',form=form,err=err)

def userop(s):
    db.session.add(Useroplog(username=session["username"],op=s,ip=request.remote_addr))
    db.session.commit()

def adminop(s):
    db.session.add(Adminoplog(username=session["username"], op=s, ip=request.remote_addr))
    db.session.commit()

@app.route('/upload',methods=["POST"])
def upload():
    try:
        session["username"]
    except:
        return render_template('init.html',info="请先登录！",form=Login())
    form=Upload()
   # print(1)
    info="上传失败！"
    if form.validate_on_submit():
     #   print(2)
        image=form.image.data
        image.save(os.path.join(app.config['UPLOAD_PATH'],session["username"]+".jpg"))
        info="上传成功！"
        userop("上传头像")
    msgs = Message.query.all()
    return render_template('login.html',session=session,form=Upload(),forma=Download(),info=info,formb=Leave(),msgs=msgs)

@app.route('/download',methods=["POST"])
def download():
    try:
        session["username"]
    except:
        return render_template('init.html',info="请先登录！",form=Login())
    form=Download()
    info="下载失败！"
    try:
        if form.validate_on_submit():
        #print(form.data)
            userop("下载头像："+form.data["username"])
            return send_from_directory(app.config['UPLOAD_PATH'],filename=form.data["username"]+".jpg",as_attachment="True")
    except:
        info = "无该用户！"
    msgs = Message.query.all()
    return render_template('login.html', session=session, form=Upload(), forma=Download(), info=info, formb=Leave(),
                               msgs=msgs)

@app.route('/message',methods=["POST"])
def message():
    try:
        session["username"]
    except:
        return render_template('init.html',info="请先登录！",form=Login())
    form=Leave()
    info="留言失败！"
    if form.validate_on_submit():
        #print(1)
        #print(form.data)
        data=form.data
        #print(data["message"])
        msg=Message(username=session["username"],message=data["message"])
        #print(msg.id)
        db.session.add(msg)
        db.session.commit()
        userop("留言")
        info="留言成功！"
    msgs = Message.query.all()
    return  render_template('login.html',session=session,form=Upload(),forma=Download(),info=info,formb=Leave(),msgs=msgs)

@app.route('/ad',methods=["GET","POST"])
def admin():
    form = Login()
    info = ""
    if form.validate_on_submit():
        data = form.data
        user = Ad.query.filter_by(username=data["username"]).first()
        if not user:
            info = "用户名不存在！"
        else:
            if user.password != data["password"]:
                info = "用户名或密码错误！"
            else:
                session["admin"] = user.username
                db.session.add(Adminlog(username=data["username"], ip=request.remote_addr))
                msgs = Message.query.all()
                users = User.query.all()
                return render_template('adlogin.html', session=session, form=DelUser(), forma=Restore(), info=info,
                                       formb=DelMessage(), msgs=msgs,users=users)
    return render_template('admin.html', info=info, form=form)

@app.route('/ad/deluser',methods=["POST"])
def deluser():
    try:
        session["admin"]
    except:
        return render_template('admin.html',info="请先登录！",form=Login())
    from model import db
    form=DelUser()
    info="删除失败!"
    if form.validate_on_submit():
        user=User.query.filter(User.username==form.data["username"]).all()
        if not user:
            info="无该用户！"
        else:
            #print(user.password)
            #for each in user:
            os.remove(".\\static\\" + form.data["username"] + ".jpg")
            db.session.delete(user[0])
            db.session.commit()
            #User.query.get(form.data["username"]).delete_obj()
            info="删除成功！"
            adminop("删除用户："+form.data["username"])
    msgs = Message.query.all()
    users = User.query.all()
    return render_template('adlogin.html', session=session, form=DelUser(), forma=Restore(), info=info,
                       formb=DelMessage(), msgs=msgs,users=users)

@app.route('/ad/restore',methods=["POST"])
def restore():
    try:
        session["admin"]
    except:
        return render_template('admin.html',info="请先登录！",form=Login())
    form=Restore()
    info="刷新失败！"
    if form.validate_on_submit():
        if User.query.filter_by(username=form.data["username"]).first():
            os.remove(".\\static\\" + form.data["username"] + ".jpg")
            copyfile(".\\static\\1234567890123456.jpg", ".\\static\\" + form.data["username"] + ".jpg")
            info="刷新成功！"
            adminop("还原头像："+form.data["username"])
        else:
            info="无该用户！"
    msgs = Message.query.all()
    users = User.query.all()
    return render_template('adlogin.html', session=session, form=DelUser(), forma=Restore(), info=info,
                       formb=DelMessage(), msgs=msgs,users=users)

@app.route('/ad/delmessage',methods=["POST"])
def delmessage():
    from model import db
    try:
        session["admin"]
    except:
        return render_template('admin.html',info="请先登录！",form=Login())
    form=DelMessage()
    info="删除留言失败！"
    if form.validate_on_submit():
        msg=Message.query.filter(Message.id==form.data["id"]).first()
        if msg:
            db.session.delete(msg)
            db.session.commit()
            info="删除留言成功！"
            adminop("删除"+str(form.data["id"])+"号留言")
        else:
            info="无该留言！"
    msgs = Message.query.all()
    users = User.query.all()
    return render_template('adlogin.html', session=session, form=DelUser(), forma=Restore(), info=info,
                           formb=DelMessage(), msgs=msgs,users=users)

if __name__=='__main__':
    app.run()