# Create your first django-project

## Getting started

### Virtualenv

First, install virtual env
```sh
python3 -m pip install --upgrade pip
```

Create a virtual environment
```sh
python3 -m venv venv
```

Activate the venv
```sh
source venv/bin/activate
```

Install the libraries
```sh
asgiref==3.6.0
asttokens==2.2.1
backcall==0.2.0
decorator==5.1.1
Django==4.1.7
django-extensions==3.2.1
executing==1.2.0
ipython==8.11.0
jedi==0.18.2
MarkupSafe==2.1.2
matplotlib-inline==0.1.6
parso==0.8.3
pexpect==4.8.0
pickleshare==0.7.5
prompt-toolkit==3.0.38
psycopg2==2.9.5
ptyprocess==0.7.0
pure-eval==0.2.2
Pygments==2.14.0
six==1.16.0
sqlparse==0.4.3
stack-data==0.6.2
traitlets==5.9.0
wcwidth==0.2.6
Werkzeug==2.2.3
```

if you have a problem to install psycopg2, try:
```sh
pip3 install psycopg2
```

Create the django-project (en este caso nombre_proyect = BetsSport)
```sh
django-admin startproject nombre_proyecto 
```

Entry to the folder the project and create a django-app
```sh
cd nombre_proyecto
```
```sh
python manage.py startapp main
```

Modify file settings.py the DATABASE parameter:
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bet_argentina_soccer',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Install postgres and create the database
```sh
sudo -u postgres psql
```

```sql
CREATE DATABASE nombre_proyect;
```

Create a models and admin. For a simple admin:
```sh
from django.contrib import admin
from .models import model_name

admin.site.register(Model_name)
```

run makemigrations and migrate:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

Enter to http://localhost:8000/admin/ with any browser


