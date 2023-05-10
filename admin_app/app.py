import base64
import datetime
import random

from bson.objectid import ObjectId
from flask_restful import Resource
from flask import redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin

from admin_app import app, db, api


# класс пользователя
class User(UserMixin):
    def __init__(self, user):
        # распаковываем поля для удобства
        self.id = user['_id']
        self.login = user['login']
        self.password = user['password']

    # метод получения id (нужен для работы фласка)
    def get_id(self):
        return self.id


# для авторизации
login_manager = LoginManager(app)
# коллекция пользователей (для упрощения обращения)
admins_db = db['administrators']
exhibitions_db = db['exhibitions']
excursions_db = db['excursions']


@app.route('/excurs_change', methods=['GET', 'POST'])
def excurs_change():
    if current_user.is_authenticated:
        if request.method == 'GET':
            excursions = list(db['excursions'].find())
            excursions_count = len(excursions)

            block = []
            output = []
            ind = -1

            for excursion in excursions:
                ind += 1

                if ind % 2 == 0:
                    if ind != 0:
                        output.append(block)

                    block = [excursion]
                else:
                    block.append(excursion)

            output.append(block)

            return render_template(
                "excurs_change.html",
                ver=datetime.datetime.now().timestamp(),
                is_authenticated=True,
                excursions=output,
                excursions_count=excursions_count
            )
    else:
        return redirect(url_for('index'))


def change_excurs_list():
    print("Ok")


@app.route('/delete_excursion', methods=['POST'])
def delete_excursion():
    delete_id = request.form['id']
    excursions_db.delete_one({'_id': ObjectId(delete_id)})

    return redirect(url_for('excurs_change'))


@app.route('/add_excursion', methods=['GET', 'POST'])
def add_excursion():
    if request.method == 'GET':
        return render_template('add_excursion.html',
                               ver=datetime.datetime.now().timestamp(),
                               is_authenticated=True,
                               excursion=None)

    photos_in = request.files.getlist('imgs')
    photos = []

    for photo in photos_in:
        photo_str = str(base64.b64encode(photo.read()))
        photos.append(photo_str[2:-1])

    if 'stars' in request.form and request.form['stars']:
        stars = int(request.form['stars'])
    else:
        stars = 0

    if '_id' in request.form and request.form['_id']:
        result = excursions_db.update_one({'_id': ObjectId(request.form['_id'])}, {'$set': {
            'name': request.form['excursion_name'],
            'stars': stars,
            'photos': photos,
            'about': request.form['about']
        }})
    else:
        result = excursions_db.insert_one({
            'name': request.form['excursion_name'],
            'stars': int(request.form['stars']),
            'photos': photos,
            'about': request.form['about']
        })

    print(result)

    return redirect('excurs_change')  # redirect(f'/exhibition?id={result.inserted_id}')


@app.route('/modify_excursion', methods=['POST'])
def modify_excursion():
    if request.method == 'POST':
        modify_id = request.form['id']
        excursion = excursions_db.find_one({'_id': ObjectId(modify_id)})

        return render_template('add_excursion.html',
                               ver=datetime.datetime.now().timestamp(),
                               is_authenticated=True,
                               excursion=excursion)


def change_exhib_list():
    print("Ok")


@app.route('/delete_exhibition', methods=['POST'])
def delete_exhibition():
    delete_id = request.form['id']
    exhibitions_db.delete_one({'_id': ObjectId(delete_id)})

    return redirect(url_for('creation'))


@app.route('/add_exhibition', methods=['GET', 'POST'])
def add_exhibition():
    if request.method == 'GET':
        return render_template('add_exhibition.html',
                               ver=datetime.datetime.now().timestamp(),
                               is_authenticated=True,
                               exhibition=None)

    photos_in = request.files.getlist('imgs')
    photos = []

    for photo in photos_in:
        photo_str = str(base64.b64encode(photo.read()))
        photos.append(photo_str[2:-1])

    if 'stars' in request.form and request.form['stars']:
        stars = int(request.form['stars'])
    else:
        stars = 0

    if '_id' in request.form and request.form['_id']:
        result = exhibitions_db.update_one({'_id': ObjectId(request.form['_id'])}, {'$set': {
            'name': request.form['exhibition_name'],
            'stars': stars,
            'photos': photos,
            'about': request.form['about']
        }})
    else:
        result = exhibitions_db.insert_one({
            'name': request.form['exhibition_name'],
            'stars': int(request.form['stars']),
            'photos': photos,
            'about': request.form['about']
        })

    print(result)

    return redirect('creation')  # redirect(f'/exhibition?id={result.inserted_id}')


@app.route('/modify_exhibition', methods=['POST'])
def modify_exhibition():
    if request.method == 'POST':
        modify_id = request.form['id']
        exhibition = exhibitions_db.find_one({'_id': ObjectId(modify_id)})

        return render_template('add_exhibition.html',
                               ver=datetime.datetime.now().timestamp(),
                               is_authenticated=True,
                               exhibition=exhibition)


@app.route('/creation', methods=['GET', 'POST'])
def creation():
    if current_user.is_authenticated:
        if request.method == 'GET':
            exhibitions = list(db['exhibitions'].find())

            exhibitions_count = len(exhibitions)

            block_exhibitions = []
            output_exhibitions = []
            ind = -1

            for exhibition in exhibitions:
                ind += 1

                if ind % 2 == 0:
                    if ind != 0:
                        output_exhibitions.append(block_exhibitions)

                    block_exhibitions = [exhibition]
                else:
                    block_exhibitions.append(exhibition)

            output_exhibitions.append(block_exhibitions)

            return render_template(
                "creation.html",
                ver=datetime.datetime.now().timestamp(),
                is_authenticated=True,
                exhibitions=output_exhibitions,
                exhibitions_count=exhibitions_count
            )
    else:
        return redirect(url_for('index'))


# <editor-fold desc="Auth">


# это авторизация пользователя
@login_manager.user_loader
def load_user(user_id):
    user = admins_db.find_one({'_id': user_id})
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
    user = User(admins_db.find_one({'login': request.form.get('userLogin')}))

    # авторизуем его
    login_user(user, remember=rm)

    # перенаправляем на страницу добавления выставок
    return redirect(url_for("creation"))  # !!!!!!Изменить


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
        user = admins_db.find_one({"login": login})
        if user:
            if user["password"] == password:
                return True, 200
        return False, 200


# API для проверки существования конкретного логина (чтобы не повторялись)
class CheckLogin(Resource):
    def get(self, login=''):
        if login == '':
            return True, 200
        if not admins_db.find_one({'login': login}):
            return False, 200
        return True, 200


# регистрация API
api.add_resource(LoginUser, "/login_user/<string:login>&<string:password>")
api.add_resource(CheckLogin, "/check_login/<string:login>", "/check_login/")


# </editor-fold>

def load_arts_from_dir(dir):
    import os

    for file in os.listdir(dir):
        _id = file.split('_')[0]

        with open(dir + '/' + file, 'rb') as fs:
            photo_str = str(base64.b64encode(fs.read()))
            photo_str = photo_str[2:-1]

        db['art'].update_one({'_id': _id}, {'$set': {'image': photo_str}})


# запуск сервера
if __name__ == '__main__':
    # load_arts_from_dir('/Users/annatalova/Desktop/arts')
    app.run(host='0.0.0.0', port=5050, debug=True)
