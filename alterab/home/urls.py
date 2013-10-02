from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(r'droits_obligations/$', login_required(direct_to_template), {'template': 'home/droits_obligations.html'}),
    url(r'mission_tuteur_ufa/$', login_required(direct_to_template), {'template': 'home/mission_tuteur_ufa.html'}),
    url(r'mission_tuteur_entreprise/$', login_required(direct_to_template), {'template': 'home/mission_tuteur_entreprise.html'}),
    url(r'referentiel/$', login_required(direct_to_template), {'template': 'home/referentiel.html'}),
    url(r'^$', login_required(direct_to_template), {'template': 'home/textes.html'}),
)


