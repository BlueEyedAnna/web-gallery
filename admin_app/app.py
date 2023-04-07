import base64
import datetime
import random

from bson.objectid import ObjectId
from flask_restful import Resource
from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from admin_app import app, db, api


# класс пользователя
class User(UserMixin):
    def __init__(self, user):
        # распаковываем поля для удобства
        self.id = user['_id']
        self.login = user['login']
        self.password = user['password']

    # метод получени id (нужен для работы фласка)
    def get_id(self):
        return self.id


# для авторизации
login_manager = LoginManager(app)
# коллекция пользователей (для упрощения обращения)
admins = db['administrators']


@app.route('/exhibCreation', methods=['GET'])
def exhibCreation():
    pass


@app.route("/excursCreation")
def excursCreation():
    pass


# <editor-fold desc="Auth">
# это авторизация пользователя
@login_manager.user_loader
def load_user(user_id):
    user = admins.find_one({'_id': user_id})
    if user:
        return User(user)
    return None


# отображение главной страницы
@app.route("/")
@app.route("/index")
def index():
    # проверка авторизован ли пользователь
    if current_user.is_authenticated:
        return render_template(
            "index.html",
            is_authenticated=True,  # передаем в отображение html что пользователь не авторизован
            ver=datetime.datetime.now().timestamp()
        )
    else:
        return render_template(
            "index.html",
            is_authenticated=False,  # передаем в отображение html что пользователь авторизован
            ver=datetime.datetime.now().timestamp()
        )


# авторизация пользователя
@app.route("/login", methods=["POST"])
def login():
    # кнопка "запомнить меня"
    rm = True if request.form.get("remainMe") else False

    # находим пользователя в базе по логину, который пытается авторизоваться
    user = User(admins.find_one({'login': request.form.get('userLogin')}))

    # авторизуем его
    login_user(user, remember=rm)

    # перенаправляем на страницу
    return redirect(url_for("index"))  # !!!!!!Изменить


# выход из системы
@app.route("/logout", methods=["POST"])
def logout():
    # выкидываем пользователя из системы
    logout_user()

    # перенаправляем на главную страницу
    return redirect(url_for("index"))


# </editor-fold>

# <editor-fold desc="API">
# API для проверки совпадения пароля и логина при авторизации
class LoginUser(Resource):
    def get(self, login, password):
        user = admins.find_one({"login": login})
        if user:
            if user["password"] == password:
                return True, 200
        return False, 200


# API для проверки существования конкретного логина (чтобы не повторялись)
class CheckLogin(Resource):
    def get(self, login=''):
        if login == '':
            return True, 200
        if not admins.find_one({'login': login}):
            return False, 200
        return True, 200


# регистрация API
api.add_resource(LoginUser, "/login_user/<string:login>&<string:password>")
api.add_resource(CheckLogin, "/check_login/<string:login>", "/check_login/")
# </editor-fold>

# запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
