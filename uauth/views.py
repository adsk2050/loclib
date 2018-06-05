from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import models, urls
from django.http import  HttpResponseRedirect
from django.urls import reverse


# Create your views here.
##################################################
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('catalog:index'))
    else:
        return HttpResponseRedirect(reverse('uauth:login'))

#class MyLogin(auth_views.LoginView)


    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    #return HttpResponseRedirect(reverse('polls:results', #args=(question.id,)))
