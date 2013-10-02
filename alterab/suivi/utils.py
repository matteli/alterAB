# coding=UTF-8
from django.forms.util import ErrorList
from suivi.forms import *
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.shortcuts import render_to_response


class No_error_list(ErrorList):
    def __unicode__(self):
        return ""

def role_user(utilisateur):
    if utilisateur.is_authenticated():
        try:
            utilisateur_extend = Utilisateur_extend.objects.get(user=utilisateur)
            return utilisateur_extend.role
        except:
            return 0
    else:
        return 0

def render_message(request, message="Erreur"):
    c = {'content': message}
    #c.update(csrf(request))
    return render_to_response('message.html', c, context_instance=RequestContext(request))


class disableCSRF:
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return None
