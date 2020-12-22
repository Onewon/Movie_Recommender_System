# Django Movie Recommender System
This repository is based on python Django web framework. Build movie recommender system by implementing collaborative filtering algorithm.
There are several main functionalities:

 - 1.Recommending user favorites movies.
 - 2.Recommending watched movies from people who favorites same movies.
 - 3.Searching target movie.

##  [Screenshots](https://github.com/Onewon/Movie_Recommender_System/blob/master/screenshots/Screenshots.md)

## Getting Started
To setup on your local machine:
1. Install Anaconda with Python >= 3.5.(64bit), create a conda environment and activate it.
2. Prepare python dependency
```
pip install -r requirements.txt
```
3. Prepare movie Dataset and configure MySQL databases:
use [MovieLens dataset](https://grouplens.org/datasets/movielens/),to import rating and links csv files into MySQL database, and configure it in MRS/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': [database name],
        'USER': 'root',
        'PASSWORD': [password],
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
4. Migrate
```
python manage.py makemigrations
python manage.py migrate
```
5. Ensure RabbitMQ and Redis server running in machine and run Celery to process asynchronous tasks
```
celery -A MRS worker -P gevent -c 100 -l info
```
6. Run django server
```
python manage.py runserver
```
