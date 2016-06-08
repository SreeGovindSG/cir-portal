from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap3_datetime.widgets import DateTimePicker
from captcha.fields import ReCaptchaField

from registration.models import *
from django.forms.models import ModelForm

class UploadFileForm(forms.Form):
    file = forms.FileField()

user_widgets = {
    'username'    : forms.TextInput(attrs={'placeholder':_('Username'), 'required': True}),
    'email'         : forms.TextInput(attrs={'placeholder':_('Your Email address'),
                                             'required': True}),
    'aums_id'       : forms.TextInput(attrs={'placeholder':_('Your AUMS ID'),
                                             'required': True}),  
}


user_fields = ['username', 'email', 'aums_id']

captcha_attrs = {'theme': 'clean', 'size': 'compact'}

class UserRegistrationForm(ModelForm):
    repass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re Enter Password',
                                                     'min_length':1, 'max_length':20}))

    class Meta:
        model = User
        fields = user_fields + ['password']
        widgets = user_widgets
        widgets['password'] = forms.PasswordInput(attrs={'placeholder':_('Password')})


    def clean(self):
        password, re_password = self.cleaned_data.get('password'), self.cleaned_data.get('repass')
        if password and password != re_password:
            raise forms.ValidationError(_("Passwords don\'t match"))
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Email "%s" is already in use.') % email)
        return email


    def clean_repass(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('repass')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don\'t match"))
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user

student_fields = ['name','curr_course','branch','tenth_mark','twelth_mark',
                  's1','s2','s3','s4','s6','cgpa','curr_arrears','hist_arrears']

class StudentRegistrationForm(ModelForm):

    class Meta:
        model = Student
        fields = ['aums_id'] + student_fields




