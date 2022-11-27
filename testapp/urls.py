from django.urls import path
from .view import Index, Register, Login, Logout, test, RegisterForm, A

urlpatterns = [
    # 此处的name是别名，用来和views中的reverse路由解析进行绑定。
    # View中有as_view方法
    path('index/', Index.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('test/<str:name>/<int:age>', test),
    path('register_form/', RegisterForm.as_view(), name='register_form'),
    path('a/', A.as_view(), name='a')
]