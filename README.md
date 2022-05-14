# Тестирование социальной сети Yatube
### Описание
```
Написание тестов для проекта Yatube. Проверяются URL адреса, шаблоны, формы, загруженные изображения и т.д. Основа для написания тестов - Unittest
```
### Технологии
```
Python 3.10
Django 2.2.16
Pillow 8.3.1
requests 2.26.0
sorl-thumbnail 12.7.0
django-debug-toolbar 2.2
pytest-django 3.8.0
pytest-pythonpath 0.7.3
pytest 5.3.5
```
### Как запустить проект: 
- Клонировать репозиторий: 
```
git clone https://github.com/sat0304/hw04_tests.git
```
- Перейти в него в командной строке 
```
cd hw04_tests
```
- Установить и активировать виртуальное окружение
```
python3 -m venv venv 
source venv/bin/activate
```
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Выполнить миграции: 
```
python3 manage.py migrate 
```
- В папке с файлом manage.py выполнить команду:
```
python manage.py runserver
```
### Автор
С.А.Токарев
