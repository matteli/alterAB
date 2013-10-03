# coding=UTF-8
from django.db import models
from django.contrib.auth.models import User
import datetime

#Personnes
class Utilisateur_extend(models.Model):
    ROLE_CHOIX = (
        (0, u'Pas de rôle'),
        (1, u'Apprentis'),
        (2, u'Tuteur entreprise'),
        (3, u'Tuteur UFA'),
        (4, u'Responsable'),
    )
    user = models.OneToOneField(User)
    role = models.IntegerField(choices=ROLE_CHOIX)
    
    def __unicode__(self):
        return self.user.username

class Tuteur_UFA(models.Model):
    utilisateur_extend = models.OneToOneField(Utilisateur_extend)
    matiere = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.utilisateur_extend.user.username

class Tuteur_entreprise(models.Model):
    utilisateur_extend = models.OneToOneField(Utilisateur_extend)
    fonction = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.utilisateur_extend.user.username

class Apprenti(models.Model):
    utilisateur_extend = models.OneToOneField(Utilisateur_extend)
    tuteur_UFA = models.ForeignKey(Tuteur_UFA, null=True, on_delete=models.SET_NULL)
    tuteur_entreprise = models.ForeignKey(Tuteur_entreprise, null=True, on_delete=models.SET_NULL)
    promotion = models.IntegerField()
    
    def __unicode__(self):
        if self.utilisateur_extend.user.last_name:
            return (self.utilisateur_extend.user.first_name + ' ' + self.utilisateur_extend.user.last_name)
        else:
            return (self.utilisateur_extend.user.username)

#Referentiel
class Config_referentiel(models.Model):
    nom_diplome = models.CharField(max_length=200)
    
    #nombre de groupements
    nombre_niveaux_savoirs = models.IntegerField()
    nombre_niveaux_competences = models.IntegerField()
    nombre_niveaux_taches = models.IntegerField()
    
    #nom utilise dans le referentiel
    nom_savoirs = models.CharField(max_length=200)
    nom_competences = models.CharField(max_length=200)
    nom_taches = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nom_diplome

'''class Groupe_savoir(models.Model):
    niveau = models.IntegerField()
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    commentaires = models.TextField(max_length=1000, blank=True)
    groupe = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return (self.ref_referentiel+self.nom)'''

class Groupe_competence(models.Model):
    niveau = models.IntegerField()
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    commentaires = models.TextField(max_length=1000, blank=True)
    groupe = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return (self.ref_referentiel+self.nom)

class Groupe_tache(models.Model):
    niveau = models.IntegerField()
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    commentaires = models.TextField(max_length=1000, blank=True)
    groupe = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return (self.ref_referentiel+self.nom)

'''class Savoir(models.Model):
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    niveau_taxo = models.IntegerField()
    commentaires = models.TextField(max_length=1000, blank=True)
    groupe = models.ForeignKey(Groupe_savoir, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return (self.ref_referentiel+self.nom)'''

class Competence(models.Model):
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    groupe = models.ForeignKey(Groupe_competence, null=True, blank=True, on_delete=models.SET_NULL)
    #savoirs = models.ManyToManyField(Savoir, through='Savoir_dans_competence')
    
    def __unicode__(self):
        return (self.ref_referentiel + " " + self.nom)

class Tache(models.Model):
    ref_referentiel = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    groupe = models.ForeignKey(Groupe_tache, null=True, blank=True, on_delete=models.SET_NULL)
    competences = models.ManyToManyField(Competence, through='Competence_dans_tache')
    
    def __unicode__(self):
        return (self.ref_referentiel + " " + self.nom)

'''class Savoir_dans_competence(models.Model):
    savoir = models.ForeignKey(Savoir)
    competence = models.ForeignKey(Competence)
    nb = models.IntegerField()'''
    

class Competence_dans_tache(models.Model):
    tache = models.ForeignKey(Tache)
    competence = models.ForeignKey(Competence)
    nb = models.IntegerField()
    def __unicode__(self):
        return (self.competence.nom+u' est lié à '+self.tache.nom)

#Activités
class Activite_entreprise(models.Model):
    apprenti = models.ForeignKey(Apprenti, default=1)
    tache = models.ForeignKey(Tache, verbose_name=u"Tâche réalisée par l'apprenti")
    description = models.TextField(verbose_name=u"Description générale de l'activité",max_length=1000)
    date = models.DateField(verbose_name=u"Date de début de l'activité")
    commentaire_tuteur = models.TextField(verbose_name=u"Commentaires sur la conduite de l'activité",max_length=1000)
    validation_tuteur = models.BooleanField(default=False)
    derniere_modification = models.DateField(auto_now=True)
    class Meta:
        permissions = (
            ("can_propose_activite_entreprise", "Peut proposer une activité en entreprise"),
            ("can_see_all_activite_entreprise", "Peut voir toutes les activités en entreprises"),
            ("can_see_owned_activite_entreprise", "Peut voir ses propres activités en entreprise"),
        )
    
    def __unicode__(self):
        return (unicode(self.id)+"."+self.tache.nom)

