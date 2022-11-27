from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission, Group
# HttpResponse返回字符串内容。 JsonResponse返回JSON类型，用于和ajax交互
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
# render用于渲染页面然后显示
from django.shortcuts import render, redirect
from django.urls import reverse
# 基于类的视图
from django.views.generic.base import View

from testapp.forms import Auth
from testapp.models import Test


def test(request, name, age):
    # 第二种从url中获取参数的方式，xxx/xxxx/xxx
    print(name, age)
    test_redis = Test(name="test_redis", age=19)
    test_redis.save()
    Test.objects.create(name="test_redis1", age=191)
    print(test_redis.get("test_redis"))
    return HttpResponse("url test")


class Register(View):
    def get(self, request):
        # 是否登陆了，如果已经登录了就跳转到首页。
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request, 'register.html')

    def post(self, request):
        # url中?name=xxx&xxx方式向后台传入参数的方法,用这个方式不能在views中路径使用后面使用/
        username = request.POST.get('username', '')
        pwd = request.POST.get('pwd', '')
        pwd1 = request.POST.get('pwd1', '')
        if pwd != pwd1:
            # HttpResponse返回值给前端界面。
            return HttpResponse("error: different input pwd")
        # check is exist
        exists = User.objects.filter(username=username).exists()
        if exists:
            return HttpResponse("error: exist user")
        User.objects.create_user(username=username, password=pwd)
        # 是reverse而不是reversed注意，否则会报错
        return redirect(reverse('login'))


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        pwd = request.POST.get('pwd', '')

        exist = User.objects.filter(username=username).exists()
        if not exist:
            return HttpResponse("error: no this user")
        # 验证是否用户名密码是相同的，如果是授权
        user = authenticate(username=username, password=pwd)
        if not user:
            return HttpResponse("error: username or password!")
        login(request, user)
        # 是reverse而不是reversed注意，否则会报错
        return redirect(reverse('index'))


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))

    def post(self, request):
        pass


class Index(View):
    def get(self, request):
        # render用于渲染页面然后显示参数：request，想要返回的页面，页面参数，这样就不需要在路由里面添加参数。
        list_data = [1, 2, 3, 4, 5, 6]
        # 这个其实是template和模板的绑定
        return render(request, 'index.html', {"name": "lzy", "list_data": list_data})

    def get1(self, request, name):
        # render用于渲染页面然后显示参数：request，想要返回的页面，页面参数，这样需要在路由里面添加参数。
        return render(request, 'index.html', {"name": name})

    def post(self, request):
        pass


class RegisterForm(View):
    def get(self, request):
        form = Auth()
        return render(request, 'register_form.html', {'form': form})

    def post(self, request):
        form = Auth(request.POST)
        if form.is_valid():
            # cleaned_data 就是读取表单返回的值，返回类型为字典dict型
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            return HttpResponse('username is {}, password is {}'.format(username, password))
        else:
            return render(request, 'register_form.html', {'form': form})


class A(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'not_permission.html')
        else:
            # 赋权
            a_permission = Permission.objects.get(codename='look_a_page')
            request.user.user_permissions.add(a_permission)
            if not request.user.has_perm('app.look_a_page'):
                return render(request, 'a.html')


class B(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'not_permission.html')
        else:
            # 获取指定用户
            user = User.objects.get(username='test')
            # 创建组
            Group.objects.get_or_create(name='b_page')
            # 获取组
            group = Group.objects.get(name='b_page')
            b_permission = Permission.objects.filter(codename='look_b_page').first()

            for per in Permission.objects.filter(content_type_id=1):
                group.permissions.add(per)

            # 用户添加到组
            user.groups.add(group)

            # 查看用户是否有某个权限,使用Q来进行数据库查找
            b_permission = Permission.objects.filter(codename='look_b_page').first()
            users = User.objects.filter(Q(groups__permissions=b_permission) | Q(user_permissions=b_permission)).distinct()
            if request.user not in users:
                return HttpResponse("no permission")



