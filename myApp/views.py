from django.shortcuts import render,render_to_response,redirect
from django.http import  HttpResponse,HttpResponseRedirect
import json
from django import forms
from myApp.models import User
from myApp.models import facility
from myApp.models import Mapmessage
from django.http import JsonResponse
from django.core import serializers
from myApp.models import Class
from myApp.models import Teacher
import pymysql
from utils import sqlheper
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.paginator import Paginator,Page

class UserForm(forms.Form):
    username = forms.CharField(label = '用户名',max_length= 100)
    password = forms.CharField(label = '密码',widget= forms.PasswordInput())

class RegistForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    Email = forms.CharField(label='电子邮件',widget=forms.EmailInput())
    phone = forms.CharField(label='电话')

def xinxi(request):
    return render(request, 'myApp/xinxi.html')

def gaode(request):
    return render(request, 'myApp/gaode.html')

def gaode1(request):
    return render(request, 'myApp/gaode1.html')

def xiala(request):
    return render(request, 'myApp/xiala.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def regist(request):
    if request.method == 'POST':
        rf = RegistForm(request.POST)
        if rf.is_valid():
            #获得表单数据
            #username = request.POST.get('username')
            username = rf.cleaned_data['username']
            password1 = rf.cleaned_data['password1']
            password2 = rf.cleaned_data['password2']
            Email = rf.cleaned_data['Email']
            phone = rf.cleaned_data['phone']
            if password1 != password2:
                message='两次输入密码不一致！'
                return render_to_response('myApp/regist.html',{"message":message})
            else:
                same_name_user = User.objects.filter(username = username)
                if same_name_user:
                    message ="用户名已存在"
                    return render_to_response('myApp/regist.html', {"message":message})
                same_Email_user = User.objects.filter(Email=Email)
                if same_Email_user:
                    message='邮箱已被注册！'
                    return render_to_response('myApp/regist.html', {"message":message})
                same_phone_user = User.objects.filter(phone=phone)
                if same_phone_user:
                    message = '电话已被注册！'
                    return render_to_response('myApp/regist.html', {"message":message})
                #创建新用户，添加到数据库
                new_user = User.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.Email = Email
                new_user.phone = phone
                new_user.save()
                message = '注册成功，请登陆'
                return render_to_response('myApp/regist.html', {"message": message})
    else:
        rf = RegistForm()
        return render_to_response('myApp/regist.html', {'rf':rf})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            #username = request.POST.get('username')
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username=username,password=password)    #User.objects.get(id=1).字段名   获取表单中id=1的字段名的数据，返回单条
            if user:                                                           #User.objects.filter( username=...).order_by('?')[:4]  随机返回4条数据
                #比较成功，跳转
                #response = HttpResponseRedirect('/test/')
                #将username写入浏览器cookie,失效时间为3600
                request.session['user_info'] = { 'username': username}
                #response.set_cookie('username',username,3600)                #cookie操作
                return redirect('/test/')
            else:
                #比较失败，还在login
                message = "用户名或密码错误，请重新登陆"
                return render(request,'myApp/login.html',{"message": message})
               #return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('myApp/login.html',{'uf':uf},)

def logout(request):
    if request.session.get('user_info'):
        request.session.delete(request.session.session_key)    #删除数据库里的数据
        #request.session.clear()  # 超时时间为0,删除缓存中的cookie
    return redirect('/login/')

def classes(request):          #注意，app名字不能与表名重复
    conn = pymysql.connect(host = '127.0.0.1',port = 3306 ,user='root',password='667596',db="data1",charset="utf8")# 连接database
    cursor = conn.cursor( cursor = pymysql.cursors.DictCursor )   # 得到一个可以执行SQL语句的光标对象
    cursor.execute("select id,title from myapp_Class")   # 执行SQL语句
    class_list = cursor.fetchall()     #获取数据传递给此变量
    cursor.close()        # 关闭光标对象
    conn.close()       # 关闭数据库连接
    return render(request, 'myApp/classes.html',{"class_list":class_list})

from utils.pager import PageInfo1
def shebei(request):
    all_count = facility.objects.all().count()  # 取该数据的总条数,取数据小于22条,用于显示分页

    page_info = PageInfo1(request.GET.get("page"), all_count, 6, '/shebei',5)  # 10:10条数据   11：11个页码，current_page = request.GET.get("page")    获取当前页
    shebei_list = facility.objects.all()[page_info.start():page_info.end()]  # 调用类获取数据
    return render(request, 'myApp/shebei.html', {"shebei_list": shebei_list, 'page_info': page_info})

