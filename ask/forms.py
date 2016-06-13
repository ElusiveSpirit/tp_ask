import re
import logging

from django import forms
from django.contrib.auth import authenticate
from ask.models import Profile, Question, Tag, Like, Answer

logger = logging.getLogger('ask.models.errors')

class TestUpload(forms.Form):
    avatar = forms.FileField(
        label='Select a file',
    )


class EditProfileForm(forms.Form):
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
    avatar = forms.FileField(
        required=False,
        label='Avatar',
        widget=forms.FileInput(attrs=common_attrs))

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
            first_name=self.cleaned_data['nickname'],
            password=self.cleaned_data['password'],
            avatar=self.cleaned_data['avatar']
        )
        if (user):
            return authenticate(username=self.cleaned_data['username'],
                        password=self.cleaned_data['password'])

    def get_url(self):
        return self.cleaned_data['url']


class AuthForm(forms.Form):
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

    def get_url(self):
        return self.cleaned_data['url']


class CorrectAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['is_correct']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        self.question = kwargs.pop('question', None)
        super(CorrectAnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CorrectAnswerForm, self).clean()
        if self.instance.question != self.question:
            raise forms.ValidationError("Wrong question and answer")

        if self.question.author.pk != self.profile.pk:
            raise forms.ValidationError("User is not owner")


class AddLikeForm(forms.ModelForm):
    obj_id = forms.IntegerField()

    class Meta:
        model = Like
        fields = ['like']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        self.obj = kwargs.pop('obj', None)
        self.user_like = None
        super(AddLikeForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(AddLikeForm, self).clean()
        obj_id = self.cleaned_data['obj_id']
        try:
            self.obj = self.obj.objects.get(pk=obj_id)
        except self.obj.DoesNotExist:
            raise forms.ValidationError(str(self.obj) + ' does not exist')

        try:
            if self.obj.author.pk == self.profile.pk:
                raise forms.ValidationError('Current user is question\'s author')
        except Profile.DoesNotExist:
            raise forms.ValidationError('Author does not exist')

        user_like = self.obj.likes.filter(profile=self.profile)
        if user_like:
            if len(user_like) > 1:
                logger.error('Wrong likes: profile.pk=' + self.profile.pk + ', obj.pk=' + self.obj.pk)
                raise forms.ValidationError('Unexpected error')
            self.user_like = user_like[0]
            # if user liked it and now dislike
            # if user disliked it and now like
            if (self.user_like.like and self.cleaned_data['like'] or
                    not self.user_like.like and not self.cleaned_data['like']):
                raise forms.ValidationError('User is already liked or disliked it')
        return cleaned_data

    def save(self, commit=True):
        obj = super(AddLikeForm, self).save(commit=False)
        obj.profile = self.profile
        if self.user_like:
            self.obj.likes.remove(self.user_like)
            self.user_like.delete()
            self.result = 0
        elif commit:
            obj.save()
            self.obj.likes.add(obj)
            self.obj.save()
            if obj.like:
                self.result = 1
            else:
                self.result = -1;
        return obj

    def get_result(self):
        return self.result


class AddAnswerForm(forms.Form):
    content = forms.CharField()
    question_id = forms.IntegerField(
        widget=forms.HiddenInput())


class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=128)


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 60:
            raise forms.ValidationError(
                u'Title is too short. It should be between 60 and 128 characters. Now it has ' + str(len(title)), code=1)
        return title

    def clean_tags(self):
        tags = self.cleaned_data['tags']
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
