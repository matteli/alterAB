from django.conf.urls.defaults import *
from suivi.views import activite_consultation


urlpatterns = patterns('suivi',
    #(r'ajout_activite', 'views.ajout_activite'),
    url(r'entreprise/ajout/$', 'views.ajout_activite', name='activite_entreprise_ajout'),
    url(r'liste/$', 'views.liste_activite', name='liste_activite'),
    url(r'entreprise/modification/(?P<id_activite>[0-9]*)/$','views.ajout_activite', name='activite_entreprise_modification'),
    url(r'entreprise/consultation/(\d+)/$', activite_consultation),
    #url(r'sequence/ajout/$', 'views.ajout_sequence', name='sequence_ufa_ajout'),
)
