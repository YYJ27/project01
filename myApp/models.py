from django.db import models

# Create your models here.
class User(models.Model):                              #创建数据表单，用户名，密码，并限制最大字符串长度
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=100)
    dateTime = models.DateTimeField(auto_now_add=True,null=True)
    user_type = models.CharField(max_length=100,default='电站业主')
    user_state = models.CharField(max_length=100, default='有效')
    def __str__(self):
        return self.username

class Mapmessage(models.Model):
    Flong = models.CharField(max_length = 100)
    Flati = models.CharField(max_length = 100)
    Address = models.CharField(max_length = 100)
    Daily_output = models.CharField(max_length = 100)
    Total_output = models.CharField(max_length = 100)
    Out_power = models.CharField(max_length = 100)
    Error = models.CharField(max_length = 50)
    def __str__(self):
        return self.Flong

class Class(models.Model):
    title = models.CharField(max_length = 20)
    def __str__(self):
        return self.title

class Teacher(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class student(models.Model):
    stu_name = models.CharField(max_length = 50)
    class_id = models.ForeignKey("Class", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class facility(models.Model):
    name_n = models.CharField(max_length = 100)
    name_sn = models.CharField(max_length = 100)
    name_pn = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    protocol = models.CharField(max_length = 100)
    belong_p = models.CharField(max_length = 100)
    belong_o = models.CharField(max_length=100)

    def __str__(self):
        return self.name_n












