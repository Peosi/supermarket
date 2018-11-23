from django import forms
from django.core import validators

from sp_user.models import Users

#注册表单
class RegForm(forms.ModelForm):
    pwd2 = forms.CharField(max_length=16,
                           min_length=6,
                           label="确认密码",
                           strip=True,
                           error_messages={
                               "required": "请填写重复密码"
                           }
                           )
    class Meta:
        model = Users
        exclude = ['isDelete']
        widgets = {
            "mobile": forms.TextInput(attrs={'class': "form-control"}),
            "password": forms.PasswordInput(attrs={'class': "form-control"}),
        }
        labels = {
            "mobile": "手机号",
            "password": "密码",
        }
        error_messages = {
            "mobile": {'required': '手机号不能为空!'},
            "password": {'required': '密码不能为空!', 'min_length': "密码长度必须大于6", 'max_length': "密码长度必须小于16"},
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        rs = Users.objects.filter(mobile=mobile).exists()
        if rs:
            raise forms.ValidationError("手机号已被注册,请换个!")
        else:
            return mobile

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['mobile'].validators.append(validators.RegexValidator(r'^1[3-9]\d{9}$',"手机号码格式错误"))

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password')
        pwd2 = cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError({"pwd2": "两次密码不一致!"})
        else:
            if all((pwd1, pwd2)):
                cleaned_data['password'] = pwd
            return cleaned_data

#登录表单
class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['mobile', 'password']
        labels = {
            "mobile": "手机号",
            "password": "密码",
        }
        error_messages = {
            'mobile': {'required': '手机号不能为空^_^'},
            'password': {'required': '密码不能为空'},
        }