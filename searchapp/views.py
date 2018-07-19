from django.shortcuts import render

# Create your views here.
from userapp.models import User


def home(request):
    # 主页接口
    # 获取登录用户token
    tok = request.session.get('login_user')
    data = {}
    if tok:
        data['username'] = User.objects.get(token=tok).username
        if not User.objects.get(token=tok).image:
            data['photo'] = '1.png'
        else:
            data['photo'] = User.objects.get(token=tok).image
    return render(request, 'home.html',{'data':data})


def changecity(request):
    # 切换城市
    return None


def search(request):
    # 获取登录用户token
    tok = request.session.get('login_user')
    data = {}
    if tok:
        data['username'] = User.objects.get(token=tok).username
        if not User.objects.get(token=tok).image:
            data['photo'] = '1.png'
        else:
            data['photo'] = User.objects.get(token=tok).image
    return render(request, 'smallsearch.html',{'data': data})