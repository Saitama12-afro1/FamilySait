from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import My_Roles, My_Room, My_Users, Type_Task, Task

admin.site.register(My_Roles)
admin.site.register(My_Room)
admin.site.register(My_Users, UserAdmin)
admin.site.register(Type_Task)
admin.site.register(Task)

