from django.conf.urls.defaults import *
from django.views.generic.simple  import direct_to_template
from django.views.generic.simple import redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    (r'^activite/', include('suivi.urls')),
    (r'^$', 'home.views.accueil'),
    (r'textes/', include('home.urls')),
    (r'calendrier/', login_required(direct_to_template), {'template': 'home/calendrier.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^comptes/', include('registration.urls')),
    #(r'^comptes/profile/$', direct_to_template, {'template': 'registration/profile.html'}),
    #(r'^comptes/profile/edit/$', direct_to_template, {'template': 'registration/profile_form.html'}),
)

urlpatterns = urlpatterns  + patterns('',
   url(r'^comptes/login/$',
       auth_views.login,
       {'template_name': 'registration/login.html'},
       name='auth_login'),
   url(r'^comptes/logout/$',
       auth_views.logout,
       {'template_name': 'registration/logout.html'},
       name='auth_logout'),
   url(r'^comptes/password_change/$',
       auth_views.password_change,
       name='auth_password_change'),
   url(r'^comptes/password/change/done/$',
       auth_views.password_change_done,
       name='auth_password_change_done'),
   url(r'^comptes/password/reset/$',
       auth_views.password_reset,
       name='auth_password_reset'),
   url(r'^comptes/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       name='auth_password_reset_confirm'),
   url(r'^comptes/password/reset/complete/$',
       auth_views.password_reset_complete,
       name='auth_password_reset_complete'),
   url(r'^comptes/password/reset/done/$',
       auth_views.password_reset_done,
       name='auth_password_reset_done'),
)

