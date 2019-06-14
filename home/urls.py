from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('take_note', views.take_note, name='take_note'),
    path('add_note', views.add_note, name='add_note'),
    path('edit_note/<nid>', views.edit_note, name='edit_note'),

    path('update_note', views.update_note, name='update_note'),

    path('delete_note', views.delete_note, name='delete_note'),
    path('signin', views.signin, name='signin'),

    path('logout', views.logout, name='logout'),
    path('index', views.index, name='index'),

]

