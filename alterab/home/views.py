# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from suivi.forms import *
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from suivi.utils import *
from django.contrib.auth.decorators import login_required

def accueil(request):
    #import pdb; pdb.set_trace()
    if role_user(request.user)==1:
        template = 'home/accueil_apprenti.html'
    elif role_user(request.user)==2:
        template = 'home/accueil_tuteur_entreprise.html'
    elif role_user(request.user)==3:
        template = 'home/accueil_tuteur_CFA.html'
    else:
        template = 'home/accueil.html'
    return render_to_response(template, context_instance=RequestContext(request))

