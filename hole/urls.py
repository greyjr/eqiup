from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^tax/', views.tax, name="tax"),
    url(r'^one_more/', views.one_more, name="one_more"),
    url(r'^reset_new/', views.reset_new, name='reset_new'),
    url(r'^reset_review/', views.reset_review, name='reset_review'),
    url(r'^resume/', views.resume, name='resume'),
    url(r'^analysis/', views.analysis, name='analysis'),
    url(r'^ie/', views.ie_temp, name="ie_temp"),
    url(r'^FAQ/', views.faq, name='faq'),
    url(r'^krz/', views.krz, name='krz'),
    path('delete/<int:idi>', views.delete, name='delete'),
    path('edit/<int:idi>/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('rewrite/', views.rewrite, name='rewrite'),
    path('analysis_unit/', views.analysis_unit, name='analysis_unit')

]
