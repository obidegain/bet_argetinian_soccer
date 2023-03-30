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

el nombre de la base de datos tiene que ser la misma que se definió dos pasos atrás en NAME (en este caso el nombre de la base de datos sería "bet_argentina_soccer").

```sql
CREATE DATABASE nombre_de_la_base_de_dtos;
```

Si lo hacemos para este proyecto sería:

```sql
CREATE DATABASE bet_argentina_soccer;
```

Create a models and admin. For a simple admin:
```sh
from django.contrib import admin
from .models import model_name

admin.site.register(Model_name)
```

crear un superuser:
```sh
python manage.py createsuperuser
```

run makemigrations and migrate:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

Enter to http://localhost:8000/admin/ with any browser


## Signals

Las señales nos sirven para ejecutar acciones automaticamente luego que se haya ejecutado una situación en una instancia.

Por ejemplo, queremos que luego de que se guarde el resultado de un partido (instancia Match) se actualicen todos los puntajes de las apuestas (que tienen como uno de sus campos la instancia Match).

Para esto, (ya hemos creado la lógica de actualización de puntajes dentro de la instancia Bet, dentro de la función save) vamos a crear un función dentro del archivo signals.py.

```sh
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Bet

@receiver(post_save, sender=Match)
def upload_score_bets(sender, instance, **kwargs):
    bets = Bet.objects.filter(match=instance)
    for bet in bets:
        bet.save()
```

Pero debemos sentar las bases para que esta función se ejecute. Esto se agrega al archivo app.py la siguiente función en la clase "NombreDeLaAppConfig".

```sh
def ready(self):
        import NombreDeLaAppsignals
```

En nuestro caso el NombreDeLaApp es main, entonces el archivo final queda asi:

```sh
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals
```
