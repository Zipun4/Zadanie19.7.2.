from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, \
                    empty_email, empty_password, invalid_auth_key, empty_auth_key
import os

pf = PetFriends()


def test_get_api_key_for_invalid_password_failed(email=valid_email, password=invalid_password):
    """Передаем не правильный пароль, ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200


def test_get_api_key_for_invalid_email_failed(email=invalid_email, password=valid_password):
    """Передаем не правильный E-mail, ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200


def test_get_api_key_for_empty_password_failed(email=valid_email, password=empty_password):
    """Передаем "пустой" пароль, ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200


def test_get_api_key_for_empty_data_failed(email=empty_email, password=empty_password):
    """Передаем "пустой" пароль и E-mail", ожидаемый результат - FAILED"""

    status, _ = pf.get_api_key(email, password)
    assert status == 200


def test_get_all_pets_with_invalid_key_failed(filter=''):
    """Передаем не корректный ключ для получения списка питомцев, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(invalid_auth_key, filter)
    assert status == 200



def test_get_all_pets_with_empty_key_failed(filter=''):
    """Передаем "пустой" ключ для получения списка питомцев, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(empty_auth_key, filter)
    assert status == 200


def test_add_new_pet_with_invalid_auth_key_failed(name='98707707', animal_type='667676776',
                                     age='4', pet_photo='images/cat2.gif'):
    """Добавляем питомца с некорректным ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(invalid_auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_new_pet_with_empty_auth_key_failed(name='870770', animal_type='667676776',
                                     age='4', pet_photo='images/cat2.gif'):
    """Добавляем питомца с "пустым" ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(empty_auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_self_pet_invalid_auth_key_failed():
    """Удаление питомца с "пустым" ключом, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_add_photo_pet(pet_photo='images/P1040103.jpg'):
    """Добавление фотографии к карточке питомца, ожидаемый результат - PASSED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")


def test_add_photo_pet_with_invalid_key_failed(pet_photo='images/P1040103.jpg'):
    """Добавление фотографии к карточке питомца с некорректным ключом, ожидаемый результат - FAILED"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(invalid_auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert "pet_photo" in result
    else:
        raise Exception("There is no my Pets")

def test_succesful_add_new_pet_no_photo_with_valid_data(name='934444443', animal_type='Homyak',
                                     age='45'):
    """Добавление нового питомца без фотографии, ожидаемый результат - PASSED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_no_photo_with_invalid_key_failed(name='93333333', animal_type='Homyak',
                                     age='45'):
    """Добавление нового питомца без фотографии с некорректным ключом, ожидаемый результат - FAILED"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(invalid_auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name