from django.urls import path
from . import views

app_name='family'
urlpatterns = [
    path('', views.index, name='index'),
    path('createFamily', views.Family_add, name="createFamily"),
    path('register', views.register, name="register"),
    path('login', views.my_login, name="login"),
    path('connect_family_key', views.connect_family_key, name="connect_family_key"),
    path('connect_family_pas', views.connect_family_pas, name="connect_family_pas"),
    path('room/<int:room_id>',views.room, name = "room")
]
