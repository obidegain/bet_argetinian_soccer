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
```py
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
sudo apt install python3-dev libpq-dev
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
```py
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
```py
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

crear un superuser:
```sh
python manage.py createsuperuser
```

to complete all migrations, you must be add the apps that you has been created to settings:
```py
INSTALLED_APPS = [
    'name_of_your_app',
]
```
run makemigrations and migrate:
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

runserser:
```sh
python manage.py runserver
```


Enter to http://localhost:8000/admin/ with any browser


## Signals

Las señales nos sirven para ejecutar acciones automaticamente luego que se haya ejecutado una situación en una instancia.

Por ejemplo, queremos que luego de que se guarde el resultado de un partido (instancia Match) se actualicen todos los puntajes de las apuestas (que tienen como uno de sus campos la instancia Match).

Para esto, (ya hemos creado la lógica de actualización de puntajes dentro de la instancia Bet, dentro de la función save) vamos a crear un función dentro del archivo **signals.py**.

```py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Bet

@receiver(post_save, sender=Match)
def upload_score_bets(sender, instance, **kwargs):
    bets = Bet.objects.filter(match=instance)
    for bet in bets:
        bet.save()
```

Pero debemos sentar las bases para que esta función se ejecute. Esto se agrega al archivo **app.py** la siguiente función en la clase "NombreDeLaAppConfig".

```py
def ready(self):
        import NombreDeLaAppsignals
```

En nuestro caso el NombreDeLaApp es main, entonces el archivo final queda asi:

```py
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals
```


## Authentication

The original documentation is: 

https://docs.djangoproject.com/en/4.2/topics/auth/default/


But, in the practice you have many ways to use the original athentication login. In summary, you have 2:
1) Verify manually if the user is logged
2) Used a decorator that do the same that the topic 1).

### Login path

First, in both cases you must create the login path.

You must go to de **urls.py** and add the follow path:

```py
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
```

```py
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ....
]
```

In the above example you use the original template. But if you have a your specific login.html, you can use it:

```py
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    ....
]
```

### Redirect 

When an user tries to entry of a specific path that have a login requiered, after entry, django redirects to a default path that is **'accounts/profile/'**. But, if you what to change this path you can add the following line in **settings.py**:

```py
LOGIN_REDIRECT_URL = '/apuestas/'
```

or the path that you want.


### CASE 1: login_required manually

So, in this moment you have the login paht, the redirect path and you have all to add the lines in the view that you need have a login_required.

The view class must be like this:

```py
def view_name(request):
    if request.user.is_authenticated:
        ...
    else:
        return redirect('login')
```

For example, I had the following view class:

```py
def bet_list(request):
    user_bets = Bet.objects.filter(user=request.user)
    context = {
        'user_bets': user_bets
    }
    return render(request, 'bet_list.html', context)
```

And after of the login requiered manually:

```py
def bet_list(request):
    if request.user.is_authenticated:
        user_bets = Bet.objects.filter(user=request.user)
        context = {
            'user_bets': user_bets
        }
        return render(request, 'bet_list.html', context)
    else:
        return redirect('login')
```


### CASE 2: login_required decorator

You can do the same easier. Only add one line:

For example, I had the following view class:

```py
def bet_list(request):
    user_bets = Bet.objects.filter(user=request.user)
    context = {
        'user_bets': user_bets
    }
    return render(request, 'bet_list.html', context)
```

And after of the login requiered decorator:

```py
@login_required(login_url="/login/")
def bet_list(request):
    user_bets = Bet.objects.filter(user=request.user)
    context = {
        'user_bets': user_bets
    }
    return render(request, 'bet_list.html', context)
```
