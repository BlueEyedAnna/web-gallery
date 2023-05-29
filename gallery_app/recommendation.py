import pandas as pd
from get_recommendation import Similar

NUM_OF_RATINGS = 21


def read_file(filename=None):
    if filename:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.readlines()
        return text


def write_to_file(filename=None, text=None):
    if filename:
        with open(filename, 'a+', encoding='utf-8') as f:
            f.writelines(text)


def get_another(art_id, sign: str, all_arts):
    sign_search = all_arts[all_arts['artId'].str.contains(str(art_id), case=False, na=False)]
    sign_name = sign_search.iloc[0][sign]

    arts_search = all_arts[all_arts[sign].str.contains(str(sign_name), case=False, na=False)]
    another_arts = arts_search['artId'].tolist()
    if another_arts:
        return int(another_arts.pop())


def make_excursion(user_ratings, ratings):  # => пользователь прошел опрос по оценке картин
    # global NUM_OF_RATINGS
    # NUM_OF_RATINGS += 1

    # user_ratings = dict.fromkeys([5.0, 4.0, 3.0, 2.0, 1.0], [])

    # text = read_file('files/user_ratings.csv')
    # for i in range(1, len(text)):
    #     # Распределение id картин по поставленным за них баллам
    #     splited = text[i].split(',')
    #     user_ratings[float(splited[1])].append(splited[0])
    #     # Добавление номера пользователя в строку
    #     text[i] = f'{NUM_OF_RATINGS},' + text[i]
    # text[1] = '\n' + text[1]
    # write_to_file('ratings.csv', text[1:])

    arts = pd.read_csv('files/arts.csv')  # Список 20 картин
    # Удаление ненужных столбцов
    arts.drop(['artist'], axis=1, inplace=True)
    arts.drop(['epoch'], axis=1, inplace=True)
    arts.drop(['genre'], axis=1, inplace=True)

    # ratings2 = pd.read_csv('files/ratings.csv')  # Общий рейтинг для 20 картин
    all_arts = pd.read_csv('files/arts_all.csv')  # Список всех картин

    excursion = []
    search = Similar(arts, ratings)

    for key, value in user_ratings.items():  # цикл по баллам, выставленным пользователем
        for art_id in value:
            # Поиск похожих по рейтингу для одной картины
            _id = int(art_id)
            excursion.extend(search.get_result(_id, k=5))
            excursion.append(get_another(_id, 'artist', all_arts))
            excursion.append(get_another(_id, 'epoch', all_arts))
            excursion.append(get_another(_id, 'genre', all_arts))
            # excursion = list(map(int, excursion))
            excursion = list(set(excursion))
        if len(excursion) > 25:
            break
    # excursion.extend(search.get_result(2, k=3))
    for ele in excursion:
        if ele is None:
            excursion.remove(ele)
    return excursion


# result = make_excursion()
# print(result)
