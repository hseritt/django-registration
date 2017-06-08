# django-registration

A user registration app for your Django project. Very simple to configure and customize.

## Setup

Download the Registration app from [https://github.com/hseritt/django-registration/archive/master.zip](https://github.com/hseritt/django-registration/archive/master.zip):

```
# cd <django_project>
# wget https://github.com/hseritt/django-registration/archive/master.zip
# unzip master.zip
```

This will create a directory called: django-registration-master

Change the name of this folder to registration:

```
# mv django-registration-master/ registration
```

Open <django_project>/<project_name>/settings.py. Add 'registration' to INSTALLED_APPS:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
]
```

Add a staticfiles_dirs entry for the app:

```
STATICFILES_DIRS = (
    'static',
)
```

Also, add your email settings to settings.py. Below is an example that uses Gmail SMTP:

```
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'MyPassw0rd' #my gmail password
EMAIL_HOST_USER = 'my.name@gmail.com' #my gmail username
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

Save settings.py.

Open <django_project>/<project_name>/urls.py. Make sure you import "include" from django.conf.urls and add the registration prefix url to urlpatterns:

```
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registration/', include('registration.urls')),
]
```

Run migrations to your database:

```
# ./manage.py migrate
```

Start the Django dev server:

```
# ./manage.py runserver
```

Open browser to [http://localhost:8000/registration/](http://localhost:8000/registration/)