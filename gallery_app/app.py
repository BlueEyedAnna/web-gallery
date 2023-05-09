import base64
import datetime
import random

from bson.objectid import ObjectId
from flask_restful import Resource
from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from gallery_app import app, db, api


# класс пользователя со всеми его полями
class User(UserMixin):
    def __init__(self, user):
        # распаковываем поля для удобства
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
# коллекция пользователей (для упрощения обращения)
users = db['users']
art_db = db['art']


@app.route('/exhibitions', methods=['GET'])
def exhibitions():
    exhibitions = list(db['exhibitions'].find())

    exhibitions_count = len(exhibitions)

    block_exhibitions = []
    output_exhibitions = []
    ind = -1

    for exhibition in exhibitions:
        ind += 1

        if ind % 3 == 0:
            if ind != 0:
                output_exhibitions.append(block_exhibitions)

            block_exhibitions = [exhibition]
        else:
            block_exhibitions.append(exhibition)

    output_exhibitions.append(block_exhibitions)

    return render_template(
        'exhibitions.html',
        ver=datetime.datetime.now().timestamp(),
        is_authenticated=current_user.is_authenticated,
        exhibitions=output_exhibitions,
        exhibitions_count=exhibitions_count
    )


@app.route('/exhibition', methods=['GET'])
def exhibition():
    current_exhibition = db['exhibitions'].find_one({'_id': ObjectId(request.args.get('id'))})

    return render_template(
        'exhibition.html',
        ver=datetime.datetime.now().timestamp(),
        is_authenticated=current_user.is_authenticated,
        exhibition=current_exhibition
    )


@app.route("/excursions", methods=['GET'])
def excursions():
    excursions_db = list(db['excursions'].find())
    excursions_count = len(excursions_db)

    block = []
    output = []
    ind = -1

    for _excursion in excursions_db:
        ind += 1

        if ind % 3 == 0:
            if ind != 0:
                output.append(block)

            block = [_excursion]
        else:
            block.append(_excursion)

    output.append(block)

    return render_template(
        'excursions.html',
        ver=datetime.datetime.now().timestamp(),
        is_authenticated=current_user.is_authenticated,
        excursions=output,
        excursions_count=excursions_count
    )


@app.route('/excursion', methods=['GET'])
def excursion():
    current_excursion = db['excursions'].find_one({'_id': ObjectId(request.args.get('id'))})

    return render_template(
        'excursion.html',
        ver=datetime.datetime.now().timestamp(),
        is_authenticated=current_user.is_authenticated,
        excursion=current_excursion
    )


@app.route("/filter")
def filter():
    arts = list(db['art'].find())
    arts_count = len(arts)

    block = []  # 5
    output = []
    ind = -1

    for art in arts:
        ind += 1

        if ind % 2 == 0:
            if ind != 0:
                output.append(block)

            block = [art]

        else:
            block.append(art)

    output.append(block)

    return render_template(
        "filter.html",
        ver=datetime.datetime.now().timestamp(),
        is_authenticated=current_user.is_authenticated,
        arts=output,
        arts_count=arts_count
    )


@app.route('/me', methods=['GET', 'POST'])
def me():
    if current_user.is_authenticated:
        if request.method == 'GET':
            return render_template(
                'me.html',
                ver=datetime.datetime.now().timestamp(),
                is_authenticated=True,
                user=current_user
            )
        elif request.method == 'POST':
            update = {}

            if request.files.get('avatar'):
                update['avatar'] = str(base64.b64encode(request.files.get('avatar').read()))[2:-1]

            if request.form['login']:
                update['login'] = request.form['login']

            if request.form['email']:
                update['email'] = request.form['email']

            if request.form['phone']:
                update['phone'] = request.form['phone']

            if request.form['fio']:
                update['fio'] = request.form['fio']

            if (request.form['password']
                    and request.form['password2']
                    and request.form['password'] == request.form['password2']):
                update['password'] = generate_password_hash(request.form['password'])

            if len(update.keys()) != 0:
                users.update_one({'_id': current_user.id}, {'$set': update})

            return redirect(url_for('me'))
    else:
        return redirect(url_for('index'))


# <editor-fold desc="Auth">
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
@app.route("/registration", methods=["POST"])
def registration():
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


# </editor-fold>

# <editor-fold desc="API">
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
# </editor-fold>

# запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
