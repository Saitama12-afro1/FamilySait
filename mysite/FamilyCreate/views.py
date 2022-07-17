import django
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .forms import RegisterUser, LoginForm, RoomForm, ConPasForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from .models import My_Room, My_Users, My_Roles, Taken_User_Task, Task, Users_Room, Type_Task
from .create_token import generate_key
from django.http import Http404

# заменить все упоминания семьи на комнату(дико впадлу)

# при подключении к комнате добавляем ее к списку юзера, и  присваиваем юзеру роль пользователя,
# а создателю комнаты в момент ее созадния присваивается роль создателя текущей комнаты     


def index(request):
    user = request.user
    rooms_current_user_1 = Users_Room.objects.filter(id_user_id = user.id)
    rooms = []
    taken_task = Taken_User_Task.objects.filter(user_id = user.id)
    info_task = []
    for j in taken_task:
        task = Task.objects.get(id = j.task_id)
        info_task.append(task)
    for i in rooms_current_user_1:
        rooms.append(My_Room.objects.get(id = i.id_room_id))
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
    return render(request, "family/index.html",{"user": user,"rooms":rooms, "taken_task": info_task} )



def Family_add(request):#переиминовать в креате
    if request.method =='POST':
        create_form = RoomForm(request.POST)
        user = request.user
        if create_form.is_valid():#Сделать  хэширование пароля
            my_room = My_Room(name_room = create_form.cleaned_data["name_room"],
                                  password = create_form.cleaned_data["password"],generate_token=generate_key())
            
            my_room.save()
            users_room = Users_Room(creator_user = user.id, id_role_id = My_Roles.objects.get(id=2).id,id_room_id =my_room.id,id_user_id = user.id)
            users_room.save()


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
                room = My_Room.objects.get(generate_token = form_key)
                cretor_user = Users_Room.objects.get(id_room_id = room.id).creator_user
                if cretor_user != request.user.id:

                    users_room = Users_Room(creator_user = cretor_user, id_role_id = My_Roles.objects.get(id=1).id,id_room_id =room.id,
                                            id_user_id = request.user.id)
                    users_room.save()
                return HttpResponseRedirect(f'room/{room.id}')

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
                room = My_Room.objects.get(name_room = name_room)
                cretor_user = Users_Room.objects.get(id_room_id = room.id).creator_user
                if cretor_user != request.user.id:

                    users_room = Users_Room(creator_user = cretor_user, id_role_id = My_Roles.objects.get(id=1).id,id_room_id =room.id,
                                            id_user_id = request.user.id)
                    users_room.save()
                return HttpResponseRedirect(f'room/{room.id}')
    else:
        form = ConPasForm()
    return render(request, "family/connect_family_pas.html", {"form":form, "my_room_exist":my_room_exist})


def room(request, room_id):
    room = get_object_or_404(My_Room, id = room_id)
    users_room = Users_Room.objects.filter(id_room_id=room_id)
    name_users_in_room = []
    
    task_all = Task.objects.filter(id_room = room_id)
    if request.method == "POST":
        if "form1" in request.POST:
            print(dict(request.POST.lists()))
            type_form = TaskForm(request.POST)
            if type_form.is_valid():
                task_title = type_form.cleaned_data["task_title"]
                task_description = type_form.cleaned_data["task_description"]
                task_type =  type_form.cleaned_data["type_task"]
                task = Task(task_title=task_title, task_description=task_description, 
                            id_room = My_Room.objects.get(id = room_id), type_task=Type_Task.objects.get(my_type = task_type))
                task.save()
                user = request.user
                user.task_set.add(task)            
                return HttpResponseRedirect(f"{room_id}")
        elif "form2" in request.POST:
            print(request.POST["id_task"])
            task = Task.objects.get(pk = int((request.POST["id_task"])))
            take_task = Taken_User_Task(user = request.user, task = task)
            Task.objects.filter(pk = int((request.POST["id_task"]))).update(active = False)
            take_task.save()
            type_form = TaskForm()
            return HttpResponseRedirect(f"{room_id}")                            
    else :
        type_form = TaskForm()
    for i in users_room:
        name_users_in_room.append(My_Users.objects.get(id = i.id_user_id))
    
    return render(request, "family/room.html",{"room":room,"name_users_in_room":name_users_in_room, "form":type_form,"task_all":task_all})