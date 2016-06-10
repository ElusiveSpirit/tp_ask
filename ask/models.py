import datetime
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

    def get_avatar_url(self):
        return 'uploads/' + self.avatar.url

    class Meta:
        db_table = 'ask_profiles'
        #ordering = ['-created_at']


class Tag(models.Model):
    text = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'ask_tags'


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


class Question(models.Model):

    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey(Profile)
    created_at = models.DateTimeField(blank = True, auto_now_add=True)
    rating = models.IntegerField(blank=True, default=0)
    #answers_count = models.IntegerField(blank=True, default=0)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_rating(self):
        return Like.objects.filter(question=self).count()

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_absolute_url(self):
        return '/question/%d/' % self.pk

    class Meta:
        db_table = 'ask_questions'
        ordering = ['-created_at']


class Answer(models.Model):

    content = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(Profile)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.content

    def get_rating(self):
        return Like.objects.filter(answer=self).count()

    class Meta:
        db_table = 'ask_answers'
        ordering = ['-created_at']


class Like(models.Model):
    """Like model for db"""

    profile = models.ForeignKey(Profile)
    like = models.BooleanField()
    question = models.ForeignKey(Question, null=True)
    answer = models.ForeignKey(Answer, null=True)
    #rating = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)


    def __str__(self):
        return self.profile.username + ' = ' + str(self.like)
