#!/usr/bin/python2.7
from django.core.management import setup_environ
from project import settings
setup_environ(settings)
from django.db import connection
import ask.models.py
#cursor = connection.cursor()

tag = Tag(text="first"); t.save()

profile = Profile(login="Konstantin", email="test@test.com", nickname="Solleks", password="0000")
profile.save();

question = Question(title="Test title", content="Hello World", author=profile, rating=0)
question.tags.add(tag)

question.save()
