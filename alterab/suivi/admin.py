from suivi.models import *
from django.contrib import admin

admin.site.register(Utilisateur_extend)
admin.site.register(Tuteur_UFA)
admin.site.register(Tuteur_entreprise)
admin.site.register(Apprenti)
admin.site.register(Config_referentiel)
#admin.site.register(Groupe_savoir)
admin.site.register(Groupe_competence)
admin.site.register(Groupe_tache)
#admin.site.register(Savoir)
admin.site.register(Competence)
admin.site.register(Tache)
#admin.site.register(Savoir_dans_competence)
admin.site.register(Competence_dans_tache)
admin.site.register(Activite_entreprise)
admin.site.register(Competence_dans_activite)
#admin.site.register(T_Activite_ufa)
#admin.site.register(T_Competence_dans_t_activite_ufa)
#admin.site.register(T_Savoir_dans_t_competence_ufa)
#admin.site.register(Activite_ufa)
#admin.site.register(Competence_dans_activite_ufa)
#admin.site.register(Savoir_dans_competence_ufa)