def shebei_jicheng(request):
    shebei_list = facility.objects.all()
    return render(request, 'myApp/shebei_jicheng.html', {"shebei_list": shebei_list})

def modal_edit_shebei(request):
    ret = {'status': True, 'message': None}
    try:
        name_n = request.POST.get('name_n')
        name_sn = request.POST.get('name_sn')
        name_pn = request.POST.get('name_pn')
        state = request.POST.get('state')
        protocol = request.POST.get('protocol')
        belong_p = request.POST.get('belong_p')
        belong_o = request.POST.get('belong_o')
        nid = request.POST.get('nid')
       # sqlheper.modify('update myapp_facility set name_n=%s,name_sn=%s,name_pn=%s,state=%s,protocol=%s,belong_p=%s,belong_o=%s, where id=%s', [name_n,name_sn,name_pn,state,protocol,belong_p,belong_o, nid,])
        update_shebei = facility.objects.filter(id=nid).update(name_n=name_n, name_sn=name_sn, name_pn=name_pn, state=state, protocol=protocol, belong_p=belong_p, belong_o=belong_o)
        update_shebei.save()
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    import json
    return HttpResponse(json.dumps(ret))

def modal_add_shebei(request):
    # 获取html页面中数据
    name_n = request.POST.get('name_n')
    name_sn = request.POST.get('name_sn')
    name_pn = request.POST.get('name_pn')
    state = request.POST.get('state')
    protocol = request.POST.get('protocol')
    belong_p = request.POST.get('belong_p')
    belong_o = request.POST.get('belong_o')
    # 判断输入数据是否为空
    if len(name_n) > 0 and len(name_sn) > 0 and len(name_pn) > 0 and len(state) > 0 and len(protocol) > 0 and len(belong_p) > 0 and len(belong_o) > 0:
        #更新数据库信息
        facility.objects.create(name_n = name_n,name_sn = name_sn,name_pn = name_pn,state = state,protocol = protocol,belong_p = belong_p,belong_o = belong_o)

        return HttpResponse('ok')
    else:
        return HttpResponse("内容不能为空")

def delshebei(request):
    nid = request.GET.get('nid')
    facility.objects.filter(id=nid).delete()
    return redirect('/shebei/')

#########################对话框

def modal_add_class(request):
    title = request.POST.get('title')         #获取classes页面中title数据
    if len(title) > 0:                         #判断数据是否为空
        sqlheper.modify("insert into myapp_class(title) values(%s)", [title, ])         #将拿到的数据添加到数据库
        return HttpResponse('ok')
        #return redirect("/classes/")
    else:
        return HttpResponse("标题不能为空")

def addclass(request):
    if request.method=="GET":
        return render(request, 'myApp/addclass.html')
    else:
        print(request.POST)
        v = request.POST.get('title')   #获得前端传来数据
        if len(v)>0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
            cursor.execute("insert into myapp_Class(title) values(%s)",[v,])  # 执行SQL语句，添加数据到title
            conn.commit()   #提交到数据库
            cursor.close()  # 关闭光标对象
            conn.close()    #关闭数据库
            return redirect('/classes/')    #提交成功进行页面跳转
        else :
            return render(request,"myApp/addclass.html",{"msg":"班级不能为空"})

