from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_add_new_pet_with_valid_data(name='Сэлем', animal_type='кот', age='10', pet_photo=''):
    """Проверяем, можно ли добавить питомца, не указав фотографию, когда она должна быть"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_pet_no_photo_with_valid_data(name='Леонард', animal_type='КОТЭ', age='8', pet_photo='images/cat1.jpg'):
    """Проверяем, можно ли добавить питомца, указав фотографию, которая не предусмотрена"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления определенного питомца по id"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Вводим id питомца из списка, которого хотим удалить и отправляем запрос на удаление
    pet_id = input()
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='', animal_type='', age=5):
    """Проверяем возможность обновления информации о питомце, заменив имя и тип на пустые значения"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_with_valid_data(name='Сэлем', animal_type='кот', age='-1', pet_photo='images/cat1.jpg'):
    """Проверяем, можно ли добавить питомца, указав отрицательный возраст"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if age < 0:
        assert status == 403
    else:
        assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name='Сэлем', animal_type='кот', age='10', pet_photo='images/cat1.jpg'):
    """Проверяем, можно ли добавить питомца без почты и пароля"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key()

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name='Сэлем', animal_type='кот', age='10', pet_photo='images/cat1.jpg'):
    """Проверяем, можно ли добавить питомца без ключа аутентификации"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=-2):
    """Проверяем возможность обновления информации о питомце, введя другие логин и пароль"""

    # Получаем ключ auth_key и список своих питомцев
    valid_email = "FTL@gmail.com"
    valid_password = "qwertyuiop"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_pet_no_photo_with_valid_data(name='Леонард', animal_type='КОТЭ', age='8'):
    """Проверяем, можно ли добавить питомцу фотографию"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фотографию и питомца
    pet_photo = 'images/cat1.jpg'
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_get_api_key_for_valid_user():
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key при условии,
     что логин и пароль вводятся пользователем"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    email = "FTL@gmail.com"
    password = "qwertyuiop"
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result