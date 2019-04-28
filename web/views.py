from flask import Blueprint, request, render_template, redirect, url_for,session
from werkzeug.security import check_password_hash

from back.models import Article, User
from utils.webfunctions import is_login

web_blueprint = Blueprint('web',__name__)


@web_blueprint.route('/exitlogin/',methods=['GET'])
@is_login
def exitlogin():
    return redirect(url_for('first.login'))


@web_blueprint.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('web/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请去注册'
                return render_template('web/login.html',error=error)
            if not check_password_hash(user.password,password):
                error = '密码错误'
                return render_template('web/login.html',error=error)
            session['user_id'] = user.id
            return redirect(url_for('web.web_index'))
        else:
            error = '请填写完整的登录信息'
            return render_template('web/login.html', error=error)


@web_blueprint.route('/index/',methods=['GET'])
@is_login
def web_index():
    if request.method == 'GET':
        articles = Article.query.limit(14).all()
        return render_template('web/index.html',articles=articles)


@web_blueprint.route('/info/<int:id>/',methods=['GET'])
@is_login
def web_info(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        return render_template('web/info.html',article=article)


@web_blueprint.route('/about/', methods=['GET'])
@is_login
def web_about():
    if request.method == 'GET':
        return render_template('web/about.html')


@web_blueprint.route('/list/', methods=['GET'])
@is_login
def list():
    if request.method == 'GET':
        articles = Article.query.limit(5).all()
        return render_template('web/list.html',articles=articles)