def modal_edit_class(request):
    ret = {'status':True,'message':None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlheper.modify('update myapp_class set title=%s where id=%s',[content,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    import json
    return HttpResponse(json.dumps(ret))

def delclass(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute("delete from myapp_Class where id=%s", [nid, ])  # 执行SQL语句，删除数据
    conn.commit()  # 提交到数据库
    cursor.close()  # 关闭光标对象
    conn.close()
    return redirect('/classes/')

def editclass(request):
    if request.method == "GET":
        nid = request.GET.get('nid')     #拿到html表单提交的数据nid
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("select id,title from myapp_Class where id=%s", [nid, ])  #查询数据
        result = cursor.fetchone()     #result就是拿到数据库此数据
        cursor.close()  # 关闭光标对象
        conn.close()
        print(result)
        return render(request, 'myApp/editclass.html',{'result':result})       #将拿到的数据进行渲染页面
    else:
        nid = request.GET.get("nid")    #注意是get请求
        title = request.POST.get("title")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("update myapp_Class set title=%s where id=%s", [title, nid])  # 执行SQL语句，更新数据
        conn.commit()   #提交
        cursor.close()  # 关闭光标对象
        conn.close()

        return redirect("/classes/")

def teacher(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute("select id,name from myapp_teacher")  # 执行SQL语句
    teacher_list = cursor.fetchall()  # 获取数据传递给此变量
    cursor.close()  # 关闭光标对象
    conn.close()
    return render(request, 'myApp/teacher.html',{"teacher_list":teacher_list})

def addteacher(request):
    if request.method=="GET":
        return render(request, 'myApp/addteacher.html')
    else:
        print(request.POST)
        v = request.POST.get('name')   #获得前端传来数据
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("insert into myapp_teacher(name) values(%s)",[v,])  # 执行SQL语句，添加数据到title
        conn.commit()   #提交到数据库
        cursor.close()  # 关闭光标对象
        conn.close()    #关闭数据库
        return redirect('/teacher/')    #提交成功进行页面跳转

def delteacher(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute("delete from myapp_teacher where id=%s", [nid, ])  # 执行SQL语句，删除数据
    conn.commit()  # 提交到数据库
    cursor.close()  # 关闭光标对象
    conn.close()
    return redirect('/teacher/')

def editteacher(request):
    if request.method == "GET":
        nid = request.GET.get('nid')  # 拿到html表单提交的数据nid
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("select id,name from myapp_teacher where id=%s", [nid, ])  # 查询数据
        result = cursor.fetchone()  # result就是拿到数据库此数据
        cursor.close()  # 关闭光标对象
        conn.close()
        print(result)
        return render(request, 'myApp/editteacher.html', {'result': result})  # 将拿到的数据进行渲染页面
    else:
        nid = request.GET.get("nid")  # 注意是get请求
        name = request.POST.get("name")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("update myapp_teacher set name=%s where id=%s", [name, nid])  # 执行SQL语句，更新数据
        conn.commit()  # 提交
        cursor.close()  # 关闭光标对象
        conn.close()

        return redirect("/teacher/")

def students(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",                     charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    #从数据库查询班级和学生的信息，注意如何关联
    cursor.execute("select myapp_student.id,myapp_student.stu_name,myapp_student.class_id_id,myapp_class.title from myapp_student left JOIN myapp_class on myapp_student.class_id_id = myapp_class.id")  # 执行SQL语句，更新数据
    student_list = cursor.fetchall()
    cursor.close()  # 关闭光标对象
    conn.close()
    class_list = sqlheper.get_list('select id,title from myapp_class',[])

    return render(request,'myApp/students.html',{"student_list":student_list,'class_list':class_list})

def modal_add_student(request):
    ret = {'status':True,'message':None}
    try:
        stu_name = request.POST.get('name')
        class_id_id = request.POST.get('class_id')
        sqlheper.modify('insert into myapp_student(stu_name,class_id_id) values(%s,%s)',[stu_name,class_id_id,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        stu_name = request.POST.get('name')
        class_id_id = request.POST.get('class_id')
        sqlheper.modify('update myapp_student set stu_name=%s,class_id_id=%s where id=%s', [stu_name,class_id_id,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


def addstudent(request):
    if request.method =="GET":     #从数据库获取数据
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("select id,title from myapp_Class")  # 执行SQL语句
        class_list = cursor.fetchall()  # 获取数据传递给此变量
        cursor.close()  # 关闭光标对象
        conn.close()
        return render(request, 'myApp/addstudent.html',{"class_list":class_list})
    else:     #提交数据到数据库
        stu_name = request.POST.get("stu_name")
        class_id_id = request.POST.get("class_id_id")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
        cursor.execute("insert into myapp_student(stu_name,class_id_id) values(%s,%s)",[stu_name,class_id_id])  # 执行SQL语句
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()
        return redirect("/students/")

def editstudent(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        class_list = sqlheper.get_list( "select id,title from myapp_class",[] )
        current_student_info = sqlheper.get_one("select id,stu_name,class_id_id from myapp_student where id=%s",[nid,])
        return render(request, 'myApp/editstudent.html',{"class_list":class_list,"current_student_info":current_student_info})
    else:
        nid = request.GET.get("nid")
        stu_name = request.POST.get("stu_name")
        class_id_id = request.POST.get("class_id_id")
        sqlheper.modify("update myapp_student set stu_name=%s,class_id_id=%s where id=%s",[stu_name,class_id_id,nid,])
        return redirect('/students/')

def test(request):
    if not request.session.get('user_info'):            # 进行登陆判断，登陆后才可以获得session，否张不能进行登陆。
        return redirect('/login/')
    else:
        return render(request, 'myApp/test.html')

def test1(request):
    return render(request, 'myApp/test1.html')

def jicheng(request):
    return render(request, 'myApp/jicheng.html')

def daily(request):
    return render(request, 'myApp/daily.html')

def power(request):
    return render(request, 'myApp/power.html')

def month(request):
    return render(request, 'myApp/month.html')

def year(request):
    return render(request, 'myApp/year.html')

def empty(request):
    user_list = User.objects.all()
    return render(request, 'myApp/empty.html',{'user_list':user_list})

def csrf1(request):
    if request.method == "GET":
        return render(request,'myapp/csrf1.html')
    else:
        return HttpResponse('ok')

def template1(request):
    return render(request,'myapp/template1.html',{"name":'yyj'})

def session_login(request):
    if request.method == "GET":
        return render(request,'myapp/session_login.html')
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        if u == 'alex' and p == '123':
            request.session['username'] =  'alex'
            return redirect('/session_success/')
        else:
            return render(request,'myapp/session_login.html',{'msg':'用户名或者密码错误'})

def session_success(request):
    #1.获取客户端cookie中随机字符串
    #2.去session中查找有没有随机字符串
    #3.去session对应key的value中查看有没有username
    v = request.session.get('username')
    if v:
        return HttpResponse('登陆成功:%s' %v)
    else:
        return redirect('/session_login/')

from utils.pager_user import PageInfo2
def user_managet(request):
    all_count = User.objects.all().count()  # 取该数据的总条数,取数据小于22条,用于显示分页
    page_info = PageInfo2(request.GET.get("page"), all_count, 6, '/user_managet',5)  # 10:10条数据   11：11个页码，current_page = request.GET.get("page")    获取当前页
    user_list = User.objects.all()[page_info.start():page_info.end()]  # 调用类获取数据
    return render(request, 'myApp/user_managet.html', {"user_list": user_list, 'page_info': page_info})

def modal_add_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    phone = request.POST.get('phone')
    Email = request.POST.get('Email')
    # 判断输入数据是否为空
    if len(username) > 0 and len(password) > 0 and len(phone) > 0 and len(Email) > 0:
        if password != password2:
            return HttpResponse('两次输入密码不一致')
        else:
            same_name_user = User.objects.filter(username=username)
            if same_name_user:
                return HttpResponse('用户名已存在')
            else:
                same_Email_user = User.objects.filter(Email=Email)
                if same_Email_user:
                    return HttpResponse('邮箱已经被注册')
                else:
                    User.objects.create(username=username,password=password,phone=phone, Email=Email)
                    return HttpResponse('ok')
    else:
        return HttpResponse("内容不能为空")

def modal_edit_user(request):
    ret = {'status': True, 'message': None}
    try:
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('Email')
        nid = request.POST.get('nid')
        User.objects.filter(id=nid).update(username=username,phone=phone,Email=email,)
        #sqlheper.modify('update myapp_User set username=%s,phone=%s,Email=%s where id=%s', [username, phone, email, nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"
    import json
    return HttpResponse(json.dumps(ret))

def deluser(request):
    nid = request.GET.get('nid')
    User.objects.filter(id=nid).delete()
    return redirect('/user_managet/')
    #return redirect('/user_managet/')

def modal_edit_password(request):
    o_password = request.POST.get('o_password')
    n_password = request.POST.get('n_password')
    n_password2 = request.POST.get('n_password2')
    nid = request.POST.get('nid')
    if len(o_password) > 0 and len(n_password) > 0 and len(n_password2) > 0:
        o_user = User.objects.filter(id=nid,password=o_password)                  #查询指定条件的值
        if o_user:
            if n_password != n_password2:
                return HttpResponse("两次密码输入不一致")
            else:
                User.objects.filter(id=nid).update(password=n_password)
                return HttpResponse('ok')
        else:
            return HttpResponse("原始密码错误")
    else:
        return HttpResponse("内容不能为空")

def Alarm(request):
    return render(request, 'myApp/Alarm.html')

