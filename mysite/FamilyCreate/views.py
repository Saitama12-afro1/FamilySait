import django
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .forms import RegisterUser, LoginForm, RoomForm, ConPasForm
from django.contrib.auth import authenticate, login, logout
from .models import My_Room, My_Users, My_Roles
from .create_token import generate_key
from django.http import Http404

# заменить все упоминания семьи на комнату(дико впадлу)

# при подключении к комнате добавляем ее к списку юзера, и  присваиваем юзеру роль пользователя,
# а создателю комнаты в момент ее созадния присваивается роль создателя текущей комнаты     


def index(request):
    user = request.user
    rooms_current_user = My_Users.objects.get(id = user.id).room.all()
    if request.method == 'POST':
        for i in request.POST:
            if request.POST[i] == "Выйти":
                logout(request)
                return HttpResponseRedirect('/')
            else:
                if request.POST[i] == "1":
                    return HttpResponseRedirect('/connect_family_key')
                elif request.POST[i] == "2":
                    return HttpResponseRedirect('/connect_family_pas')
    return render(request, "family/index.html",{"user": user,"rooms_current_user":rooms_current_user} )



def Family_add(request):
    if request.method =='POST':
        create_form = RoomForm(request.POST)
        user = request.user
        if create_form.is_valid():#Сделать  хэширование пароля
            my_room = My_Room(name_room = create_form.cleaned_data["name_room"],
                                  password = create_form.cleaned_data["password"],generate_token=generate_key())
            
            my_room.save()
            user.room.add(my_room)


            return HttpResponseRedirect("/")
    else:
        create_form = RoomForm()
    return render(request, "family/create_family.html",{"form":create_form})


def register(request):
    if request.method == 'POST':
        user_form = RegisterUser(request.POST)
        
        if  user_form.is_valid():

            user = My_Users(email = user_form.cleaned_data["email"],
                                            first_name=user_form.cleaned_data["first_name"],
                                            last_name=user_form.cleaned_data["last_name"], 
                                             
                                            role = My_Roles.objects.get(id = 1),
                                            username=user_form.cleaned_data['username'])
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            return HttpResponseRedirect("/")
        else:
            
            return HttpResponseRedirect("/register")
    else:
        user_form = RegisterUser()
    
    return render(request,"family/register.html",{"form":user_form})

def my_login(request):
    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, "family/login.html",{"form":form})


def connect_family_key(request):#при подключении добавляем комнату к юзеру, если эта комнаат не его 
    my_room_exist = True
    if request.method == "POST":
        form_key = request.POST["key"]
        my_room_on_key = My_Room.objects.filter(generate_token = form_key)
        if len(my_room_on_key) == 0:
            my_room_exist = False
        else:
                a = My_Room.objects.get(generate_token = form_key)
                return HttpResponseRedirect(f'room/{a.id}')

    return render(request, "family/connect_family_key.html", {"my_room_exist":my_room_exist})


def connect_family_pas(request):
    my_room_exist = True
    if request.method == "POST":
        form = ConPasForm(request.POST)
        if form.is_valid():
            name_room = form.cleaned_data["name_room"]
            password = form.cleaned_data["password"]
            if  len(My_Room.objects.filter(name_room = name_room)) == 0 or len(My_Room.objects.filter(password=password)) == 0:
                my_room_exist = False
            else:
                a = My_Room.objects.get(name_room = name_room)
                
                return HttpResponseRedirect(f'room/{a.id}')
    else:
        form = ConPasForm()
    return render(request, "family/connect_family_pas.html", {"form":form, "my_room_exist":my_room_exist})


def room(request, room_id):
    room = get_object_or_404(My_Room, id = room_id)
    return render(request, "family/room.html",{"room":room})