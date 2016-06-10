import re

from django import forms
from django.contrib.auth import authenticate
from ask.models import Profile, Question, Tag


class TestUpload(forms.Form):
    avatar = forms.FileField(
        label='Select a file',
    )


class RegistrationForm(forms.Form):
    label_suffix = ''
    common_attrs = {'class' : 'form-control'}

    username = forms.CharField(
        label='Login', max_length=30,
        widget=forms.TextInput(attrs=common_attrs))
    email = forms.EmailField(
        label='Email', max_length=30,
        widget=forms.EmailInput(attrs=common_attrs))
    nickname = forms.CharField(
        label='Nickname', max_length=30,
        widget=forms.TextInput(attrs=common_attrs))
    password = forms.CharField(
        label='Password', max_length=40,
        widget=forms.PasswordInput(attrs=common_attrs))
    re_password = forms.CharField(
        label='Repeat password', max_length=40,
        widget=forms.PasswordInput(attrs=common_attrs))
    avatar = forms.FileField(
        label='Avatar')
    url = forms.CharField(
        max_length=40,
        widget=forms.HiddenInput())

    def clean_url(self):
        url = self.cleaned_data['url']
        if '.' in url:
            url = '/'
            raise forms.ValidationError('Url to a different site', code=10)
        return url

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r"^[A-Za-z0-9_-]{3,30}$", username):
            raise forms.ValidationError('Username may contains only letters and decimals', code=9)
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if not re.match(r"^[A-Za-z0-9_-]{3,30}$", nickname):
            raise forms.ValidationError('Nickname may contains only letters and decimals', code=8)
        return nickname

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.match(r"^[A-Za-z0-9_-]{3,30}$", password):
            raise forms.ValidationError('Password may contains only letters and decimals', code=8)
        return password

    def clean_re_password(self):
        re_password = self.cleaned_data['re_password']
        if re_password != self.cleaned_data['password']:
            pass
            #raise forms.ValidationError('Passwords must be equals', code=8)
        return re_password

    def clean(self):
        # Create user
        # If exist -> Exception
        pass

    def save(self):
        user = Profile.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            #nickname=self.cleaned_data['nickname'],
            password=self.cleaned_data['password'],
            avatar=self.cleaned_data['avatar']
        )
        if (user):
            return authenticate(username=self.cleaned_data['username'],
                        password=self.cleaned_data['password'])

    def get_url(self):
        return self.cleaned_data['url']


class AuthForm(forms.Form):
    #required_css_class = 'form-control'
    label_suffix = ''
    common_attrs = {'class' : 'form-control'}

    username = forms.CharField(
        label='Login',
        max_length=30,
        widget=forms.TextInput(attrs=common_attrs))
    password = forms.CharField(
        label='Password',
        max_length=30,
        widget=forms.PasswordInput(attrs=common_attrs))
    url = forms.CharField(
        max_length=40,
        widget=forms.HiddenInput())

    def clean_url(self):
        url = self.cleaned_data['url']
        if '.' in url:
            url = '/'
            #raise forms.ValidationError('Url to a different site', code=10)
        return url

    def clean(self):
        self.user = authenticate(username=self.cleaned_data['username'],
                        password=self.cleaned_data['password'])
        if self.user is None:
            raise forms.ValidationError('Login or password incorrect', code=10)

    def authenticate(self):
        return self.user

    def get_url(self):
        return self.cleaned_data['url']


class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=128)


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 128:
            raise forms.ValidationError(
                u'Заголовок слишком длинный', code=1)
        return title

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 128:
            raise forms.ValidationError(
                u'Пожалуйста, используйте меньше тегов или сократите их длинну', code=2)

        tags = tags.replace(" ", "")
        return tags

    def save(self, profile):
        question = Question.objects.create(
            author=profile,
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content'],
        )
        tags = self.cleaned_data['tags'];
        tags = tags.split(",")
        for tag in tags:
            obj, created = Tag.objects.get_or_create(text=tag)
            question.tags.add(obj)

        return question
