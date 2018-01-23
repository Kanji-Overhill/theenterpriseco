from django.conf.urls import url
from . import views

urlpatterns = [
    ##  /
    url(r'^$', views.index, name='index'),
    #Login y Logout
    url(r'^login/$', views.login, name='login'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    ##Otras URLs staticas
    url(r'^rentals$', views.rentals, name='rentals'),
    url(r'^tenants$', views.tenants, name='tenants'),
    url(r'^forms$', views.forms, name='forms'),
    url(r'^maintenance$', views.maintenance, name='maintenance'),
    url(r'^move$', views.move, name='move'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^individual$', views.individual, name='individual'),
    url(r'^about$', views.about, name='about'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^thanks$', views.thanks, name='thanks'),
    # Administrativas
    url(r'^admin$', views.admin, name='admin'),
    url(r'^admin/building$', views.adminBuilding, name='admin_building'),
    url(r'^admin/department$', views.adminDepartment, name='adminDepartment'),
]