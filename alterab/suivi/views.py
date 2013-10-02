# coding=UTF-8
from suivi.forms import *
from django.http import Http404
#from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from suivi.models import Activite_entreprise, Competence_dans_activite
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from suivi.utils import *
from django.views.generic import list_detail
from django.core.mail import send_mail


@login_required
def liste_activite(request):
    #import pdb; pdb.set_trace()
    if request.user.has_perm('suivi.can_see_all_activite_entreprise'):
        activite_entreprise = Activite_entreprise.objects.filter()
    else:
        if role_user(request.user)==1:
            activite_entreprise = Activite_entreprise.objects.filter(apprenti__utilisateur_extend__user = request.user)
        elif role_user(request.user)==2:
            activite_entreprise = Activite_entreprise.objects.filter(apprenti__tuteur_entreprise__utilisateur_extend__user = request.user)
        else:
            return render_message(request, message="Accès non authorisé")
    c = {'activite_entreprise': activite_entreprise}
    #c.update(csrf(request))
    return render_to_response('suivi/liste_activite.html', c, context_instance=RequestContext(request))

@login_required
def ajout_activite(request, id_activite=0):
    # on vérifie qui est l'utilisateur et on donne la bonne form pour ajouter ou proposer une activité
    if request.user.has_perm('suivi.add_activite_entreprise'):
        Activite_entreprise_form = Activite_entreprise_form_tuteur
    elif request.user.has_perm('suivi.can_propose_activite_entreprise'):
        Activite_entreprise_form = Activite_entreprise_form_apprenti
    else :
        return render_message(request, message="Accès non authorisé")
    
    #un post arrive
    if request.method == 'POST':
        action = request.POST.get('action')
        tache = request.POST.get('tache')
        
        # on vérifie qu'une tâche est sélectionné
        if tache=="":
            activite_entreprise_form = Activite_entreprise_form(request.POST, query=request.user)
            competence_dans_activite_formset=""
        else:
            # on prend la tâche dans la bd et les compétences associées en les comptant
            e = Tache.objects.get(id=tache)
            n = e.competences.count()
            coms = e.competences.all()
            Competence_dans_activite_formset = formset_factory (Competence_dans_activite_form, extra=0)
            z=n*[""]
            
            # il y a juste une tâche de sélectionnée
            if action == 'select':
                # une form est préparée avec le nombre de compétences adéquat
                activite_entreprise_form = Activite_entreprise_form(request.POST, error_class=No_error_list, query=request.user)
                competence_dans_activite_formset = Competence_dans_activite_formset(initial=z)
                for i in range(n):
                    competence_dans_activite_formset[i].titre=coms[i]
                    
            # l'utilisateur a posté une form complète
            else :
                # on récupère l'id_activite (0 si c'est une nouvelle entrée, un autre chiffre si c'est une entrée modifiée
                if id_activite==0:
                    try:
                        id_activite=request.session.get('id')
                    except:
                        pass
                
                # Si c'est une nouvelle entrée, on intègre dans une form vierge les données entrée par l'utilisateur
                if id_activite==0:
                    activite_entreprise_form = Activite_entreprise_form(request.POST ,query=request.user)
                    competence_dans_activite_formset=Competence_dans_activite_formset(request.POST, initial=z)
                
                #sinon on associe les nouvelles entrées avec la form associée au modèle modifié
                else:
                    activite = Activite_entreprise.objects.get(pk=id_activite)
                    activite_entreprise_form = Activite_entreprise_form(request.POST, query=request.user, instance=activite)
                    Competence_dans_activite_formset = modelformset_factory (Competence_dans_activite, form = Competence_dans_activite_form, extra=0)
                    comas = Competence_dans_activite.objects.filter(activite_entreprise=activite)
                    competence_dans_activite_formset = Competence_dans_activite_formset(request.POST, queryset=comas)
                for i in range(n):
                    competence_dans_activite_formset[i].titre=coms[i]
                    
                # On vérifie que la form est valide
                #import pdb; pdb.set_trace()
                if activite_entreprise_form.is_valid() and competence_dans_activite_formset.is_valid():
                    # on récupère les données
                    data_activite = activite_entreprise_form.save(commit=False)
                    # on valide ou non l'activité suivant les permissions
                    if request.user.has_perm('suivi.add_activite_entreprise'):
                        data_activite.validation_tuteur = True
                    elif request.user.has_perm('suivi.can_propose_activite_entreprise'):
                        data_activite.apprenant = request.user.utilisateur_extend.apprenti
                        data_activite.validation_tuteur = False
                    # on enregistre l'activité dans la bd...
                    data_activite.save()
                    activite_entreprise_form.save_m2m()
                    # ...et les compétences associées
                    for i in range(n):
                        data=competence_dans_activite_formset[i].save(commit=False)
                        data.activite_entreprise = data_activite
                        data.competence = coms[i]
                        data.save()
                        competence_dans_activite_formset[i].save_m2m()
                    # on envoie un email au tuteur d'entreprise car une activité a été proposé par son apprenti
                    if request.user.has_perm('suivi.can_propose_activite_entreprise'):
                        msg = u'Bonjour,\n\nVotre apprenti, ' + request.user.first_name + u' ' + request.user.last_name + u", a décrit une activité. Votre validation est nécessaire.\nA l'adresse " + u"http://" + request.META['HTTP_HOST'] + u"/activite/liste/ , vous pourrez visualiser toutes les activités décrites.\nCliquez sur les activités à fond rouge, modifiez les champs si vous jugez que votre apprenti a mal décrit son activité, ajoutez un commentaire tout en bas et validez.\n\nMerci"
                        send_mail(u'Activité proposée par votre apprenti', msg, 'django@abriand.info',[request.user.utilisateur_extend.apprenti.tuteur_entreprise.utilisateur_extend.user.email], fail_silently=False)
                    # on redirige vers une page de merci
                    return render_message(request, message="Merci")
                    
    # cette page est appelée sans post
    else:
        # c'est pour un ajout, on prépare une form vierge
        if id_activite==0:
            activite_entreprise_form = Activite_entreprise_form(query=request.user)
            competence_dans_activite_formset=""
            request.session['id']=0  
               
        # c'est une modification, on prépare une form remplie
        else:
            #import pdb; pdb.set_trace()
            activite = Activite_entreprise.objects.get(pk=id_activite)
            activite_entreprise_form = Activite_entreprise_form(query=request.user, instance=activite)
            data=activite_entreprise_form.save(commit=False)
            request.session['id']=data.id
            Competence_dans_activite_formset = modelformset_factory (Competence_dans_activite, form = Competence_dans_activite_form, extra=0)
            comas = Competence_dans_activite.objects.filter(activite_entreprise=activite)
            competence_dans_activite_formset = Competence_dans_activite_formset(queryset=comas)
            e = activite.tache
            n = e.competences.count()
            coms = e.competences.all()
            for i in range(n):
                competence_dans_activite_formset[i].titre=coms[i]
    
    # on envoie vers le template
    c = {'activite_entreprise_form': activite_entreprise_form, 'competence_dans_activite_formset': competence_dans_activite_formset}
    #c.update(csrf(request))
    return render_to_response('suivi/ajout_activite.html', c, context_instance=RequestContext(request))


@login_required
def activite_consultation(request, num):
    try:
        activite = Activite_entreprise.objects.get(pk=int(num))
    except:
        raise Http404
        
    if request.user.has_perm('suivi.can_see_all_activite_entreprise'):
        pass
    elif role_user(request.user)==1:
        if (activite.apprenti.utilisateur_extend.user != request.user):
            return render_message(request, message="Accès non authorisé")
    elif role_user(request.user)==2:
        if (activite.apprenti.tuteur_entreprise.utilisateur_extend.user != request.user):
            return render_message(request, message="Accès non authorisé")
    else:
        return render_message(request, message="Accès non authorisé")
            
    competence = Competence_dans_activite.objects.filter(activite_entreprise=activite)
    apprenti = activite.apprenti
    
    return list_detail.object_list(
        request,
        queryset = Activite_entreprise.objects.filter(pk=int(num)),
        template_name = "suivi/activite_consultation.html",
        extra_context = {"competence" : competence, "apprenti" : apprenti}
    )

'''@login_required
def ajout_sequence(request, id_activite=0):
    if not request.user.has_perm('suivi.add_t_activite_ufa'):
        return render_message(request, message="Accès non authorisé")
    if request.method == "POST":
        pass
    else:
        # c'est pour un ajout, on prépare une form vierge
        if id_activite==0:
            t_activite_ufa_form = T_Activite_ufa_form()
            request.session['id']=0  
        
    # on envoie vers le template
    competence = Competence.objects.all()
    c = {'t_activite_ufa_form': t_activite_ufa_form, 'competence' : competence}
    #c.update(csrf(request))
    return render_to_response('suivi/ajout_sequence.html', c, context_instance=RequestContext(request))'''

#def csrf_failure(request, reason="csrf_failure"):
#    return render_message(request, message="Vous devez authoriser les cookies pour utiliser ce site.")
