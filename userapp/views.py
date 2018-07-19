
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from userapp.forms import RegistForm
from userapp.models import User
from userapp.tools import *


def login(request):
    # 登录接口
    if request.method == 'GET':
        # 判断目前是否已经有用户
        print('%%%%%%%%%%%%%%%%%',request.COOKIES.get('login_user'))
        if request.COOKIES.get('login_user'):
            return redirect('/home/')
        return render(request, 'login.html')

    # 用户登录
    # 获取表单中的数据，以便返回表单
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    verifycode = request.POST.get('txt_Code', '')

    # 验证验证码
    if not checkCode(request, verifycode):
        return render(request, 'login.html',
                      {'username': username, 'password': password, 'code': verifycode,
                       'errorcode': '验证码输入有误'})

    user = User.objects.filter(username=username,password=password).first()
    if user:
        resp = redirect('/home/')
        # 生成token，并保存到cookie和session中
        tok = token()
        request.session['login_user'] = tok
        if request.POST.get('cbx_keepState') == '1':
            resp.set_cookie('login_user', tok)
            # 把token存入到用户表中
            user.token = tok
            user.save()
            return resp
        return resp
    return render(request, 'login.html',
                      {'username': username, 'password': password, 'code': verifycode,
                       'errorcode': '用户名密码不匹配'})


def regist(request):
    # 注册接口
    if request.method == 'GET':
        return render(request, 'regist.html')

    # 获取表单中的数据，以便返回表单
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    password2 = request.POST.get('password2','')
    verifycode = request.POST.get('txt_Code','')

    # 验证验证码
    if not checkCode(request, verifycode):
        return render(request, 'regist.html',
            {'username':username,'password':password,'password2':password2,'code':verifycode,'errorcode':'验证码输入有误'})
    # 验证用户名是否已存在
    user = User.objects.filter(username=username).last()
    if user:
        return render(request, 'regist.html',
            {'username':username,'password':password,'password2':password2,'code':verifycode,'erroruname':'用户名已存在'})

    # 用户注册
    form = RegistForm(request.POST)
    if form.is_valid():
        # 保存数据到数据库
        form.save()
        # 生成token，并保存到cookie和session中
        tok = token()
        request.session['login_user'] = tok
        # 判断是否含有自助登录
        if request.POST.get('cbx_keepState') == '1':
            # 自助登录，返回主页
            resp = redirect('/home/')
            resp.set_cookie('login_user',tok)
            # 把token存入到用户表中
            user = User.objects.get(username=username)
            user.token = tok
            user.save()
            return resp
        else:
            return redirect('/user/login/')
    else:
        return render(request, 'regist.html',
            {'form':form, 'errors':form.errors,
             'username': username, 'password': password, 'password2': password2, 'code': verifycode})

# 验证码接口
def verifycode(request):
    codeImg = proverifycode(request)
    return HttpResponse(codeImg,
                        content_type='image/png')

# 退出
def logout(request):
    tok = request.session.get('login_user')
    if tok:
        try:
            user = User.objects.get(token=tok)
            user.token = ''
            user.save()
            resp = redirect('/home/')

            # 退出时，从客户端中删除token,服务端删除token
            resp.delete_cookie('login_user')
            request.session.flush()
            return resp
        except:
            pass


def modify(request):
    # 修改密码
    if request.method == 'GET':
        return render(request, 'modify.html')

    # POST
    # 获取表单中的数据，以便返回表单
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    password2 = request.POST.get('password2', '')
    verifycode = request.POST.get('txt_Code', '')

    # 验证验证码
    if not checkCode(request, verifycode):
        return render(request, 'modify.html',
                      {'username': username, 'password': password, 'password2': password2, 'code': verifycode,
                       'errorcode': '验证码输入有误'})
    # 验证用户名是否已存在
    user = User.objects.filter(username=username).last()
    if not user:
        return render(request, 'modify.html',
                      {'username': username, 'password': password, 'password2': password2, 'code': verifycode,
                       'erroruname':'用户不存在'})
    # 开始修改
    form = RegistForm(request.POST)
    if form.is_valid():
        # 生成token
        tok = token()
        user.password = password
        user.token = tok
        user.save()
        # 判断是否含有自助登录
        if request.POST.get('cbx_keepState') == '1':
            # 生成token，并保存到cookie和session中
            request.session['login_user'] = tok
            # 自助登录，返回主页
            resp = redirect('/home/')
            resp.set_cookie('login_user', tok)
            return resp
        else:
            return redirect('/user/login/')
    else:
        return render(request, 'modify.html',
            {'form':form, 'errors':form.errors,
             'username': username, 'password': password, 'password2': password2, 'code': verifycode})
