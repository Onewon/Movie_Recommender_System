# Django_Movie_Recommender_System
This repository is one Final Year Project, based on Python Django Web framework. Build Movie Recommender System by implementing collaborative filtering algorithm.
There are several main functionalities:
 - 1.Recommanding user favorites movies.
 - 2.Recommanding Watched the same movie's people who favorites movies.
 - 3.Searching target movie.
## Getting Started：
To setup on your local machine:
1. Install Anaconda with Python >= 3.5.(64bit), create a conda environment and activate it.
2. Prepare python dependency
```
{Anaconda.location}\Scripts\pip install -r requirements.txt
```
3. Prepare movie Dataset and configure MySQL databases:
use [MovieLens Dataset](https://grouplens.org/datasets/movielens/), import rating and links csv files into MySQL database, configure it in MRS/settings.py
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
5. Ensure Redis server running in machine and run Celery to process asynchronous tasks
```
celery worker -A MRS -l info
```
6. Run django server
```
python manage.py runserver
```
