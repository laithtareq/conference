from django import forms
from django.contrib.auth.models import User
from .models import newManuscript,Comment,Profile,PDF_Files
class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='User Name',max_length=50)
    email = forms.EmailField(label='e-mail')
    first_name = forms.CharField(label='First Name',max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    password1=forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(),min_length=8)
    password2 = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput(),min_length=8)
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1']!=cd['password2']:
            raise forms.ValidationError('كلمة السر غير مطابقة')
        return cd['password2']
    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('اسم المستخدم مكرر')
        return cd['username']
class newManuscriptForm(forms.ModelForm):
    ispaperoriginal = forms.BooleanField(label='All contents of this paper original',required=False)
    published = forms.BooleanField(label='Paper has been previously published',required=False)
    undercosideration = forms.BooleanField(label='Paper is under consideration',required=False)
    containcopyright = forms.BooleanField(label='Paper contain copyrighted material',required=False)
    class Meta:
        model = newManuscript
        fields = ('title','category','text','ispaperoriginal','published','undercosideration','containcopyright','file','fileImg')
class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='e-mail')
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
class PDFUpdateForm(forms.ModelForm):
    class Meta:
        model = PDF_Files
        fields = ('file','manuscript',)