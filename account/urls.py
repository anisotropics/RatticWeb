from django.conf.urls import patterns, url
from django.conf import settings
from views import profile, newapikey
from models import LDAPPassChangeForm

urlpatterns = patterns('',
    url(r'^profile/$', profile, {}),
    url(r'^newapikey/$', newapikey, {}),

    url(r'^login/$', 'django.contrib.auth.views.login', {
        'template_name': 'account_login.html'}),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '/'}),
)

# URLs we don't want enabled with LDAP
if not settings.LDAP_ENABLED:
    urlpatterns += (
        url(r'^reset/$', 'django.contrib.auth.views.password_reset', {
            'post_reset_redirect': '/account/reset/done/',
            'template_name': 'password_reset.html'
            }, name="password_reset"),

        url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done', {
            'template_name': 'password_reset_done.html'}),

        url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {
            'post_reset_redirect': '/',
            'template_name': 'password_reset_confirm.html'}),

        url(r'^changepass/$', 'django.contrib.auth.views.password_change', {
            'post_change_redirect': '/account/profile/',
            'template_name': 'account_changepass.html'})
    )

# URLs we do want enabled with LDAP
if settings.LDAP_ENABLED:
    urlpatterns += patterns('account.views',
        url(r'^changepass/$', 'django.contrib.auth.views.password_change', {
            'post_change_redirect': '/account/profile/',
            'template_name': 'account_changepass.html',
            'password_change_form': LDAPPassChangeForm})
    )
