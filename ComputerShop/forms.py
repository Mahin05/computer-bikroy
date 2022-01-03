from django.contrib.auth.models import User
from django import forms
from ComputerShop.models import product
from ComputerShop.models import userprofile

class UserForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ['username','email','password']
        widgets = {'password':forms.PasswordInput}

class ProductForm(forms.ModelForm):
    class Meta :
        model = product
        # fields = ['brand','model','price','image']
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta :
        model = userprofile
        fields = ['phone','location']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class EditPostForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('brand','model','condition','price','details','image')