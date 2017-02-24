from django import forms
from django.contrib.auth import (authenticate,
                                 get_user_model,
                                 login,
                                 logout,
                                 )


User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email address', required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('There are no such user!')
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password.')
        if not user.is_active:
            raise forms.ValidationError('User is no more active.')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address', required=True)
    email2 = forms.EmailField(label='Confirm email', required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', max_length=30, required=False)
    # last_name = forms.CharField(label='Last name', max_length=30, required=False)
    # birthday = forms.DateField(label='Birthday', required=False)
    country = forms.CharField(label='Country', max_length=30, required=False)
    city = forms.CharField(label='City', max_length=30, required=False)

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if not email == email2:
            raise forms.ValidationError('Oops. Check your amail address.')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password == password2:
            raise forms.ValidationError('Oops. Check your password.')
        return password2

    class Meta:
        model = User
        fields = ['email',
                  'email2',
                  'password',
                  'password2',
                  ]
