Here are some helpful instruction fork working with django, and mainly adding
templates. Make sure to install virtualenv, before doing anything there are
tutorials online on how to do it.

First we need to get the django project running, so open terminal and cd into
into the proper directory.

#### Initial Setup
First things first you need to source you virtual environment. If not created
you can create a virtual environment (preferable not in the git repo):
```
virtualenv [VIRTUAL_ENVIRONMENT_NAME]
```
I usually use simply v for my virtual environment name so I'm going to use
that for the rest of the README. If your virtualenv is already created you can
run 
```
source v/bin/activate
```
You'll know if you have properly run the command, because there will be a "(v)"
on the far left of your next bash command.

In order to detach from your virtual python environment run
```
deactivate
```
When this happens you should see the (v) o

Now cd back into the git repo. There should be a manage.py file in this
directory. First things first make sure you have all the requirements
installed. Run

```
pip install -r requirements.txt
```

Let that do it's work and then you can run

```
python manage.py runserver 
```

This will start a development server on port 8080, go to your browser and type
in 

```
localhost:8000
```
and you should be taken to the homepage. Assuming that worked you should be all
set up.

#### Adding/finding templates

In order to add a template you have to find the correspond view for that
template, each app has a views.py file, and in there are all the views. In the
views.py file you'll see something like this:
``` python
class CreateAccountView(View):
    template_name = 'create_account.html'
    form = UserCreationForm

    def get(self, request):
        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:it_worked'))

        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)
 ```
See the variable 
```python
template_name = 'create_account.html'
```
That specifies the name of the html file that that view will load. In each app
there should be a directory called tempaltes, and the file tree will look
something like this
```
[app namne]/
  migrations/
    [ignore these files]
  static/
    css/
      # This is where all your css will go
    imgs/
      # This is where all your images will go
    js/
      # This is where all your js will go
  templates/
    # html files
  admin.py
  apps.py
  forms.py
  models.py
  tests.py
  urls.py         # ! IMPORTANT
  views.py        # ! IMPORTANT 
```

***It's important ot remeber that each app has it's own templates directory, and
static directory.***

If you wanted to edit teh create_accounts.html file you would use:
```
vi accounts/templates/create_accounts.html
```
Then you'd be free to edit the html file. In order to find what the
corresponding url would be there's two place you need to go.

app/urls.py (this is the top level url file):
``` python
from django.conf.urls import url, include
from django.contrib import admin

from accounts.views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^dev/', include('echo-dev.urls', namespace='dev')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^recipes/', include('Recipes.urls', namespace='Recipes')),
    url(r'^session/', include('session.urls', namespace='session')),

    url(r'^admin/', admin.site.urls),
]
```
***Notice the varaible namespace='accounts' that's used for referecing the
html file in the tempaltes but we'll come back to that***
You'll notice there's a couple urls that have include example:

```
url(r'^accounts/', include('accounts.urls', namespace='accounts')),
```
This means that you can go looking for more urls in the accounts app and in the
urls.py file which looks like this

``` python
urlpatterns = [
    url(r'^createaccount/$', views.CreateAccountView.as_view(),
        name='create_account'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^linktoecho/$', views.LinkEchoToUserView.as_view(),
        name='link_echo_to_user'),

    url(r'^itworkd/$', views.ItWorkedView.as_view(), name='it_worked'),
]
```
If you remeber from the previous view create_account.html files was assoviated
with the CreateAccountView and if you look at this file you'll notice
```python
url(r'^createaccount/$', views.CreateAccountView.as_view(),
    name='create_account'),
```
***Notice the varaible name='create_account' that's used for referecing the
html file in the tempaltes but we'll come back to that***

If you want to get to the CreateAccountView which is associated with the
create_account.html file then you could follow the urls from the app/urls.py
file and the accounts/urls.py file. The urls in the accounts files are all
prepended with their include (in the app/urls.py file) so you could go to the
url:
```
localhost:8000/accounts/createaccount/
```
And you would be taken to the corresponding view which would render the
corresponding create_accounts.html template. If you want to change or add
templates you could do so by change the template_name variable in the
CreateAccountView class and then in the templates/ directory add that
corresponding html file. 

#### Django template notes

There's a few things your going to want to know about creating django
templates. First things firs tdjango has it's own templating engine. And it
simple goes through the html file and parses it with different information.
There are two things to look out for in django templates

```
{{ usually_some_variable }} 
or
{% usually_some_method %}
```

If those are ever in a django template it's going to get parsed and replaced by
something in the django templating engine. One of the most common tags is
something like this 

```
{% url 'accounts:create_account' %}
```

Remember the naemspace space variable and the name variable from the urls.py
files. Well those variables are used here to easily parse in the corresponding
url. The above line essentially the same as

```
/accounts/createaccount/
```

And the format of that tag is

```
{% url 'NAMESPACE:NAME' %}
```

##### Other useful tags 
###### if statement

```
{% if CONDITONAL %}

# html to be added only if it passes the conditonal

{% else %}

# html to be add if it fails 

{% endif %}
```
Something you might want to do would be
``` html
{% if user.is_authenticated %}
<form method="post" action="{% url 'accounts:login' %}">
  {% csrf_tokent %}
  <input type="text" name="username" placeholder="username">
  <input type="password" name="password" placeholder="password">
  <button type="submit">Login</button>
</form>

{% else %}

<p> Hello {{ user.email }}!</p>

{% endif %}
```

###### Loading static files 

At the top of the document add 

``` html
{% load static %}
```
Then you can load ***local*** static files by doing

``` html
<link href="{% static 'css/signin.css' %}" rel="stylesheet">
```
Or for JavaScript

``` html
<script src="{% static 'js/base.js' %}"></script>
```
or and image
``` html
<img src="{% static 'imgs/example.png' %}"></img>
```

###### For loops

It's also possible to do for loops in a django template example:

``` html
{% for book in books %}

<li>{{ book.title }}</li>

{% endfor }
```

You may be wondering where the books variable comes from, inside of a view you
can pass variables example. Lets look at CreateAccountView
``` python
class CreateAccountView(View):
    template_name = 'create_account.html'
    form = UserCreationForm

    def get(self, request):
        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:it_worked'))

        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)
 ```
 See how there's a context variable that is rendered with the text, that
 variable can be anything, and often time it'll be a list of things. If say
 books was a list of books that the above html code would have iterated through
 all the books inside context['books'] and displayed there title. 

#### Bootstrap and CDNs

Often times you going to want to load outside resources into an html file such
as bootstrap, in my opinion the best way to do that is to use a CDN. All major
javascript and css libraries have a cdn, and all you would do to added that
library would be to make their src or href attribute equal to the url. Example:

``` html

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

```

In order to find the cdn for somehting like jquery just google jquery cdn and
it'll probably be one of the first links. 


Ok that covers most of the basics, if you have any questions feel free to ask,
and I'll try to add things here.
