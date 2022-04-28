import base64
import datetime
import random

from flask_restful import Resource
from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, api


# класс пользователя со всеми его полями
class User(UserMixin):
    def __init__(self, user):
        # распаковываем поля дл я удобства
        self.id = user['_id']
        self.login = user['login']
        self.password = user['password']
        self.avatar = user['avatar']
        self.fio = user['fio']
        self.email = user['email']
        self.phone = user['phone']

    # метод получени id (нужен для работы фласка)
    def get_id(self):
        return self.id


# для генерации id
CHARS_FOR_ID = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# для авторизации
login_manager = LoginManager(app)

# коллекция пользователей (для уцпрощения обращения)
users = db['users']


@app.route("/exhibitions")
def exhibitions():
    return render_template("exhibitions.html",
                           ver=datetime.datetime.now().timestamp())


@app.route("/excursions")
def excursions():
    return render_template("excursions.html",
                           ver=datetime.datetime.now().timestamp())


# это авторизация пользователя
@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({'_id': user_id})

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
    user = User(users.find_one({'login': request.form.get('userLogin')}))

    # авторизуем его
    login_user(user, remember=rm)

    # перенаправляем на главную страницу
    return redirect(url_for("index"))


# выход из системы
@app.route("/logout", methods=["POST"])
def logout():
    # выкидываем пользователя из системы
    logout_user()

    # перенаправляем на главную страницу
    return redirect(url_for("index"))


# регистрация нового пользователя
@app.route("/signup", methods=["POST"])
def signup():
    # оборачиваем ошибки, что-то может пойти не так
    try:
        # цикл по поиску нового не существующего id в системе
        while True:
            # генерация нового id
            user_id = ''.join(random.choices(CHARS_FOR_ID, k=20))

            # проверка на существования такого id
            if users.find_one({"_id": user_id}):
                continue

            # сюда попали значит нашли новый не существующий id
            # добавление в базу нового пользователя
            users.insert_one({
                "_id": user_id,
                "login": request.form["userLogin"],
                "password": generate_password_hash(request.form["userPassword"]),
                "avatar": "",
                "email": "",
                "fio": "",
                "phone": ""
            })

            # сразу авторизация нового пользователя
            login_user(User(users.find_one({'_id': user_id})), remember=False)

            # выход из бесконечного цикла
            break
    finally:
        # если произошла ошибка или все хорошо в любом случае попадем сюда
        # переадресация на главную страницу
        return redirect(url_for("index"))


# API для проверки совпадения пароля и логина при авторизации
class LoginUser(Resource):
    def get(self, login, password):
        user = users.find_one({"login": login})
        if user:
            password_hash = user["password"]
            if check_password_hash(password_hash, password):
                return True, 200

        return False, 200


# API для проверки существования конкретного логина (чтобы не повторялись)
class CheckLogin(Resource):
    def get(self, login=''):
        if login == '':
            return True, 200
        if not users.find_one({'login': login}):
            return False, 200
        return True, 200


# регистрация API
api.add_resource(LoginUser, "/login_user/<string:login>&<string:password>")
api.add_resource(CheckLogin, "/check_login/<string:login>", "/check_login/")

# запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
