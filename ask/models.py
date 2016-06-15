import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User, UserManager
# Create your models here.


class TestUpload(models.Model):
    docfile = models.FileField()

    def get_avatar_url(self):
        url = self.docfile.url[1:]
        return 'uploads' + url

    class Meta:
        db_table = 'test'


class Profile(User):
    avatar = models.FileField(max_length=100, blank=True, default="avatar.png")
    objects = UserManager()

    def get_absolute_url(self):
        return reverse('ask:profile-detail', kwargs={'pk':self.pk})

    def get_avatar_url(self):
        return '/uploads/' + self.avatar.url

    class Meta:
        db_table = 'ask_profiles'
        #ordering = ['-created_at']


class Like(models.Model):
    """Like model for db"""

    profile = models.ForeignKey(Profile)
    like = models.BooleanField()
    created_at = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return (self.profile.username + ' = ' + str(self.like)
                    + " at " + str(self.created_at))


class Tag(models.Model):
    text = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'ask_tags'


class LikedMethods():
    likes = None

    def get_rating(self):
        return self.likes.filter(like=True).count() - self.likes.filter(like=False).count()

    def get_who_like_pk(self):
        authors = []
        for like in self.likes.filter(like=True):
            authors.append(like.profile.pk)
        return authors

    def get_who_dislike_pk(self):
        authors = []
        for dislike in self.likes.filter(like=False):
            authors.append(dislike.profile.pk)
        return authors

class QuestionManager(models.Manager):
    def best(self):
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=100)
        return self.filter(created_at__gt=one_year_ago).order_by('-rating', '-created_at')

    def new(self):
        return self

    def by_tag(self, tag):
        print(tag)
        tag = Tag.objects.filter(text=tag)
        return self.filter(tags__in=tag)


class Question(models.Model, LikedMethods):
    author = models.ForeignKey(Profile)
    title = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(blank = True, auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.ManyToManyField(Like, blank=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def has_correct_answer(self):
        return Answer.objects.filter(question=self, is_correct=True).count() > 0

    def get_url_with_answer_anchor(self, anchor):
        return self.get_absolute_url() + '#' + str(anchor)

    def get_absolute_url(self):
        return reverse('ask:question-detail', kwargs={'pk' : self.pk})
        #return '/question/%d/' % self.pk

    class Meta:
        db_table = 'ask_questions'
        ordering = ['-created_at']


class Answer(models.Model, LikedMethods):
    author = models.ForeignKey(Profile)
    content = models.TextField()
    question = models.ForeignKey(Question)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    likes = models.ManyToManyField(Like, blank=True)

    def __str__(self):
        return self.content

    def get_anchor(self):
        return 'answer_' + str(self.pk)

    class Meta:
        db_table = 'ask_answers'
        ordering = ['created_at']


# Not needed
class LikesField(models.ManyToManyField):

    def __init__(self, *args, **kwargs):
        super(LikesField, self).__init__(*args, **kwargs)

    def get_rating(self):
        return self.likes.filter(like=True).count() - self.likes.filter(like=False).count()

    def get_who_like_pk(self):
        authors = []
        for like in self.likes.filter(like=True):
            authors.append(like.profile.pk)
        return authors

    def get_who_like_pk(self):
        authors = []
        for dislike in self.likes.filter(like=False):
            authors.append(dislike.profile.pk)
        return authors