class Competence_dans_activite(models.Model):
    PRATIQUE_CHOIX = (
        (0, u'Observation'),
        (1, u'Pratique assistée'),
        (2, u'Pratique en autonomie')
    )
    RESULTAT_CHOIX = (
        (0, u'Non'),
        (1, u'A peu près'),
        (2, u'Oui')
    )
    observable = models.BooleanField(default=False)
    competence = models.ForeignKey(Competence)
    activite_entreprise = models.ForeignKey(Activite_entreprise)
    donnees = models.TextField(verbose_name=u'Données pour réaliser la tâche (documents, logiciel...)')
    resultats = models.TextField(verbose_name=u'Résultats attendus (document, intervention dans un système...')
    pratique = models.IntegerField(choices=PRATIQUE_CHOIX, verbose_name=u'Pratique')
    resultat = models.IntegerField(choices=RESULTAT_CHOIX, verbose_name=u'Réussite')
    
    def __unicode__(self):
        return (unicode(self.activite_entreprise.id)+"."+self.competence.nom)


#Suite en projet - Non utilisé pour l'instant
'''class T_Activite_ufa(models.Model):
    formateur = models.ForeignKey(Formateur)
    titre = models.CharField(max_length=100, verbose_name = u'Titre de la séquence')
    titre_tache = models.ForeignKey(Tache, blank=True, verbose_name=u'Tâche (facultatif)')
    description = models.TextField(max_length=1000, verbose_name=u'Description')
    derniere_modif = models.DateField(auto_now=True)
    class Meta:
        permissions = (
            ("can_see_all_t_activite_ufa", "Can see all t_activite_ufa"),
            ("can_see_owned_t_activite_ufa", "Can see owned t_activite_ufa"),
        )
    
class T_Competence_dans_t_activite_ufa(models.Model):
    t_activite_ufa = models.ForeignKey(T_Activite_ufa)
    competence = models.ForeignKey(Competence)
    description = models.TextField(max_length=1000, blank=True)

class T_Savoir_dans_t_competence_ufa(models.Model):
    NIVEAUX_TAXO = (
        (1, u'Information'),
        (2, u'Expression'),
        (3, u"Maîtrise d'outils"),
        (4, u"Maîtrise méthodologique"),
    )
    savoir = models.ForeignKey(Savoir)
    t_competence_dans_t_activite_ufa = models.ForeignKey(T_Competence_dans_t_activite_ufa)
    niveau_cible = models.IntegerField(choices=NIVEAUX_TAXO)

class Activite_ufa(models.Model):
    formateur = models.ForeignKey(Formateur)
    apprenant = models.ForeignKey(Apprenant)
    date = models.DateField(verbose_name=u"Date de début de l'activité")
    titre = models.TextField(max_length=200, verbose_name=u"Titre de l'activité")
    description = models.TextField(max_length=1000, verbose_name=u"Description de l'activité")
    derniere_modif = models.DateField(auto_now=True)
    class Meta:
        permissions = (
            ("can_evaluate_activite_ufa", "Can evaluate activite_ufa"),
            ("can_see_all_activite_ufa", "Can see all activite_ufa"),
            ("can_see_owned_activite_ufa", "Can see owned activite_ufa"),
        )

class Competence_dans_activite_ufa(models.Model):
    REUSSITE_CHOIX = (
        (0, u'Non acquis'),
        (1, u"En cours d'acquisition"),
        (2, u"Acquis"),
    )
    activite_ufa = models.ForeignKey(Activite_ufa)
    competence = models.ForeignKey(Competence)
    description = models.TextField(max_length=1000, blank=True, verbose_name=u"Description (données, résultats attendus...)")
    reussite = models.IntegerField(choices=REUSSITE_CHOIX, verbose_name=u"Niveau d'acquisition")
    
class Savoir_dans_competence_ufa(models.Model):
    NIVEAUX_TAXO = (
        (1, u'Information'),
        (2, u'Expression'),
        (3, u"Maîtrise d'outils"),
        (4, u"Maîtrise méthodologique"),
    )
    savoir = models.ForeignKey(Savoir)
    competence_dans_activite_ufa = models.ForeignKey(Competence_dans_activite_ufa)
    niveau_cible = models.IntegerField(choices=NIVEAUX_TAXO, verbose_name=u"Niveau ciblé")'''
