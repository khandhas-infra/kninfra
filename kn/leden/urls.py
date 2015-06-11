from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from kn.leden import views, api

urlpatterns = [
    url(r'^$',
    login_required(TemplateView.as_view(template_name='leden/home.html')),
               name='smoelen-home'),
    url(r'^gebruikers/(?:p/(?P<page>[0-9]+)/)?$',
        views.user_list, name='user-list'),
    url(r'^naamdrager/(?P<name>[^/]+)/$',
        views.entity_detail, name='entity-by-name'),
    url(r'^id/(?P<_id>[^/]+)/$',
        views.entity_detail, name='entity-by-id'),
    url(r'^gebruiker/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'user'}, name='user-by-name'),
    url(r'^gebruiker/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'user'}, name='user-by-id'),
    url(r'^gebruiker/id/(?P<_id>[^/]+)/reset-wachtwoord$',
        views.user_reset_password, name='user-reset-password'),
    url(r'^groep/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'group'}, name='group-by-name'),
    url(r'^groep/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'group'}, name='group-by-id'),
    url(r'^brand/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'brand'}, name='brand-by-name'),
    url(r'^brand/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'brand'}, name='brand-by-id'),
    url(r'^stempel/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'tag'}, name='tag-by-name'),
    url(r'^stempel/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'tag'}, name='tag-by-id'),
    url(r'^studie/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'tag'}, name='study-by-name'),
    url(r'^studie/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'study'}, name='study-by-id'),
    url(r'^instituut/(?P<name>[^/]+)/$',
        views.entity_detail, {'type': 'institute'},
        name='institute-by-name'),
    url(r'^instituut/id/(?P<_id>[^/]+)/$',
        views.entity_detail, {'type': 'institute'},
        name='institute-by-id'),
    url(r'^bouwjaar/$',
        views.years_of_birth, name='years-of-birth'),
    url(r'^bouwjaar/(?P<year>\d+)/$',
        views.entities_by_year_of_birth, name='entities-by-year-of-birth'),
    url(r'^smoel/(?P<name>[^.]+).jpg$',
        views.user_smoel, name='user-smoel'),
    url(r'^geenalcohol/$',
        views.users_underage, name='users-underage'),
    url(r'^ik', views.ik, name='ik'),
    url(r'^ik/wachtwoord$', views.ik_chpasswd, name="chpasswd"),
    url(r'^ik/wachtwoord/villanet/$', views.ik_chpasswd_villanet,
        name="chpasswd-villanet"),
    url(r'^ik/smoel$', views.ik_chsmoel, name="ik-chsmoel"),
    url(r'^api/users$', views.api_users),
    url(r'^api/?$', api.view, name='leden-api'),
    url(r'^ik/openvpn/$', views.ik_openvpn, name="ik-openvpn"),
    url(r'^ik/openvpn/(?P<filename>.+(exe|zip))$', views.ik_openvpn_download,
                name="ik-openvpn-download"),
    url(r'^secretariaat/inschrijven$',
        views.secr_add_user, name='secr-add-user'),
    url(r'^secretariaat/update-site-agenda/$',
        views.secr_update_site_agenda, name='secr-update-site-agenda'),
    url(r'^secretariaat/addgroup$',
        views.secr_add_group, name='secr-add-group'),
    url(r'^secretariaat/notes$',
        views.secr_notes, name='secr-notes'),
    url(r'^relaties/(?P<_id>[^/]+)/beindig$',
        views.relation_end, name='relation-end'),
    url(r'^relaties/begin$',
        views.relation_begin, name='relation-begin'),
    url(r'^noteer$',
        views.note_add, name='add-note'),

    # style
    url(r'^styles/leden/$',
        TemplateView.as_view(template_name='leden/base.css',
                             content_type='text/css'), name='leden-base'),
        ]

# vim: et:sta:bs=2:sw=4:
