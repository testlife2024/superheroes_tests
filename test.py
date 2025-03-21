import requests
import os
import pytest
from unittest.mock import patch, Mock


def work(a: str): #функция проверяющая наличие работы
    response_work = requests.get(f'https://akabab.github.io/superhero-api/api/work/{a}')
    if response_work.json()['occupation'] == '-':
        return False
    else:
        return True


def top_high(gender: str, occupation: bool):#функция, выводящая самого высокого героя
    height_list = []
    for x in os.listdir('superhero-api/api/id'):
        base_url = f'https://akabab.github.io/superhero-api/api/appearance/{x}'
        response = requests.get(base_url)

        if response.status_code != 200:
            continue

        data = response.json()
        gender_hero = data['gender']
        height = data['height']

        if (gender_hero == gender and
                work(x) == occupation and
                height not in ['-', '0 cm'] and
                (gender in ['Male', 'Female'])):
            height_list.append(height)

    if height_list:
        print(max(height_list))
    else:
        print("No valid heights found.")


def test_work_valid_occupation(): #тест, проверяющий выводится ли значение True, если работа имеется
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {'occupation': 'Hero'})
        assert work('some_id') is True


def test_work_no_occupation():#тест, проверяющий выводится ли значение False, если работы нет
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {'occupation': '-'})
        assert work('some_id') is False


if __name__ == "__main__":
    pytest.main()










