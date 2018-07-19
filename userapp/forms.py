from django import forms
from django.core.exceptions import ValidationError

from userapp.models import User


class RegistForm(forms.ModelForm):
    password2 = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username','password','password2']

    def clean_username(self):
        # 验证用户名
        username = self.cleaned_data.get('username')
        if username != '' and username.isalnum():
            # 防sql注入验证（用户名只能为字母和数字）
            if len(username.strip()) >= 8:
                return username
            else:
                raise ValidationError('用户名长度至少为8位')
        raise ValidationError('用户名只能为字母和数字')

    def clean_password(self):
        # 验证用户名
        password = self.cleaned_data.get('password')
        if password.find(';')==-1 and password.find('"')==-1 and password.find("'")==-1:
            # 防sql注入验证
            if len(password.strip()) >= 6:
                return password
            else:
                raise ValidationError('密码长度至少为6位')
        raise ValidationError('密码不能包含分号或引号')

    # 验证二次密码
    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 != pwd2:
            raise ValidationError('两次口令不相同')
        return pwd2