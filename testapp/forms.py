from django import forms
from django.forms import fields

from testapp.models import Test


class Auth(forms.Form):
    username = fields.CharField(
        label='username',
    )

    password = fields.CharField(
        # HTML插件类型
        widget=forms.PasswordInput(),
        label='password',
        min_length=5,
        # 在使用instance时会显示password到界面，但是是***
        # render_value=True
    )

    # 全局验证,方法重写
    def clean(self):
        username = self.changed_data.get('username', '')
        password = self.changed_data.get('password', '')
        if not username:
            raise forms.ValidationError('username is none')

    # 单独验证。方法名称固定clean_属性。
    def clean_username(self):
        username = self.changed_data.get("username", "")
        if not username:
            raise forms.ValidationError('username is none1')


# 模型表单
class AuthModelForm(forms.ModelForm):
    class Meta:
        # 绑定模型
        model = Test

        # 渲染我们想要展示的模型字段
        fields = ['name', 'age']

        # 渲染模型的所有字段。
        # fields = '__all__'
