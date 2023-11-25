from flask import Flask
from flask import request
from flask import render_template
import sqlite3

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/signup",methods=["GET","POST"])
def signup():
    name=request.form.get("name")
    phonenumber=request.form.get("phonenumber")
    username=request.form.get("username")
    password=request.form.get("password")
    conn=sqlite3.Connection("RevRes.db")
    conn.execute("insert into users values(?,?,?,?)",(name,phonenumber,username,password))
    conn.commit()
    return render_template("homepage.html",user=username,pass1=password)
@app.route("/signup1",methods=["GET","POST"])
def signup1():
    return render_template("signup.html")
@app.route("/login1",methods=['GET','POST'])
def login1():
    return render_template("login.html")
@app.route('/login',methods=['GET','POST'])
def login():
    o=request.form.get('username')
    p=request.form.get('password')
    conn=sqlite3.connect('RevRes.db')
    d=list(conn.execute('select * from users'))
    c=0
    for i in d:
        if i[2]==o and i[3]==p:
            c+=1
            break
    if c==0:
        return "Invalid username/password"
    else:
        return render_template('homepage.html',user=o,pass1=p)
@app.route('/postresume',methods=['GET','POST'])
def postresume():
    d=request.form.get('submit').split()
    o=d[2]
    conn=sqlite3.connect('RevRes.db')
    e=list(conn.execute('select * from Resume'))
    c=0
    q=''
    r=''
    for i in range(len(e)):
        if(e[i][0]==o):
            c+=1
            q=e[i][1]
            r=e[i][2]
            break
    if c==0:
        return render_template("postresume.html",user=o)
    else:
        return render_template("postresume1.html",user=o,link=q,response=r)
@app.route('/update_resume',methods=['GET','POST'])
def update_resume():
    a=request.form.get('url')
    b=request.form.get('submit').split()
    c1=b[2]
    print(c1)
    conn=sqlite3.connect('RevRes.db')
    e=list(conn.execute('select * from Resume'))
    c=0
    q=''
    r=''
    for i in range(len(e)):
        if(e[i][0]==c1):
            c+=1
            q=e[i][1]
            r=e[i][2]
            break
    if c==0:
        conn.execute('insert into Resume values(?,?,?)',(c1,a,"No Response Yet"))
        conn.commit()
    else:
        conn.execute("update Resume set resume='"+a+"' where username='"+c1+"'")
        print(a,c1)
        conn.commit()
    print(a)
    return render_template('postresume1.html',user=c1,link=a,response=r)
@app.route('/admin',methods=["GET","POST"])
def admin():
    return render_template("admin_login.html")
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    o=request.form.get("username")
    p=request.form.get("password")
    if(o=="Saurabh@123" and p=="HelloSaurabh") or (o=="Jayanth@123" and p=="HelloJayanth"):
        conn=sqlite3.connect("RevRes.db")
        e=list(conn.execute("select * from Resume"))
        for i in range(len(e)):
            e[i]=list(e[i])
        print(e)
        return render_template("admin_homepage.html",username=o,password=p,Resume=e)
    else:
        return "invalid_credentials"
@app.route("/write_review",methods=["GET","POST"])
def write_review():
    conn=sqlite3.connect("RevRes.db")
    p=request.form.get("review")
    q=request.form.get("submit").split()
    r=q[1]
    conn.execute("update Resume set response='"+p+"' where username='"+r+"'")
    conn.commit()
    return 'Response updated sucessfully!'
@app.route("/blog_section",methods=["GET","POST"])
def blogs():
    conn=sqlite3.connect('RevRes.db')
    q=list(conn.execute('select * from blogs'))
    r=[]
    for i in q:
        r.append(i[1])
    return render_template('blogs.html',blogs=r)
@app.route("/add_blog",methods=["GET","POST"])
def add_blog():
    r=request.form.get("content")
    print(r)
    conn=sqlite3.connect("RevRes.db")
    o=0
    p=list(conn.execute("select * from blogs"));
    q=len(p)
    conn.execute("insert into blogs values(?,?)",(q,r))
    conn.commit()
    return "blog added sucessfully!"
@app.route("/meetings",methods=['GET','POST'])
def meeting():
    conn=sqlite3.connect("RevRes.db")
    p=list(conn.execute("select * from meetings"))
    q=[]
    for i in p:
        # print(i)
        q.append(i[0]) 
    return render_template("meetings.html",meetings=q)
@app.route("/add_link",methods=["GET","POST"])
def add_meeting():
    o=request.form.get("url")
    conn=sqlite3.connect("RevRes.db")
    conn.execute("insert into meetings values('"+o+"')")
    conn.commit()
    return "Added Sucessfully!"
@app.route('/fetch_blogs', methods=["GET","POST"])
def fetchblogs():
    conn=sqlite3.connect('revres.db')
    q=list(conn.execute('select * from blogs'))
    r=[]
    for i in q:
        r.append(i[1])
    return render_template('view_blogs.html',blogs=r)
@app.route('/check_meetings',methods=['GET','POST'])
def checkmeetings():
    conn=sqlite3.connect('revres.db')
    p=list(conn.execute("select * from meetings"))
    q=[]
    for i in p:
        # print(i)
        q.append(i[0]) 
    return render_template("view_meetings.html",meetings=q)