from flask import Blueprint, request, render_template, redirect, url_for, make_response, session

from werkzeug.security import generate_password_hash,check_password_hash
from back.models import db, User, ArticleType,Article
from utils.functions import is_login

back_blueprint = Blueprint('back',__name__)

@back_blueprint.route('/create_db/',methods=['GET'])
def create_db():
    db.create_all()
    return '创建表成功'

#文章分类
@back_blueprint.route('/category/',methods=['GET','POST'])
@is_login
def category():
    if request.method == 'GET':
        # types = ArticleType.query.order_by(ArticleType.id).all()
        types = ArticleType.query.all()
        return render_template('back/category.html',types=types)
    if request.method == 'POST':
        return redirect(url_for('back.add_type'))


#修改分类
@back_blueprint.route('/update_category/<int:id>',methods=['GET','POST'])
@is_login
def update_category(id):
    if request.method == 'GET':
        categorys=ArticleType.query.get(id)
        return render_template('back/update-category.html',categorys=categorys)
    if request.method == 'POST':
        ArticleType.id = request.view_args.get('id')
        type = ArticleType()
        if  type.id == request.view_args.get('id'):
            del_article_type(type.id)
        type.id=id
        type.t_name=request.values.get('t_name')
        db.session.add(type)
        db.session.commit()
        return redirect(url_for('back.category'))


#添加后的文章分类
@back_blueprint.route('/a_type/',methods=['GET','POST'])
def a_type():
    if request.method == 'GET':
        types=ArticleType.query.all()
        return render_template('back/category.html',types=types)


#添加文章分类
@back_blueprint.route('/add_type/',methods=["POST","GET"])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')

    if request.method == 'POST':
        atype=request.form.get('atype')
        if atype:
            art_type =ArticleType()
            art_type.t_name=atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.category'))
        else:
            error ='请填写分类信息'
            return render_template('back/category_add.html',error=error)


#删除文章
@back_blueprint.route('/del_article_type/<int:id>/',methods=['GET'])
def del_article_type(id):
    delart = ArticleType.query.get(id)
    db.session.delete(delart)
    db.session.commit()
    return redirect(url_for('back.category'))


#首页
@back_blueprint.route('/index/', methods=['GET'])
@is_login
def index():

    username=session.get('username')
    return render_template('back/index.html',username=username)

#退出登录
@back_blueprint.route('/logout/',methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))




#注册
@back_blueprint.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已注册，请更换账号'
                return render_template('back/register.html', error=error)
            else:
                if password2 == password:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('back.login'))
                else:
                    error ='两次密码不一致'
                    return render_template('back/register.html',error=error)
        else:
                error = '请填写完整的信息'
                return render_template('back/register.html',error=error)


#登录
@back_blueprint.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请去注册'
                return render_template('back/login.html',error=error)
            if not check_password_hash(user.password,password):
                error = '密码错误'
                return render_template('back/login.html',error=error)
            session['user_id'] = user.id
            return redirect(url_for('back.index'))
        else:
            error = '请填写完整的登录信息'
            return render_template('back/login.html', error=error)


#文章
@back_blueprint.route('/article/',methods=['GET','POST'])
@is_login
def article():
    if request.method == 'GET':
        articles =Article.query.all()
        return render_template('back/article.html',articles=articles)

# request.form_data_parser_class.parse_functions.__len__()
#添加文章
@back_blueprint.route('/add_article/',methods=['GET','POST'])
@is_login
def add_article():
    if request.method == 'GET':
       types = ArticleType.query.order_by(ArticleType.id).all()
       return render_template('back/add-article.html',types=types)
    if request.method == 'POST':
        title=request.form.get('title')
        desc=request.form.get('describe')
        content=request.form.get('content')
        type=request.form.get('category')
        art =Article()
        art.title=title
        art.desc=desc
        art.content=content
        art.type=type
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('back.article'))


#修改文章
@back_blueprint.route('/update_article/<int:id>/',methods=['GET','POST'])
@is_login
def update_article(id):
    if request.method == 'GET':
        articles=Article.query.get(id)
        types = ArticleType.query.order_by(ArticleType.id).all()
        return render_template('back/update-article.html',articles=articles,types=types)
    if request.method == 'POST':

        Article.id = request.view_args.get('id')
        art = Article()
        if art.id==request.view_args.get('id'):
            del_article(id)
        art.id=id
        art.title = request.form['title']
        art.desc = request.form.get('describe')
        art.content = request.form.get('content')
        art.type = request.form.get('category')
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('back.article'))


#删除文章
@back_blueprint.route('/del_article/<int:id>/',methods=['GET'])
def del_article(id):
    delart = Article.query.get(id)
    db.session.delete(delart)
    db.session.commit()
    return redirect(url_for('back.article'))



#用户管理
@back_blueprint.route('/manage-user/',methods=['GET'])
@is_login
def manage_user():
    return render_template('back/manage-user.html')


#登录管理
@back_blueprint.route('/loginlog/',methods=['GET'])
@is_login
def loginlog():
    return render_template('back/loginlog.html')

