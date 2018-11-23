from django import forms
from django_redis import get_redis_connection

from sp_user.models import SpUser
class ForgetModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码长度不能大于16个字符',
                                    'min_length': '密码长度必须大于6个字符',
                                }
                                )
    password2 = forms.CharField(error_messages={'required': "确认密码必填"})
    verify_code = forms.CharField(error_messages={'required':"验证码必填"})
    class Meta:
        model = SpUser
        fields = ['phone', ]
        error_messages = {
            "phone": {
                "required": "手机号码必须填写!"
            }
        }

    # 验证两个密码是否一致
    def clean_password2(self):

        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("两次密码输入不一致!")
        return pwd2

    # 验证手机号码是否唯一
    def clean_phone(self):

        phone = self.cleaned_data.get('phone')
        rs = SpUser.objects.filter(phone=phone)
        if not rs:
            raise forms.ValidationError("这个电话还没注册")


    def clean_verify_code(self):
        # 获取用户表单提交的
        phone = self.cleaned_data.get("phone")
        verify_code = self.cleaned_data.get('verify_code')
        # 获取redis中的
        r = get_redis_connection("default")
        if phone:
            # 获取 redis中获取的值 是二进制编码,必须解码
            code = r.get(phone)
            code = code.decode("utf-8")
            if code is None:
                raise forms.ValidationError("验证码已经过期或者错误!")
            if verify_code != code:
                raise forms.ValidationError("验证码填写错误!")
            # 最后返回当前字段清洗后的结果
            return verify_code
        else:
            return verify_code
    # def clean_checkbox(self):
    #     checkbox = self.

class RegModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必填',
                                    'max_length': '密码长度不能大于16个字符',
                                    'min_length': '密码长度必须大于6个字符',
                                }
                                )
    password2 = forms.CharField(error_messages={'required': "确认密码必填"})
    verify_code = forms.CharField(error_messages={'required':"验证码必填"})
    class Meta:
        model = SpUser
        fields = ['phone', ]
        error_messages = {
            "phone": {
                "required": "手机号码必须填写!"
            }
        }

    # 验证两个密码是否一致
    def clean_password2(self):

        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("两次密码输入不一致!")
        return pwd2

    # 验证手机号码是否唯一
    def clean_phone(self):

        phone = self.cleaned_data.get('phone')
        rs = SpUser.objects.filter(phone=phone).exists()
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        return phone

    def clean_verify_code(self):
        # 获取用户表单提交的
        phone = self.cleaned_data.get("phone")
        verify_code = self.cleaned_data.get('verify_code')
        # 获取redis中的
        r = get_redis_connection("default")
        if phone:
            # 获取 redis中获取的值 是二进制编码,必须解码
            code = r.get(phone)
            code = code.decode("utf-8")
            if code is None:
                raise forms.ValidationError("验证码已经过期或者错误!")
            if verify_code != code:
                raise forms.ValidationError("验证码填写错误!")
            # 最后返回当前字段清洗后的结果
            return verify_code
        else:
            return verify_code
    # def clean_checkbox(self):
    #     checkbox = self.


# 登录表单
class LoginModelForm(forms.ModelForm):
    """登陆的form表单"""

    class Meta:
        model = SpUser
        fields = ['phone', 'password']

        error_messages = {
            'phone': {
                "required": "手机号码必须填写!"
            },
            'password': {
                "required": "密码必须填写!"
            }
        }
        widgets = {
            'phone': forms.TextInput(attrs={"class": "login-name", "placeholder": '请输入手机号'}),
            'password': forms.PasswordInput(attrs={"class": "login-password", "placeholder": '请输入密码'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        # 获取用手机和密码
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([phone, password]):
            # 根据手机号码获取用户
            try:
                user = SpUser.objects.get(phone=phone)
            except SpUser.DoesNotExist:
                raise forms.ValidationError({"phone": "该用户不存在!"})

            # 判断密码是否正确
            if user.password != password:
                raise forms.ValidationError({"password": "密码填写错误!"})
            cleaned_data['user'] = user
            return cleaned_data
        else:
            return cleaned_data
