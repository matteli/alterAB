# coding=UTF-8
from django.db import models
from django import forms
from django.forms import ModelForm, DateInput, TypedChoiceField
from django.forms.formsets import *

from suivi.models import *


class Activite_entreprise_form_apprenti(ModelForm):
    action = forms.CharField(widget=forms.HiddenInput)
    nom_bouton = "Soumettre"
    def __init__(self,*args,**kwrds):
        self.query = kwrds['query']
        del kwrds['query']
        super(Activite_entreprise_form_apprenti,self).__init__(*args,**kwrds)
    class Meta:
        model = Activite_entreprise
        exclude = ('validation_tuteur','commentaire_tuteur', 'apprenti',)

class Activite_entreprise_form_tuteur(ModelForm):
    action = forms.CharField(widget=forms.HiddenInput)
    nom_bouton = "Valider"
    def __init__(self,*args,**kwrds):
        self.query = kwrds['query']
        del kwrds['query']
        super(Activite_entreprise_form_tuteur,self).__init__(*args,**kwrds)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['apprenti'].required = False
            self.fields['apprenti'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['apprenti'].queryset = Apprenti.objects.filter(tuteur_entreprise__utilisateur_extend__user=self.query)
    def clean_apprenti(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.apprenti
        else:
            return self.cleaned_data.get('apprenti', None)
   
    class Meta:
        model = Activite_entreprise
        exclude = ('validation_tuteur',)
	
class Competence_dans_activite_form(ModelForm):
    titre="titre"
    def __init__(self, *args, **kwargs):
        super(Competence_dans_activite_form, self).__init__(*args, **kwargs)
        self.fields['observable'].widget.attrs['class'] = 'class_observable'
    class Meta:
        model = Competence_dans_activite
        exclude = ('activite_entreprise', 'competence',)
    def clean(self):
        from django.core.exceptions import ValidationError
        cleaned_data = self.cleaned_data
        obs = cleaned_data.get('observable', None)
        if obs==False:
            cleaned_data['donnees']=u'Pas de données'
            cleaned_data['resultats']=u'Pas de résultats'
            cleaned_data['pratique']=0
            cleaned_data['resultat']=0
            try:
                del self.errors['donnees']
            except:
                pass
            try:
                del self.errors['resultats']
            except:
                pass
            try:
                del self.errors['pratique']
            except:
                pass
            try:
                del self.errors['resultat']
            except:
                pass
                
        #import pdb; pdb.set_trace()
        return cleaned_data

'''class T_Activite_ufa_form(ModelForm):
    class Meta:
        model = T_Activite_ufa
        exclude = {'formateur'}
        
class T_Competence_dans_t_activite_ufa_form(ModelForm):
    class Meta:
        model = T_Competence_dans_t_activite_ufa
        exclude = {'t_activite_ufa'}
        
class T_Savoir_dans_t_competence_ufa_form(ModelForm):
    class Meta:
        model = T_Savoir_dans_t_competence_ufa
        exclude = {'t_competence_dans_t_activite_ufa'}'''
