import pickle

# Функция для сохранения данных пользователей в файл
def save_user_filters(user_filters: dict):
    with open('user_filters.pkl', 'wb') as f:
        pickle.dump(user_filters, f)

# Функция для загрузки данных пользователей из файла
def load_user_filters():
    try:
        with open('user_filters.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}
