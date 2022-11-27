from django.urls import path

from message_test.view import Message

urlpatterns = [
    # 此处的name是别名，用来和views中的reverse路由解析进行绑定。
    # View中有as_view方法
    path('index/<str:message_type>', Message.as_view(), name='message'),
]