from django.shortcuts import render
from django.views.generic.base import View

from message_test.consts import MessageType


class Message(View):
    def get(self, request, message_type):
        data = {}
        try:
            obj = MessageType[message_type]
        except Exception as e:
            data['error'] = "error input"
            return render(request, 'message.html', data)

        message = request.GET.get('message', '')
        if not message:
            data['error'] = 'kong input'
            return render(request, 'message.html', data)

        data['message'] = message
        data['message_type'] = obj
        return render(request, 'message.html', data)
