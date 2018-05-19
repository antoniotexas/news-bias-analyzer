# News Bias Analyzer
Our CSCE 470 Project

## Features
Given a list of preselected relevent politicians, it analyzes how biased news outlets are towards those individuals.

## How to Use

To use this project, follow these steps:

1. clone the application with
    `git clone https://github.tamu.edu/guillermo-lopez6988/NewsBiasAnalyzer.git`
2. Install Django (`$ sudo pip install django`)
3. Install whitenoise (`$ sudo pip install whitenoise`)
4. Install dj-database-url (`$ sudo pip install dj-database-url`)
5. Install rest framework (`$ sudo pip install djangorestframework`)
6. Install newspaper3k (`$ sudo pip3 install newspaper3k`)

## running locally

In case you want to run your Django application from the terminal just run:
Run syncdb command to sync models to database and create Django’s default superuser and auth system
	
	$ python manage.py migrate
	$ python manage.py runserver $IP:$PORT
	
In cloud 9: To change the version of python from 2 to 3 (needed for newspaper3k)
	
	$ sudo mv /usr/bin/python /usr/bin/python2
	$ sudo ln -s /usr/bin/python3 /usr/bin/python

To verify python version was succesfully changed
	$ python --version
	
Install django again to make it compatible with python 3
	$ sudo pip3 install django

## The projected can be found at:
https://new-bias-analyzer.herokuapp.com/


## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate
    
    add nlp to heroku 
    nltk.txt tells heroku which corpora to download.
    
## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)

## Code Retrieved From Internet:

- [Material Design Checkbox Example](https://codepen.io/hansmaad/pen/qaGrQL/)
