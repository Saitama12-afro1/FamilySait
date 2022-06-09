from django.db import models
from django.contrib.auth.models import AbstractUser

class My_Roles(models.Model):#Связь с юзер один ко многим
    name_role = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name_role
    
    class Meta:
        db_table = "my_roles"


class Type_Task(models.Model):
    my_type = models.CharField(max_length=100)
    
    
    class Meta:
        db_table = "my_type"
    
class My_Room(models.Model):
    name_room = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    generate_token = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name_room}"
    class Meta:
        db_table = "my_room"
    
class My_Users(AbstractUser):
    
    role = models.ForeignKey(My_Roles, on_delete=models.CASCADE, default=None)
    
    room = models.ManyToManyField(My_Room)
    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        db_table = "my_users"


class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_description =  models.TextField()
    
    type_task = models.ForeignKey(Type_Task, on_delete=models.CASCADE, default=None)
    
    id_user = models.ManyToManyField(My_Users)
    
        
    class Meta:
        db_table = "task"