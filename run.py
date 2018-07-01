#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for, session,g,flash
import config
from exts import db
from functools import wraps
from form import CreateForm
from database import User,BlogPost,Comment
from flask_mail import Mail,Message

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_object(config_filename)
#
#     @app.after_request
#     def after_request(response):
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         if request.method == 'OPTIONS':
#             response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
#             headers = request.headers.get('Access-Control-Request-Headers')
#             if headers:
#                 response.headers['Access-Control-Allow-Headers'] = headers
#         return response
#
#     from exts import db
#     db.init_app(app)
#
#     from api import init_api
#     init_api(app)
#
#     return app

# db.create_all()

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mail=Mail(app)

def log_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('id'):
            return func(*args,**kwargs)
        else:
            flash('非用户操作, 请登录后浏览', 'danger')
            return redirect(url_for('login'))
    return wrapper


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        str = request.form.get('searchstr')
        content = BlogPost.query.filter(BlogPost.title.contains(str)| BlogPost.content.contains(str))
        if content.first()!= None:
            context = {'blogs':content.all()}
            return render_template('search.html', **context)
        else:
            return u'sorry'

@app.route('/content/<int:id>',methods=['GET','POST'])
@log_required
def content(id):
    post = BlogPost.query.get(id)
    return render_template('content.html',blog = post)

@app.route('/reedit/<int:id>',methods=['GET','POST'])
@log_required
def reedit(id):
    if request.method == 'GET':
        post = BlogPost.query.get(id)
        return render_template('reedit.html', blog=post)
    else:
        post = BlogPost.query.filter(BlogPost.id == id).first()
        title = request.form.get('title')
        content = request.form.get('content')
        post.title = title
        post.content = content
        db.session.merge(post)
        db.session.commit()
        return render_template('content.html')


# @app.route('/voteup/',methods=['POST'])
# @log_required
# def voteup():
#     blog_id = request.form.get('blog_id')
#     vote = Vote(blog_id = blog_id,voteup = voteup + 1)
#     vote.voter = g.user
#     vote.blog = BlogPost.query.get(blog_id)
#     db.session.add(vote)
#     db.session.commit()
#
#
# @app.route('/votedown/',methods=['POST'])
# @log_required
# def votedown():
#     blog_id = request.form.get('blog_id')
#     vote = Vote(blog_id=blog_id, voteup = votedown + 1)
#     vote.voter = g.user
#     vote.blog = BlogPost.query.get(blog_id)
#     db.session.add(vote)
#     db.session.commit()

@app.route('/delete/',methods=['GET','POST'])
@log_required
def delete():
    blog_id = request.form.get('delete_id')
    print(blog_id)
    _blog = BlogPost.query.filter(BlogPost.id == blog_id).first()
    db.session.delete(_blog)
    db.session.commit()

    return redirect(url_for('blog'))

@app.route('/comment/',methods=['POST'])
@log_required
def comment():
    blog_id = request.form.get('blog_id')
    content = request.form.get('comment')
    comm = Comment(content=content)
    comm.audience =g.user
    comm.blog = BlogPost.query.get(blog_id)
    db.session.add(comm)
    db.session.commit()

    to_someone = User.query.filter(User.id == comm.blog.author_id).first()
    re_to = to_someone.email
    re_title = 'Message from {} to you'.format(g.user.email)
    re_content = comm.content
    msg = Message(re_title,sender='myblogserver@163.com',recipients=[re_to])
    msg.body = re_content
    mail.send(msg)
    flash('邮件发送成功!', 'success')
    return redirect(url_for('content',id=blog_id))

# @app.route('/create/',methods=['GET','POST'])
# def create():
#     if request.method == 'GET':
#         return render_template('create.html')
#     else:
#         email = request.form.get('email')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         check_password = request.form.get('check_password')
#
#         user = User.query.filter(User.username == username).first()
#         if user:
#             return u'不好意思,该账号已被注册，请更换您的账号'
#         else:
#             if password != check_password:
#                 return u'两次密码不匹配，请重新设置'
#             else:
#                 editor = User(username=username,email= email,password=password)
#                 db.session.add(editor)
#                 db.session.commit()
#                 return redirect(url_for('login'))

@app.route('/create/',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        form = CreateForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            check_password = form.check_password.data
            check_user = User.query. filter(User.username == username and User.email == email).first()
            if check_user:
                flash('不好意思,该账号或邮箱已被注册，请更换您的账号', 'danger')
                return redirect(url_for('create'))
                # return u'不好意思,该账号或邮箱已被注册，请更换您的账号'
            else:
                if password != check_password:
                    flash('两次密码不匹配，请重新设置', 'danger')
                    return redirect(url_for('create'))
                    # return u'两次密码不匹配，请重新设置'
                else:
                    user = User(email=email,username=username,password=password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('login'))
        else:
            flash('注册条件不符合要求，请重新退回注册界面', 'danger')
            return redirect(url_for('create'))
            # return u'注册条件不符合要求，请重新退回注册界面'

@app.route('/problem_login/')
def problem_login():
    return render_template('problem_login.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        status = request.form.get('status')
        user = User.query.filter(User.username==username,User.password==password).first()
        if user :
            session['id'] = user.id
            if status:
                session.permanent = True
                g.user = user
            return redirect(url_for('index'))
        else:
            flash('您的用户名或密码错误，请重新输入', 'danger')
            return redirect(url_for('create'))
            # return u'您的用户名或密码错误，请重新输入'

@app.route('/info/',methods=['GET','POST'])
@log_required
def info():
    return render_template('info.html')

@app.route('/blog/',methods=['GET','POST'])
@log_required
def blog():
    context ={'blogs':BlogPost.query.order_by('-date_posted').all()}
    return render_template('blog.html',**context)

@app.route('/edit/',methods=['GET','POST'])
@log_required
def edit():
    if request.method == 'GET':
        return render_template('edit.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        _blog = BlogPost(title = title,content = content)
        _blog.author = g.user
        db.session.add(_blog)
        db.session.commit()
        return redirect(url_for('blog'))

@app.route('/logout/',methods=['GET'])
@log_required
def logout():
    session.clear()
    flash('你已成功注销账号', 'success')
    return redirect(url_for('login'))

@app.before_request
def before_request():
    id = session.get('id')
    if id:
        user = User.query.get(id)
        g.user = user

@app.context_processor
def context_processor():
    if hasattr(g,'user'):
        return {"user":g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run(debug=True)
