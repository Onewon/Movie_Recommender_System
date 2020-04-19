# Django Movie Recommender System
The Recommender System is based on python Django web framework. Build movie recommender system by implementing user-based collaborative filtering algorithm.
There are several main functionalities:

 - 1.Recommending user favorites movies.
 - 2.Recommending movie similar to watched movies from user.
 - 3.Searching target movie.

##  [Screenshots](https://github.com/Onewon/Movie_Recommender_System/blob/master/screenshots/Screenshots.md)

## Getting Started
To setup on your local machine:
1. Install Python >= 3.5.(64bit)
2. Prepare python dependency
```
pip.exe install -r requirements.txt
```
3. Prepare movie Dataset and configure MySQL databases or directly use csv files: use [MovieLens dataset](https://grouplens.org/datasets/movielens/),to import rating and links csv files into MySQL database, and configure it in MRS/settings.py
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
5. Run django server

```
python manage.py runserver
```
